# Generated by Django 3.1.7 on 2021-03-16 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='text',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('receive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receive', to=settings.AUTH_USER_MODEL)),
                ('send', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send', to=settings.AUTH_USER_MODEL)),
                ('targetplan', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='targetplan', to='api.plan')),
            ],
        ),
    ]