from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import TaskViewSet, UserViewSet, profile, login_view

router = SimpleRouter()

router.register('user', UserViewSet, basename='user')
router.register('task', TaskViewSet, basename='task')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/profile/', profile, name='signup'),
    path('v1/login/', login_view, name='signup'),
]
