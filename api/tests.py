from shutil import rmtree
from typing import NamedTuple

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from rest_framework.test import APITestCase

from api.models import Task, User


class ReverseData(NamedTuple):
    list: str
    detail: str


class TestUserTask(APITestCase):
    def setUp(self):
        user = User.objects.create(username='name', password='admin1989')
        Task.objects.create(
            user=user,
            task_title='test',
            task_description='test',
            task_completion='2022-09-01',
        )
        self.client.force_authenticate(user=user)
        self.reverse_data = {
            'task': ReverseData(
                list=reverse('tasks-list'),
                detail=reverse('tasks-detail', args=[1]),
            ),
            'user': ReverseData(
                list=reverse('users-list'),
                detail=reverse('users-detail', args=[1]),
            ),
        }
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif',
        )
        self.data = {
            'task_title': 'put-path-test',
            'task_description': 'put-path-test',
            'task_completion': '2022-09-03',
            'file': uploaded,
        }
        self.data_user = {
            'username': 'put-test',
            'name': 'put-test',
        }

    @classmethod
    def tearDownClass(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_get(self):
        for url in self.reverse_data.values():
            with self.subTest(url=url.list):
                response = self.client.get(url.list).status_code
                self.assertEqual(response, HTTP_200_OK)

    def test_delete(self):
        for url in self.reverse_data.values():
            with self.subTest(url=url.detail):
                response = self.client.delete(url.detail).status_code
                self.assertEqual(response, HTTP_204_NO_CONTENT)

    def test_put_user(self):
        response = self.client.put(
            self.reverse_data['user'].detail, self.data_user
        ).status_code
        self.assertEqual(response, HTTP_200_OK)

    def test_put_task(self):
        response = self.client.put(
            self.reverse_data['task'].detail, self.data
        ).status_code
        self.assertEqual(response, HTTP_200_OK)

    def test_patch_user(self):
        response = self.client.patch(
            self.reverse_data['user'].detail, self.data_user
        ).status_code
        self.assertEqual(response, HTTP_200_OK)

    def test_patch_task(self):
        response = self.client.patch(
            self.reverse_data['task'].detail, self.data
        ).status_code
        self.assertEqual(response, HTTP_200_OK)

    def test_post_task(self):
        task_count = Task.objects.count()
        response = self.client.post(self.reverse_data['task'].list, self.data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(task_count + 1, Task.objects.count())
