from django.urls import path, include
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
#router.register('ads', APIPeriodicSettingViewSet)

urlpatterns = [
    path(f'', include(router.urls)),
    path(f'', router.APIRootView.as_view(), name='root')
]