from django.urls import path, include
from rest_framework.routers import SimpleRouter

from events.views import EventModelViewSet

router = SimpleRouter()

router.register('events', EventModelViewSet, 'event')

urlpatterns = [
    path('', include(router.urls)),
]
