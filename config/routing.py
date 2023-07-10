from django.urls import path, include
from rest_framework import routers

from oauth.views import UserViewSet
from apps.projects.views import ProjectViewSet, PostViewSet

router = routers.DefaultRouter()
router.register(r'user', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'posts', PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls))
]