from rest_framework import serializers

from .models import Project, Post
from apps.core.models import Result, Tool


class PostSerialazer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Post
        fields = "__all__"


class ToolsSerialazer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = '__all__'


class ResultSerialazer(serializers.ModelSerializer):
    tools = ToolsSerialazer(many=True, read_only=True)
    class Meta:
        model = Result
        exclude = ('users',)

class ProjectSerialazer(serializers.ModelSerializer):
    # posts = PostSerialazer(many=True, read_only=True)
    # results = ResultSerialazer(many=True, read_only=True)
    posts = serializers.PrimaryKeyRelatedField(many=True, queryset=Post.objects.all(), required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    results = serializers.PrimaryKeyRelatedField(many=True, queryset=Result.objects.all(), required=False)
    class Meta:
        model = Project
        fields = '__all__'