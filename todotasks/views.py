from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
)

from .models import Tag, Task
from .serializers import (
    TagListSerializer,
    TaskListSerializer,
    TagDetailSerializer,
    TaskDetailSerializer,
    TagCreateSerializer,
    TaskCreateSerializer,
    UserSerializer,
)


#
# class UserGet(APIView):
#     """"""
#     def get(self, request):
#         tags = User.objects.first()
#         serializer = UserSerializer(tags)
#         return Response(serializer.data, status=HTTP_200_OK)


class UserRegisterView(APIView):
    """Регистрация"""
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)

            user_serialized = UserSerializer(user)
            result = {**user_serialized.data, **{
                'token': token.key
            }}
            return Response(result, status=HTTP_201_CREATED)
        else:
            return Response('Failed to register, verify the entered data',
                            status=HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """Авторизация"""
    permission_classes = [AllowAny]

    def post(self, request):

        data = request.data
        try:
            username = data['username']
            password = data['password']
        except:
            return Response("Enter username and password", status=HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username, password=password)
        except:
            return Response("Invalid username or password entered", status=HTTP_400_BAD_REQUEST)

        token, _ = Token.objects.get_or_create(user=user)

        user_serialized = UserSerializer(user)
        result = {**user_serialized.data, **{
            'token': token.key
        }}

        return Response(result, status=HTTP_200_OK)


class TagCreateView(APIView):
    """Добавление тега"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_data = dict(request.data.lists())
        request_data_clear = {}
        for key in request_data:
            request_data_clear[key] = request_data[key][0]
        request_data_clear['user'] = request.user.id

        tag = TagCreateSerializer(data=request_data_clear)
        if tag.is_valid():
            # return Response(tag.data)
            tag.save()
            return Response(tag.data, status=HTTP_201_CREATED)
        else:
            return Response('Failed to create tag, verify the entered data',
                            status=HTTP_400_BAD_REQUEST)


class TaskCreateView(APIView):
    """Добавление тега"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_data = request.data
        request_data['user'] = request.user.id
        task = TaskCreateSerializer(data=request_data)
        if task.is_valid():
            task.save()
            return Response(task.data, status=HTTP_201_CREATED)
        else:
            return Response('Failed to create task, check the correctness of the entered data',
                            status=HTTP_400_BAD_REQUEST)


class TagListView(APIView):
    """Вывод списка всех тегов"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tags = Tag.objects.filter(user=request.user)
        if bool(tags) is False:
            return Response('Tags not found', status=HTTP_404_NOT_FOUND)
        serializer = TagListSerializer(tags, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TagDetailView(APIView):
    """Выыод деталей тега и всех задач с таким тегом"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            tag = Tag.objects.get(id=pk)
        except Tag.DoesNotExist:
            return Response('Tag not found', status=HTTP_404_NOT_FOUND)
        tag_serializer = TagDetailSerializer(tag, many=False)
        data = tag_serializer.data
        return Response(data, status=HTTP_200_OK)


class TasksListView(APIView):
    """Вывод списка всех задач"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        if bool(tasks) is False:
            return Response('Tasks not found', status=HTTP_404_NOT_FOUND)
        serializer = TaskListSerializer(tasks, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class TaskDetailView(APIView):
    """Вывод списка всех задач"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = Task.objects.get(id=pk, user=request.user)
        except Task.DoesNotExist:
            return Response('Task not found', status=HTTP_404_NOT_FOUND)
        serializer = TaskDetailSerializer(task, many=False)
        return Response(serializer.data, status=HTTP_200_OK)
