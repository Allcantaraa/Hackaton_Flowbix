from django.urls import path
from . import views

urlpatterns = [
    path('sala/<int:sala_id>/', views.detalhes_sala, name='detalhes_sala'),
    path('sala/<int:sala_id>/sortear/', views.realizar_sorteio, name='realizar_sorteio'),
    path('sala/<int:sala_id>/iniciar/', views.iniciar_sala, name='iniciar_sala'),
    path('sala/<int:sala_id>/inscrever/', views.inscrever_sala, name='inscrever_sala'),
    path('sala/<int:sala_id>/jurado/', views.painel_jurado, name='painel_jurado'),
    path('sala/<int:sala_id>/ranking/', views.ranking_sala, name='ranking_sala'),
    path('sala/<int:sala_id>/ranking/data/', views.ranking_data, name='ranking_data'),
]