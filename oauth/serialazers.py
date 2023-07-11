from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.tariffs.models import Tariff, Products
from apps.core.models import Interests, Result, Tool
from apps.projects.models import Project, Post


User = get_user_model()


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    User model w/o password
    """

    class Meta:
        model = User
        fields = "__all__"
        read_only_fields = ('email',)


class InterestsSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Interests
        fields = ('name',)


class ProductsSerialaer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class TarrifSerialazer(serializers.ModelSerializer):
    products = ProductsSerialaer(many=True, read_only=True)
    class Meta:
        model = Tariff
        fields = '__all__'


class ToolsSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class ResultSerialazer(serializers.ModelSerializer):
    tools = ToolsSerialazer(many=True)
    class Meta:
        model = Result
        exclude = ('users',)


class PostsSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class ProjectSerialazer(serializers.ModelSerializer):
    posts = PostsSerialazer(many=True, read_only=True)
    results = ResultSerialazer(many=True, read_only=True)
    class Meta:
        model = Project
        exclude = ('user',)


class UserSerialazer(serializers.ModelSerializer):
    interests = InterestsSerialazer(many=True, read_only=True)
    tariff = TarrifSerialazer(read_only=True)
    results = ResultSerialazer(many=True, read_only=True)
    projects = ProjectSerialazer(many=True, read_only=True)

    class Meta:
        model = User
        exclude = ('last_login', 'groups', 'is_staff', 'is_active', 'user_permissions', 'otp', 'password', 'is_superuser')
        read_only_fields = ('tg_id', 'tg_username', 'created', 'energy',)