from django.db import models


class Event(models.Model):
    session_id = models.UUIDField('session id')
    category = models.CharField('category', max_length=50)
    name = models.CharField('name', max_length=150)
    data = models.JSONField('payload data')
    timestamp = models.DateTimeField('event datetime', auto_now_add=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'event'
        verbose_name_plural = 'events'
