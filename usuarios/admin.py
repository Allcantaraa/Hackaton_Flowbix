from django.contrib import admin
from .models import Perfil

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'foto', 'eh_jurado')
    
    list_editable = ('eh_jurado',)
    
    search_fields = ('usuario__username',)