from shutil import rmtree

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_201_CREATED,
                                   HTTP_204_NO_CONTENT)
from rest_framework.test import APITestCase

from api.models import Task, User


class GetTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='name', password='admin1989')
        Task.objects.create(
            user=user,
            task_title='test',
            task_description='test',
            task_completion='2022-09-01',
        )

    def test_get_task(self):
        response = self.client.get(reverse('tasks-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_user(self):
        response = self.client.get(reverse('users-list'))
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_get_detail_tasks(self):
        response = self.client.get(reverse('tasks-detail', args=[1]))
        self.assertEqual(response.status_code, HTTP_200_OK)


class DeleteTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='name', password='admin1989')
        Task.objects.create(
            user=user,
            task_title='test',
            task_description='test',
            task_completion='2022-09-01',
        )
        self.client.force_authenticate(user=user)

    def test_delete_task(self):
        response = self.client.delete(reverse('tasks-detail', args=[1]))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)

    def test_delete_user(self):
        response = self.client.delete(reverse('users-detail', args=[1]))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)


class PostTest(APITestCase):
    def setUp(self):
        user = User.objects.create(username='name', password='admin1989')

        Task.objects.create(
            user=user,
            task_title='test',
            task_description='test',
            task_completion='2022-09-01',
        )
        self.client.force_authenticate(user=user)

    @classmethod
    def tearDownClass(cls):
        rmtree(settings.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_post_task(self):
        task_count = Task.objects.count()
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
        task_data = {
            'task_title': 'post-test',
            'task_description': 'post-test',
            'task_completion': '2022-09-03',
            'file': uploaded,
        }
        response = self.client.post(reverse('tasks-list'), task_data)
        self.assertEqual(response.status_code, HTTP_201_CREATED)
        self.assertEqual(task_count + 1, Task.objects.count())


class PutPatchTest(APITestCase):
    def setUp(self):
        user = User.objects.create(
            username='test-user-name',
            password='admin1989',
            name='test-name',
        )
        Task.objects.create(
            user=user,
            task_title='test',
            task_description='test',
            task_completion='2022-09-01',
        )
        self.client.force_authenticate(user=user)
        self.data = {
            'task_title': 'put-path-test',
            'task_description': 'put-path-test',
            'task_completion': '2022-09-03',
        }
        self.data_user = {
            'username': 'put-test',
            'name': 'put-test',
        }

    def test_put_task(self):
        response = self.client.put(
            reverse('tasks-detail', args=[1]), self.data
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_patch_task(self):
        response = self.client.patch(
            reverse('tasks-detail', args=[1]), self.data
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_put_user(self):
        response = self.client.put(
            reverse('users-detail', args=[1]), self.data_user
        )
        self.assertEqual(response.status_code, HTTP_200_OK)

    def test_patch_user(self):
        response = self.client.patch(
            reverse('users-detail', args=[1]), self.data_user
        )
        self.assertEqual(response.status_code, HTTP_200_OK)
