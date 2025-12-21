from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from competicao.views import lista_salas, detalhes_sala, inscrever_sala

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include('usuarios.urls')),
    path('', lista_salas, name='home'),
    path('sala/', include('competicao.urls')),
    path('chat/', include('chat.urls')),
    
]

if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)