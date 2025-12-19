from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required

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

@login_required
def perfil(request) :
    if request.method == 'POST' :
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.perfil)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Seu perfil foi atualizado com sucesso!')
            return redirect('perfil')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.perfil)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'usuarios/perfil.html', context)