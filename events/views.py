from django_filters import rest_framework as filters
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from events.filters import EventFilterSet
from events.models import Error, Event, Session
from events.serializers import ErrorSerializer, EventSerializer, SessionSerializer
from events.tasks import create_event


class EventModelViewSet(ModelViewSet):
    queryset = Event.objects.select_for_update().all().order_by('-timestamp')
    serializer_class = EventSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = EventFilterSet

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            return Event.objects.all().order_by('-timestamp')

    def create(self, request, *args, **kwargs):
        create_event.delay(request.data)
        return Response('Event will be created after validation')


class ErrorModelViewSet(ReadOnlyModelViewSet):
    queryset = Error.objects.all()
    serializer_class = ErrorSerializer


class SessionModelViewSet(ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
