from django.db import models
from django.contrib.auth.models import User
from competicao.models import Sala

class Mensagem(models.Model) :
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, related_name='mensagens')
    texto = models.TextField(max_length=500, null=False, blank=False)
    data_envio = models.DateTimeField(auto_now_add=True)
    
    class Meta :
        ordering = ['data_envio']
    
    def __str__(self):
        return f'{self.usuario.username}: {self.texto[:20]}'