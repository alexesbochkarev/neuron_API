from rest_framework import viewsets, mixins

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serialazers import UserSerialazer

User = get_user_model()


class UserViewSet(mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    serializer_class = UserSerialazer

    def get_queryset(self):
        user_id = self.request.user.id
        return User.objects.filter(id=user_id)
    
