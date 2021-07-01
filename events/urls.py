from django.urls import path, include
from rest_framework.routers import SimpleRouter

from events.views import ErrorModelViewSet, EventModelViewSet, SessionModelViewSet

router = SimpleRouter()

router.register('events', EventModelViewSet, 'event')
router.register('errors', ErrorModelViewSet, 'error')

urlpatterns = [
    path('', include(router.urls)),
    path('sessions/', SessionModelViewSet.as_view(), name='session')
]
