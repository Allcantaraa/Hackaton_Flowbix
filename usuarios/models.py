from django.db import models
from django.contrib.auth.models import User

class Perfil(models.Model) :
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='avatares/', default='avatares/default.png', blank=True)
    
    def __str__(self):
        return f'Perfil do {self.usuario.username}'