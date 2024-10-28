from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    upload_image,
    perfume_list, perfume_detail, create_perfume, perfume_update, perfume_delete,
    description_list, description_create, description_update, description_delete
)

app_name = 'App1'  # Define namespace here

urlpatterns = [
    path('upload/', upload_image, name='upload_image'),
    path('', perfume_list, name='perfume_list'),  # List of perfumes
    path('perfume/<int:perfume_id>/', perfume_detail, name='perfume_detail'),  # Perfume details
    path('perfume/new/', create_perfume, name='perfume_create'),  # Create a perfume
    path('perfume/<int:perfume_id>/edit/', perfume_update, name='perfume_update'),  # Edit a perfume
    path('perfume/<int:perfume_id>/delete/', perfume_delete, name='perfume_delete'),  # Delete a perfume
    
    # Description paths within the 'App1' namespace
    path('descriptions/', description_list, name='description_list'),
    path('descriptions/create/', description_create, name='description_create'),
    path('descriptions/update/<int:id>/', description_update, name='description_update'),
    path('descriptions/delete/<int:pk>/', description_delete, name='description_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
