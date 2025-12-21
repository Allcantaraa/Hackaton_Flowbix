from django.shortcuts import render, get_object_or_404, redirect
from .models import Sala, Grupo, Entrega
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
import random

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
    
    grupo_liderado = Grupo.objects.filter(sala=sala, lider=request.user).first()
    meu_grupo = Grupo.objects.filter(sala=sala, membros=request.user).first()
    
    # --- LÓGICA DE VERIFICAÇÃO DE TEMPO ---
    tempo_esgotado = False
    if sala.status == 'andamento' and sala.inicio_atividades:
        # Calculamos o fim: inicio + (minutos * 60 segundos)
        fim_atividades = sala.inicio_atividades + timezone.timedelta(minutes=sala.duracao_horas) # 'duracao_horas' agora agirá como minutos
        if timezone.now() > fim_atividades:
            tempo_esgotado = True

    entrega = None
    if meu_grupo and hasattr(meu_grupo, 'entrega'):
        entrega = meu_grupo.entrega
    
    if request.method == 'POST' and 'btn_entrega' in request.POST:
        # SÓ PERMITE SE NÃO ESTIVER ESGOTADO
        if grupo_liderado and not tempo_esgotado:
            link = request.POST.get('link_projeto')
            comentario = request.POST.get('comentarios')
            Entrega.objects.update_or_create(
                grupo=grupo_liderado,
                defaults={'link_projeto': link, 'comentarios': comentario}
            )
            messages.success(request, 'Projeto entregue com sucesso!')
        elif tempo_esgotado:
            messages.error(request, 'O tempo acabou! Não é mais possível realizar entregas.')
            
        return redirect('detalhes_sala', sala_id=sala.id)
    
    contexto = {
        'sala': sala,
        'todos_os_grupos': todos_os_grupos,
        'liderando': grupo_liderado,
        'meu_grupo': meu_grupo,
        'entrega': entrega,
        'tempo_esgotado': tempo_esgotado # Enviamos para o template
    }
    return render(request, 'competicao/detalhes.html', contexto)

@staff_member_required
def realizar_sorteio(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    participantes = list(sala.participantes.all())
    temas = list(sala.temas.all())
    
    if len(participantes) < 1:
        messages.error(request, "Não há participantes inscritos para sortear.")
        return redirect('detalhes_sala', sala_id=sala.id)
    
    if not temas:
        messages.error(request, "Cadastre temas no Admin antes de realizar o sorteio.")
        return redirect('detalhes_sala', sala_id=sala.id)

    # 1. Limpa grupos antigos
    sala.grupos.all().delete()
    
    # 2. Define tamanho dos grupos (Ajustado para 2 para separar pessoas em testes)
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