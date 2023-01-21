from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Task, User
from api.permissions import OwnerOrReadOnly
from api.serializers import UserSerializer, TaskSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (OwnerOrReadOnly,)
    http_method_names = ('get', 'put', 'patch', 'delete')
    pagination_class = LimitOffsetPagination


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.select_related('user').all()
    serializer_class = TaskSerializer
    permission_classes = (OwnerOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        """
        Метод не позволяет неавторизованным пользователям
        использовать метод POST.
        """
        if request.user.is_anonymous:
            raise serializers.ValidationError(
                'Метод POST не разрешен для неавторизованного пользователя.'
            )
        return super().create(request)

    @action(detail=True, methods=['get'])
    def detail_info(self, request, pk=None):
        """Метод выводит список задач пользователя по id."""
        queryset = Task.objects.filter(user_id=pk).all()
        if not queryset:
            raise serializers.ValidationError(
                'Такого пользователя не существует или у него нет задач.'
            )
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)
