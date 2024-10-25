from django.urls import path
from .views import upload_image
from .views import perfume_list, perfume_detail, create_perfume, perfume_update, perfume_delete
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('upload/',upload_image, name='upload_image'),
    path('', perfume_list, name='perfume_list'),  # Liste des parfums
    path('perfume/<int:perfume_id>/', perfume_detail, name='perfume_detail'),  # Détails d'un parfum
    path('perfume/new/', create_perfume, name='perfume_create'),  # Créer un parfum
    path('perfume/<int:perfume_id>/edit/', perfume_update, name='perfume_update'),  # Modifier un parfum
    path('perfume/<int:perfume_id>/delete/', perfume_delete, name='perfume_delete'),  # Supprimer un parfum

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)