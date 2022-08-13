from django.contrib.auth.tokens import default_token_generator
from rest_framework import serializers, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Task, User
from api.serializers import TaskSerializer, UserSerializer
from big_data_test import settings


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


from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import ensure_csrf_cookie
from .serializers import UserSerializer
from .utils import generate_access_token, generate_refresh_token


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    # User = settings.AUTH_USER_MODEL
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')
    user = User.objects.filter(username=username).first()
    if(user is None):
        raise exceptions.AuthenticationFailed('user not found')
    if (not user.check_password(password)):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = UserSerializer(user).data
    print(user)
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }

    return response

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def signup(request):
#     serializer = SignupSerializer(data=request.data)
#     if serializer.is_valid():
#         password = serializer.validated_data['password']
#         user = serializer.save(password=password)
#         password = default_token_generator.make_token(user)
#         return Response({'token': f'{password}'}, status=status.HTTP_200_OK)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def profile(request):
    user = request.user
    serialized_user = UserSerializer(user).data
    return Response({'user': serialized_user })