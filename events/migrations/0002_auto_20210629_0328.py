# Generated by Django 3.2.4 on 2021-06-29 03:28

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='session_id',
        ),
        migrations.AddField(
            model_name='event',
            name='session',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='events', to='events.session', verbose_name='session'),
            preserve_default=False,
        ),
    ]
