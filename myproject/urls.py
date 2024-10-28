from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("APP1.urls")),
    path('', include('auth_app.urls')),
    path('livraisons/', include('livraisons.urls')),
    path('trajets/', include('trajets.urls')),     
    path('perfumes/', include('perfumes.urls')),
    path('personality-test/', include('question.urls')),
    path('payment/', include('payment.urls')),
    path('commande_perso/', include('commande_perso.urls')),
    path('cart/', include('panier.urls')),  # Inclure les URLs du panier


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

