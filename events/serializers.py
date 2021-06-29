from django.utils import timezone
from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from events.models import Event, Session, Error


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id',)


class EventSerializer(WritableNestedModelSerializer):
    session = SessionSerializer()

    def validate_data(self, data):
        if not data:
            message = 'The data can\' be empty.'
            Error.objects.create(message=message)
            raise serializers.ValidationError(message)
        elif not type(data) == dict:
            message = 'The data content must a JSON format.'
            Error.objects.create(message=message, data=data)
            raise serializers.ValidationError('The data content must a JSON format.')
        return data

    def validate_timestamp(self, timestamp):
        if timestamp > timezone.now():
            message = 'The timestamp can\'t be greater than now.'
            Error.objects.create(message=message, data=self.initial_data.get('data'))
            raise serializers.ValidationError(message)
        return timestamp

    class Meta:
        model = Event
        fields = ('id', 'session', 'category', 'name', 'data', 'timestamp')


class ErrorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Error
        fields = '__all__'
