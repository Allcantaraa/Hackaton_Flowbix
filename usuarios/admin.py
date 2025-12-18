from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    # Exibe o nome do usuário e o caminho da foto na lista do Admin
    list_display = ('usuario', 'foto')
    
    # Adiciona uma barra de pesquisa pelo nome do usuário
    search_fields = ('usuario__username',)