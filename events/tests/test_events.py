from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

from events.models import Event, Session
from events.views import EventModelViewSet


class EventModelViewSetTestCase(APITestCase):
    def setUp(self):
        session = Session.objects.create(id='e2085be5-9137-4e4e-80b5-f1ffddc25423')
        self.event = Event.objects.create(
            session=session,
            category='page interaction',
            name='pageview',
            data={
                "host": "www.consumeraffairs.com",
                "path": "/",
            },
            timestamp=timezone.now()
        )
        self.list_url = reverse('event-list')
        self.detail_url = reverse('event-detail', kwargs={'pk': self.event.pk})
        self.new_event_data = {
            'session': {"id": 'e2085be5-9137-4e4e-80b5-f1ffddc25423'},
            'category': 'page interaction',
            'name': 'cta click',
            'data': {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            'timestamp': timezone.now()
        }
        self.factory = APIRequestFactory()

    def test_create_event(self):
        request = self.factory.post(self.list_url, self.new_event_data, format='json')
        view = EventModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.new_event_data['name'])

    def test_create_event_without_session_id(self):
        data = {
            'category': 'page interaction',
            'name': 'cta click',
            'data': {
                "host": "www.consumeraffairs.com",
                "path": "/",
                "element": "chat bubble"
            },
            'timestamp': timezone.now()
        }
        request = self.factory.post(self.list_url, data, format='json')
        view = EventModelViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['session'][0], 'This field is required.')

    def test_list_events(self):
        request = self.factory.post(self.list_url, self.new_event_data, format='json')
        view = EventModelViewSet.as_view({'post': 'create'})
        response = view(request)

        request = self.factory.get(self.list_url)
        view = EventModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(Event.objects.all().count(), 2)

    def test_retrieve_event(self):
        request = self.factory.get(self.detail_url, format='json')
        view = EventModelViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=self.event.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.event.id)
        self.assertEqual(response.data['name'], self.event.name)

    def test_update_event(self):
        data = {'name': 'event new name'}
        request = self.factory.patch(self.detail_url, data, format='json')
        view = EventModelViewSet.as_view({'patch': 'partial_update'})
        response = view(request, pk=self.event.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.event.id)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_product(self):
        self.assertEqual(Event.objects.all().count(), 1)
        request = self.factory.delete(self.detail_url, format='json')
        view = EventModelViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=self.event.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Event.objects.all().count(), 0)
