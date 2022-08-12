from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import TaskViewSet, UserViewSet

router = SimpleRouter()

router.register('user', UserViewSet, basename='user')
router.register('task', TaskViewSet, basename='task')


urlpatterns = [
    path('v1/', include(router.urls)),
]
