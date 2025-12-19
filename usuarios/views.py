from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


def cadastro(request) :
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)
        
        if form.is_valid() :
            form.save()
            messages.success(request, f'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else :
        form = UserCreationForm()
            
    return render(request, 'usuarios/cadastro.html', {'form': form})