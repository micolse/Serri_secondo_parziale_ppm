from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from polls.views import register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include('polls.urls')),
    
    path('api/register/', register_user, name='register'),
    path('api/login/', obtain_auth_token, name='login'),
]