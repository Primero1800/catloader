from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import APIIntervalScheduleViewSet, APIPeriodicTaskViewSet

app_name = 'api'

router = DefaultRouter()
router.register('intervals', APIIntervalScheduleViewSet)
router.register('ptasks', APIPeriodicTaskViewSet)

urlpatterns = [
    path(f'', include(router.urls)),
    path(f'', router.APIRootView.as_view(), name='root')
]