from django.shortcuts import render
from .models import Sala
from django.contrib.auth.decorators import login_required

@login_required
def lista_salas(request) :
    salas = Sala.objects.all()
    
    return render (request, 'competicao/home.html', {'salas': salas})