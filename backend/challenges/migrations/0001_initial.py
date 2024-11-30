# Generated by Django 5.1.3 on 2024-11-30 19:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('hobbies', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Challenge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('reward', models.PositiveIntegerField()),
                ('progress', models.PositiveIntegerField(default=0)),
                ('target', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('successful', models.BooleanField(default=False)),
                ('expiration_date', models.DateTimeField()),
                ('hobby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to='hobbies.hobby')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='challenges', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
