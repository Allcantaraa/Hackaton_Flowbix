from django.urls import path
from . import views

urlpatterns = [
    path('mensagens/<int:sala_id>/', views.buscar_mensagens, name='buscar_mensagens'),
    path('enviar/<int:sala_id>/', views.enviar_mensagem, name='enviar_mensagem'),
]