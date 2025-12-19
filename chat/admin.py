from django.contrib import admin
from .models import Mensagem

@admin.register(Mensagem)
class MensagemAdmin(admin.ModelAdmin) :
    list_display = ('usuario', 'sala', 'texto', 'data_envio')
    list_filter = ('sala', 'usuario')