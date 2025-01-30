from django_celery_beat.models import IntervalSchedule, PeriodicTask
from django_celery_results.models import TaskResult
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import IntervalScheduleSerializer, PeriodicTaskSerializer, TaskResultSerializer


class APIIntervalScheduleViewSet(ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    ordering_fields = '__all__'


class APIPeriodicTaskViewSet(ModelViewSet):
    queryset = PeriodicTask.objects.all()
    serializer_class = PeriodicTaskSerializer
    ordering_fields = '__all__'


class APITaskResultViewSet(ReadOnlyModelViewSet):
    queryset = TaskResult.objects.all()
    serializer_class = TaskResultSerializer
    ordering_fields = '__all__'


