from django_celery_beat.models import IntervalSchedule
from rest_framework import serializers


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'