from django_celery_beat.models import IntervalSchedule
from rest_framework.viewsets import ModelViewSet

from api.serializers import IntervalScheduleSerializer


class APIIntervalScheduleViewSet(ModelViewSet):
    queryset = IntervalSchedule.objects.all()
    serializer_class = IntervalScheduleSerializer
    ordering_fields = '__all__'


