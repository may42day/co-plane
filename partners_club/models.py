from django.db import models
from user.models import User


def picture_directory_path(instance, filename):
    return f'uploads/clubs/{instance.pk // 100}/{instance.pk}/{filename}'


class PartnersClub(models.Model):
    """Group for several members"""
    club_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User,
                              related_name='club_owner',
                              on_delete=models.PROTECT)
    members = models.ManyToManyField(User, related_name='members')
    description = models.TextField(null=True, blank=True)
    picture = models.ImageField(upload_to=picture_directory_path,
                                verbose_name='Club picture',
                                default='uploads/clubs/flying-club-default.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    OPEN = 'opn'
    CLOSED = 'cls'
    CLUB_STATUSES = (
        (OPEN, 'Looking for a new partners'),
        (CLOSED, 'Closed'),
    )
    status = models.CharField(max_length=3,
                              choices=CLUB_STATUSES,
                              default=CLOSED)
