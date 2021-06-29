from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from events.models import Event, Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id',)


class EventSerializer(WritableNestedModelSerializer):
    session = SessionSerializer()

    class Meta:
        model = Event
        fields = ('id', 'session', 'category', 'name', 'data', 'timestamp')
