from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import TaskViewSet, UserViewSet

router = SimpleRouter()

router.register('user', UserViewSet, 'user')
router.register('tasks', TaskViewSet, 'tasks')
router.register(r'^tasks/(?P<user_id>\d+)/detail_info/$', TaskViewSet, 'tasks-detail_info')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
