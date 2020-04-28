from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Tag, Task


class TagListSerializer(serializers.ModelSerializer):
    """Список тегов"""

    class Meta:
        model = Tag
        fields = ('id', 'name',)


class TaskListSerializer(serializers.ModelSerializer):
    """Список задач"""

    class Meta:
        model = Task
        fields = ('id', 'name',)


class TagDetailSerializer(serializers.ModelSerializer):
    """Детали тега с задачами относящимися к данному тегу"""
    tasks = TaskListSerializer(many=True)

    class Meta:
        model = Tag
        exclude = ('user',)


class TaskDetailSerializer(serializers.ModelSerializer):
    """Детали задачи с тегами"""
    tags = TagListSerializer(many=True)

    class Meta:
        model = Task
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = User
        fields = ('id', 'username', 'password')


class TagCreateSerializer(serializers.ModelSerializer):
    """"""
    # user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Tag
        fields = ('name', 'user')
        # exclude = ('created_at', 'updated_at')
        # extra_kwargs = {
        #     'user': {'read_only': True},
        #     'user': {'default': serializers.CurrentUserDefault()},
        # }


class TaskCreateSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = Task
        exclude = ('created_at', 'updated_at')
