from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Personalização do Admin
admin.site.site_header = "Painel Administrativo Estudai"
admin.site.site_title = "Administração do Estudai"
admin.site.index_title = "Bem-vindo ao painel de administração do Estudai"

urlpatterns = [
    path("admin/", admin.site.urls),
    path('summernote/', include('django_summernote.urls')),
    path("", include("simulado.urls")),
    path("questao/", include("questao.urls")),
#    path("assunto/", include("assunto.urls")),
#    path("concurso/", include("concurso.urls")),    
#    path("materia/", include("materia.urls")),
#    path("questao/", include("questao.urls")),
#    path("respostausuario/", include("respostausuario.urls")),
]

# Adiciona as URLs de mídia APENAS em modo de desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)