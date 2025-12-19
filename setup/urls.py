from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from competicao.views import lista_salas, detalhes_sala, inscrever_sala

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('usuarios.urls')),
    path('', lista_salas, name='home'),
    path('sala/<int:sala_id>/', detalhes_sala, name='detalhes_sala'),
    path('chat/', include('chat.urls')),
    path('sala/<int:sala_id>/inscrever/', inscrever_sala, name='inscrever_sala')
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)