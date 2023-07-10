from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .models import Project, Post
from .serialazers import ProjectSerialazer, PostSerialazer
from .permissions import IsAuthor

User = get_user_model()


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerialazer
    permission_classes = [IsAuthor, IsAuthenticated]
    queryset = Project.objects.all()

    # def get_queryset(self):
    #     user_id = self.request.user.id
    #     return Project.objects.filter(user=user_id)

    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerialazer
    permission_classes = [IsAuthor, IsAuthenticated]
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)