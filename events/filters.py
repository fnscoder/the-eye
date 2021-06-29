from django_filters import rest_framework as filters

from events.models import Event


class EventFilterSet(filters.FilterSet):
    session = filters.UUIDFilter(field_name='session_id', lookup_expr='exact')

    class Meta:
        model = Event
        fields = {
            'category': ['exact'],
            'timestamp': ['lte', 'gte']
        }
