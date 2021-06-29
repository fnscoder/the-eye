from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from events.models import Error, Event
from events.serializers import ErrorSerializer, EventSerializer


class EventModelViewSet(ModelViewSet):
    queryset = Event.objects.select_for_update().all()
    serializer_class = EventSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Event.objects.all()


class ErrorModelViewSet(ReadOnlyModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer
