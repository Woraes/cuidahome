
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.urls import include


from central import urls as central_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include (central_urls)),
    path("select2/", include("django_select2.urls")),
]


#essa pomba aqui que faz ver a imagem no html em modo desenvolvimento aaaaaaa
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)