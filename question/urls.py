# urls.py
from django.urls import path
from .views import personality_test ,test_result , update_test , delete_test, capture_voice_input

urlpatterns = [
    path('', personality_test, name='personality_test'),
    path('test-result/<str:personality_type>/', test_result, name='test_result'),
    path('update-test/', update_test, name='update_test'),  
    path('personality-test/delete/', delete_test, name='delete_test'),
    path('voice/', capture_voice_input, name='capture_voice_input'),



]