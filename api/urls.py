from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import TaskViewSet, UserViewSet

router = SimpleRouter()

router.register('user', UserViewSet, 'users')
router.register('tasks', TaskViewSet, 'tasks')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
