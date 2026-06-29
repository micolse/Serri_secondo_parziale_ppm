from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'choices', ChoiceViewSet, basename='choice')

urlpatterns = [
    path('', include(router.urls)),
]