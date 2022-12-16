# Generated by Django 4.1.3 on 2022-12-16 20:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import partners_club.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnersClub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(default='uploads/clubs/flying-club-default.png', upload_to=partners_club.models.picture_directory_path, verbose_name='Club picture')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('opn', 'Looking for a new partners'), ('cls', 'Closed')], default='cls', max_length=3)),
                ('members', models.ManyToManyField(related_name='members', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='club_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
