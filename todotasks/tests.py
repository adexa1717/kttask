from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
)

from .models import Tag
from .serializers import TaskCreateSerializer


class TagTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='user1')
        user2 = User.objects.create_user(username='user2', password='user2')
        user3 = User.objects.create_user(username='user3', password='user3')

        user1.save()
        user2.save()
        user3.save()

        self.user1_token = Token.objects.create(user=user1)
        self.user2_token = Token.objects.create(user=user2)
        self.user3_token = Token.objects.create(user=user3)

        self.tag1 = Tag.objects.create(name='tag1', user=user1)
        self.tag2 = Tag.objects.create(name='tag2', user=user1)
        self.tag3 = Tag.objects.create(name='tag3', user=user2)

        self.data_tag = {
            'name': 'tag4'
        }

    def test_tag_auth_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_tag_list_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user3_token.key)
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_tag_list_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('tag-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_tag_detail_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('tag-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_tag_detail_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('tag-detail', kwargs={'pk': self.tag2.id}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'tag2')

    def test_tag_create_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user3_token.key)
        response = self.client.post(reverse('tag-create'), {})
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_tag_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user3_token.key)
        response = self.client.post(reverse('tag-create'), self.data_tag)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'tag4')


class TaskTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create_user(username='user1', password='user1')
        user2 = User.objects.create_user(username='user2', password='user2')
        user3 = User.objects.create_user(username='user3', password='user3')

        user1.save()
        user2.save()
        user3.save()

        self.user1_token = Token.objects.create(user=user1)
        self.user2_token = Token.objects.create(user=user2)
        self.user3_token = Token.objects.create(user=user3)

        tag1 = Tag.objects.create(name='tag1', user=user1)
        tag2 = Tag.objects.create(name='tag2', user=user1)
        tag3 = Tag.objects.create(name='tag3', user=user2)

        data_task1 = {
            "name": "task1",
            "description": "Some description",
            "tags": [tag1.id, tag2.id],
            "user": user1.id
        }
        data_task2 = {
            "name": "task2",
            "description": "Some description",
            "tags": [tag1.id],
            "user": user1.id
        }

        data_task3 = {
            "name": "task3",
            "description": "Some description",
            "tags": [tag3.id],
            "user": user2.id
        }

        self.task1 = TaskCreateSerializer(data=data_task1)
        if self.task1.is_valid():
            self.task1.save()
        self.task2 = TaskCreateSerializer(data=data_task2)
        if self.task2.is_valid():
            self.task2.save()
        self.task3 = TaskCreateSerializer(data=data_task3)
        if self.task3.is_valid():
            self.task3.save()

        self.data_task = {
            'name': 'task4',
            'description': 'some description',
            'tags': [tag3.id]
        }

    def test_task_auth_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)

    def test_task_list_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user3_token.key)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_task_list_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_task_detail_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('task-detail', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_task_detail_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.get(reverse('task-detail', kwargs={'pk': self.task2.data['id']}))
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['name'], 'task2')

    def test_task_create_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user3_token.key)
        response = self.client.post(reverse('task-create'), {}, format='json')
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def test_task_create_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user3_token.key)
        response = self.client.post(reverse('task-create'), self.data_task, format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'task4')
