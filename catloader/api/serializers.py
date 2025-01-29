from django_celery_beat.models import IntervalSchedule, PeriodicTask
from rest_framework import serializers


class IntervalScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'


class PeriodicTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeriodicTask
        fields = "__all__"
        read_only_fields = ('id', 'queue', 'routing_key', 'exchange', 'headers')

    def validate(self, attrs):
        headers_dict = {
            'name': attrs.get('name'),
            'task': attrs.get('task')
        }
        attrs['headers'] = headers_dict
        if not attrs['args']:
            attrs['args'] = []
        if not attrs['kwargs']:
            attrs['kwargs'] = {}
        return super().validate(attrs)
