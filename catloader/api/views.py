from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework.viewsets import ModelViewSet

from api.serializers import IntervalScheduleSerializer, PeriodicTaskSerializer


class APIIntervalScheduleViewSet(ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    ordering_fields = '__all__'


class APIPeriodicTaskViewSet(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    ordering_fields = '__all__'


