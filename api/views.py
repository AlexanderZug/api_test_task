
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Task, User
from api.permissions import OwnerOrReadOnlyTask, OwnerOrReadOnlyUser
from api.serializers import TaskSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOrReadOnlyUser,)
    http_method_names = ['head', 'get', 'put', 'patch', 'delete']
    pagination_class = LimitOffsetPagination


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related('user').all()
    serializer_class = TaskSerializer
    permission_classes = (OwnerOrReadOnlyTask,)
    pagination_class = LimitOffsetPagination

    @action(detail=True, methods=['get'])
    def detail_info(self, request, pk=None):
        queryset = Task.objects.filter(user_id=pk).all()
        if not queryset:
            raise serializers.ValidationError(
                'Такого пользователя не существует или у него нет задач.'
            )
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
