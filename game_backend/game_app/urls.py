from django.urls import path, include
from .views import UserViewSet, ScoreViewSet
from rest_framework.routers import DefaultRouter

router= DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'score', ScoreViewSet, basename='score')

urlpatterns = [
    path('', include(router.urls)),
]