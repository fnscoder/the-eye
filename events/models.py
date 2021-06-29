import uuid

from django.db import models


class Event(models.Model):
    session = models.ForeignKey(
        'events.Session',
        verbose_name='session',
        related_name='events',
        on_delete=models.CASCADE
    )
    category = models.CharField('category', max_length=50)
    name = models.CharField('name', max_length=150)
    data = models.JSONField('payload data')
    timestamp = models.DateTimeField('event datetime', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'


class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField('created at', auto_now_add=True)
