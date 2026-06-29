from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from polls.views import register_user

urlpatterns = [
    # Il pannello di amministrazione di Django
    path('admin/', admin.site.urls),
    
    # Colleghiamo tutti gli indirizzi dell'app polls sotto il prefisso 'api/'
    path('api/', include('polls.urls')),
    
    # Nuove rotte per la sicurezza (Login e Registrazione):
    path('api/register/', register_user, name='register'),
    path('api/login/', obtain_auth_token, name='login'),
]