from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Task, User
from api.serializers import TaskSerializer, UserSerializer, SignupSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @action(detail=True, methods=['get'])
    def detail_info(self, request, pk=None):
        queryset = Task.objects.filter(user_id=pk).all()
        if not queryset:
            raise serializers.ValidationError(
                'Такого пользователя не существует или у него нет задач.'
            )
        serializer = TaskSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        password = serializer.validated_data['password']
        user = serializer.save(password=password)
        password = default_token_generator.make_token(user)
        return Response({'token': f'{password}'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
