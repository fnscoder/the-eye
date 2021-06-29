from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from events.models import Error, Event
from events.serializers import ErrorSerializer, EventSerializer


class EventModelViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class ErrorModelViewSet(ReadOnlyModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer
