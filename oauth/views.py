from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.shortcuts import render

from apps.projects.models import Project, Post
from . import serialazers

User = get_user_model()


def index(request):
    template = 'login.html'
    print(request.user)
    return render(request, template, {'request': request})


def profile(request):
    template = 'lk.html'
    print(request.user)
    return render(request, template)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin, 
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    
    permission_classes = (IsAuthenticated,)
    serializer_class = serialazers.UserDetailsSerializer
    queryset = User.objects.all()

    def get_queryset(self):
        user_id = self.request.user.id
        if self.action == 'list':
            return User.objects.filter(id=user_id)
        if self.action == 'projects':
            return Project.objects.filter(user=user_id)
        if self.action == "posts":
            return Post.objects.filter(user=user_id)
        return self.queryset
        
    def get_serializer_class(self):
        if self.action == "list" or "retrieve":
            return serialazers.UserSerialazer
        if self.action == "projects":
            return serialazers.ProjectSerialazer
        if self.action == "posts":
            return serialazers.PostsSerialazer
        return self.serializer_class   
    
    @action(detail=False)
    def projects(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def posts(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)



class UserDetailsView(mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Default accepted fields: username, first_name, last_name
    Default display fields: pk, username, email, first_name, last_name
    Read-only fields: pk, email

    Returns UserModel fields.
    """
    serializer_class = serialazers.UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        """
        return get_user_model().objects.none()