from django.shortcuts import render, get_object_or_404, redirect
from .models import Sala, Grupo, Entrega
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def lista_salas(request) :
    salas = Sala.objects.all()
    
    return render (request, 'competicao/home.html', {'salas': salas})

@login_required
def detalhes_sala(request, sala_id):
    sala = get_object_or_404(Sala, id=sala_id)
    return render(request, 'competicao/detalhes.html', {'sala': sala})

@login_required
def inscrever_sala(request, sala_id) :
    sala = get_object_or_404(Sala, id=sala_id)
    
    sala.participantes.add(request.user)
    return redirect('detalhes_sala', sala_id=sala.id)

@login_required
def detalhes_sala(request, sala_id) :
    sala = get_object_or_404(Sala, id=sala_id)
    
    grupo_liderado = Grupo.objects.filter(sala=sala, lider=request.user).first()
    
    meu_grupo = Grupo.objects.filter(sala=sala, membros=request.user).first()
    
    entrega = None
    
    if meu_grupo and hasattr(meu_grupo, 'entrega') :
        entrega = meu_grupo.entrega
    
    if request.method == 'POST' and 'btn_entrega' in request.POST :
        if grupo_liderado :
            link = request.POST.get('link_projeto')
            comentario = request.POST.get('comentarios')
            
            Entrega.objects.update_or_create(
                grupo=grupo_liderado,
                defaults={'link_projeto': link, 'comentarios': comentario}
            )
            messages.success(request, 'Projeto entregue!')
            return redirect('detalhes_sala', sala_id=sala.id)
        
    contexto = {
        'sala': sala,
        'liderando': grupo_liderado,
        'entrega': entrega
    }
    
    return render(request, 'competicao/detalhes.html', contexto)