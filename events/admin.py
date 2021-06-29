from django.contrib import admin

from events.models import Event, Session

admin.site.register(Event)
admin.site.register(Session)
