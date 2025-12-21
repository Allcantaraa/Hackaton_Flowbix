from django.shortcuts import render, get_object_or_404, redirect
from .models import Sala, Grupo, Entrega
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
import random
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.db.models import Avg

@login_required
def lista_salas(request) :
    salas = Sala.objects.all()
    
    return render (request, 'competicao/home.html', {'salas': salas})


@login_required
def inscrever_sala(request, sala_id) :
    sala = get_object_or_404(Sala, id=sala_id)
    
    if sala.status != 'aberta' :
        messages.error(request, "As inscrições para esta sala já foram encerradas.")
        return redirect('home')
    
    sala.participantes.add(request.user)
    return redirect('detalhes_sala', sala_id=sala.id)

@login_required
def detalhes_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    todos_os_grupos = sala.grupos.all().prefetch_related('entrega', 'lider', 'membros')
    
    grupo_liderado = None
    meu_grupo = None
    tempo_esgotado = False
    
    if sala.status != 'aberta':
        grupo_liderado = Grupo.objects.filter(sala=sala, lider=request.user).first()
        meu_grupo = Grupo.objects.filter(sala=sala, membros=request.user).first()

    if sala.status == 'andamento' and sala.inicio_atividades:
        fim_atividades = sala.inicio_atividades + timezone.timedelta(minutes=sala.duracao_horas)
        
        if timezone.now() > fim_atividades:
            tempo_esgotado = True
            sala.status = 'finalizada'
            sala.save()
        
        elif todos_os_grupos.exists() and not todos_os_grupos.filter(entrega__isnull=True).exists():
            sala.status = 'finalizada'
            sala.save()
            messages.success(request, "Todas as equipes entregaram! Sala finalizada antecipadamente.")

    total_grupos = todos_os_grupos.count()
    total_jurados = User.objects.filter(perfil__eh_jurado=True).count()
    total_votos_sala = Avaliacao.objects.filter(grupo__sala=sala).count()
    
    avaliacoes_concluidas = False
    if total_grupos > 0 and total_jurados > 0:
        if total_votos_sala >= (total_grupos * total_jurados):
            avaliacoes_concluidas = True

    entrega = meu_grupo.entrega if meu_grupo and hasattr(meu_grupo, 'entrega') else None
    
    if request.method == 'POST' and 'btn_entrega' in request.POST:
        if sala.status != 'andamento':
            messages.error(request, "O portal de entrega está fechado!")
        elif grupo_liderado and not tempo_esgotado:
            link = request.POST.get('link_projeto')
            comentario = request.POST.get('comentarios')
            Entrega.objects.update_or_create(
                grupo=grupo_liderado,
                defaults={'link_projeto': link, 'comentarios': comentario}
            )
            messages.success(request, 'Projeto enviado com sucesso!')
        return redirect('detalhes_sala', sala_id=sala.id)
    
    contexto = {
        'sala': sala,
        'todos_os_grupos': todos_os_grupos,
        'liderando': grupo_liderado,
        'meu_grupo': meu_grupo,
        'entrega': entrega,
        'tempo_esgotado': tempo_esgotado,
        'avaliacoes_concluidas': avaliacoes_concluidas
    }
    return render(request, 'competicao/detalhes.html', contexto)

@staff_member_required
def realizar_sorteio(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    participantes = list(sala.participantes.filter(perfil__eh_jurado=False))
    temas = list(sala.temas.all())
    
    if len(participantes) < 1:
        messages.error(request, "Não há participantes inscritos para sortear.")
        return redirect('detalhes_sala', sala_id=sala.id)
    
    if not temas:
        messages.error(request, "Cadastre temas no Admin antes de realizar o sorteio.")
        return redirect('detalhes_sala', sala_id=sala.id)

    sala.grupos.all().delete()
    
    tamanho_max = 2 
    random.shuffle(participantes)
    num_grupos = (len(participantes) + tamanho_max - 1) // tamanho_max

    for i in range(num_grupos):
        if not participantes: break
        
        lider = participantes.pop(0)
        tema_sorteado = random.choice(temas)
        
        grupo = Grupo.objects.create(
            sala=sala,
            nome=f"Grupo {i+1}",
            lider=lider,
            tema=tema_sorteado
        )
        grupo.membros.add(lider)

        for _ in range(tamanho_max - 1):
            if participantes:
                membro = participantes.pop(0)
                grupo.membros.add(membro)

    sala.status = 'sorteio'
    sala.save()
    messages.success(request, f"Sorteio concluído! {num_grupos} grupos criados.")
    return redirect('detalhes_sala', sala_id=sala.id)

def iniciar_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    if request.method == 'POST' :
        horas = request.POST.get('duracao_horas', 24)
        sala.duracao_horas = int(horas)
        sala.inicio_atividades = timezone.now()
        sala.status = 'andamento'
        sala.save()
        return redirect('detalhes_sala', sala_id=sala.id)
    
    return redirect('detalhes_sala', sala_id=sala.id)

from .models import Avaliacao

@login_required
def painel_jurado(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    
    if not request.user.perfil.eh_jurado:
        messages.error(request, "Acesso restrito.")
        return redirect('detalhes_sala', sala_id=sala.id)

    grupos_para_avaliar = Grupo.objects.filter(sala=sala, entrega__isnull=False)

    if request.method == 'POST':
        grupo_id = request.POST.get('grupo_id')
        nota_valor = request.POST.get('nota')
        comentario = request.POST.get('comentario')
        
        grupo = get_object_or_404(Grupo, id=grupo_id)
        
        Avaliacao.objects.update_or_create(
            grupo=grupo,
            jurado=request.user,
            defaults={'nota': nota_valor, 'comentario': comentario}
        )
        
        media = grupo.avaliacoes.aggregate(Avg('nota'))['nota__avg']
        
        grupo.pontuacao_total = media
        grupo.save()

        messages.success(request, f"Avaliação do {grupo.nome} salva com sucesso!")
        return redirect('painel_jurado', sala_id=sala.id)

    return render(request, 'competicao/painel_jurado.html', {'sala': sala, 'grupos': grupos_para_avaliar})


@login_required
def ranking_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    return render(request, 'competicao/ranking.html', {'sala': sala})

@login_required
def ranking_data(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    grupos = sala.grupos.all().order_by('-pontuacao_total')
    
    total_jurados = User.objects.filter(perfil__eh_jurado=True).count()
    
    ranking_list = []
    votos_totais_concluidos = True
    
    for gp in grupos:
        num_votos = gp.avaliacoes.count()
        if num_votos < total_jurados:
            votos_totais_concluidos = False
            
        ranking_list.append({
            'nome': gp.nome,
            'lider': gp.lider.username,
            'pontuacao': float(gp.pontuacao_total or 0),
            'votos': f"{num_votos}/{total_jurados}"
        })
    
    return JsonResponse({
        'ranking': ranking_list,
        'concluido': votos_totais_concluidos,
        'status_sala': sala.status
    })