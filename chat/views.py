from django.shortcuts import render
from .models import Mensagem
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from competicao.models import Sala

@login_required
def buscar_mensagens(request, sala_id) :
    mensagens = Mensagem.objects.filter(sala_id=sala_id).order_by('data_envio')[:50]
    
    dados = []
    
    for msg in mensagens :
        dados.append({
            'usuario': msg.usuario.username,
            'texto': msg.texto,
            'data': msg.data_envio.strftime('%H:%M')
        })
        
    return JsonResponse({'mensagens': dados})

@login_required
def enviar_mensagem(request, sala_id) :
    
    if request.method == 'POST' :
        texto = request.POST.get('texto')
        sala = get_object_or_404(Sala, id=sala_id)
        
        if texto :
            nova_msg = Mensagem.objects.create(
                usuario=request.user,
                sala=sala,
                texto=texto
            )
            
            return JsonResponse({
                'status': 'sucesso',
                'usuario': nova_msg.usuario.username,
                'texto': nova_msg.texto,
                'data': nova_msg.data_envio.strftime('%H:%M')
            })
            
    return JsonResponse({'status': 'erro'}, status=400)