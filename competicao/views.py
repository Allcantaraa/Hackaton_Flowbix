from django.shortcuts import render, get_object_or_404, redirect
from .models import Sala
from django.contrib.auth.decorators import login_required

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