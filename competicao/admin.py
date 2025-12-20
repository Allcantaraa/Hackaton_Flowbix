from django.contrib import admin
from .models import Sala, Tema, Grupo, Avaliacao

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'status', 'criado_em')
    list_filter = ('status',)

@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'sala')

@admin.register(Grupo)
class GrupoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'sala', 'tema', 'lider', 'pontuacao_total')
    list_filter = ('sala', 'lider')

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('grupo', 'jurado', 'nota')
