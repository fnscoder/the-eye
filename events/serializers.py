from django.utils import timezone
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from events.models import Event, Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id',)


class EventSerializer(WritableNestedModelSerializer):
    session = SessionSerializer()

    def validate_data(self, data):
        if not data:
            raise serializers.ValidationError('The data can\' be empty.')
        elif not type(data) == dict:
            raise serializers.ValidationError('The data content must a JSON format.')
        return data

    def validate_timestamp(self, timestamp):
        if timestamp > timezone.now():
            raise serializers.ValidationError('The timestamp can\'t be greater than now.')
        return timestamp

    class Meta:
        model = Event
        fields = ('id', 'session', 'category', 'name', 'data', 'timestamp')
