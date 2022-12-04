from django.db import models
from django.contrib.auth.models import AbstractUser
from .usa_states import get_states_choices


def photo_directory_path(instance, filename):
    return f'uploads/users/{instance.pk // 100}/{instance.pk}/{filename}'


class User(AbstractUser):
    state = models.CharField(max_length=2, choices=get_states_choices(), default='None')
    phone_number = models.CharField(max_length=15, null=True)
    EVERYONE = 'evr'
    NOBODY = 'nbd'
    PARTNERS = 'prt'
    PHONE_STATUSES = (
        (EVERYONE, 'everyone'),
        (NOBODY, 'nobody'),
        (PARTNERS, 'parterns'),
    )
    profile_status = models.CharField(max_length=3, choices=PHONE_STATUSES, default=NOBODY)
    photo = models.ImageField(upload_to=photo_directory_path,
                              verbose_name='User Photo',
                              default='uploads/users/default.png')

    # def get_absolute_url(self):
    #     return reverse('profile', kwargs={'pk':self.pk})

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

# class PilotProfile(models.Model):
#     user =
#     license =
#     date
