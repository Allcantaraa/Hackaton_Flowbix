from django.urls import path
from . import views

urlpatterns = [
    path('sala/<int:sala_id>/', views.detalhes_sala, name='detalhes_sala'),
    path('sala/<int:sala_id>/sortear/', views.realizar_sorteio, name='realizar_sorteio'),
    path('sala/<int:sala_id>/iniciar/', views.iniciar_sala, name='iniciar_sala'),
    path('sala/<int:sala_id>/inscrever/', views.inscrever_sala, name='inscrever_sala')
]