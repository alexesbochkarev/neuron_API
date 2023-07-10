from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from apps.projects.models import Project, Post
from . import serialazers

User = get_user_model()



class UserViewSet(mixins.ListModelMixin,
                  viewsets.GenericViewSet):

    def get_queryset(self):
        user_id = self.request.user.id
        if self.action == 'list':
            return User.objects.filter(id=user_id)
        if self.action == 'projects':
            return Project.objects.filter(user=user_id)
        if self.action == "posts":
            return Post.objects.filter(user=user_id)
        
    def get_serializer_class(self):
        if self.action == "list":
            return serialazers.UserSerialazer
        if self.action == "projects":
            return serialazers.ProjectSerialazer
        if self.action == "posts":
            return serialazers.PostsSerialazer
    
    @action(detail=False)
    def projects(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def posts(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
