# Generated by Django 2.0.1 on 2018-01-14 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_remove_emotion_event'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emotion',
            name='id',
        ),
        migrations.AddField(
            model_name='emotion',
            name='event',
            field=models.OneToOneField(default=123, on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.Event'),
            preserve_default=False,
        ),
    ]