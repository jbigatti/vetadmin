"""Define models here in alphabetic order."""

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

DEFAULT_MAX_LENGTH = 256


def user_uploads(instance, filename):
    """Files uploads for users"""
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def vet_uploads(instance, filename):
    """Files for index and stuff."""
    return 'vet/{0}'.format(filename)


class CarouselSlide(models.Model):
    """A slide for the Carousel of index."""

    MAX_CAROUSEL_SLIDES = 3

    COLOR_CHOICES = (
        ('black', 'Black'),
        ('white', 'White'),
    )

    title = models.CharField(blank=True, max_length=25)
    text = models.TextField(blank=True)
    text_color = models.CharField(choices=COLOR_CHOICES, default='white', max_length=5)
    image = models.ImageField(
        upload_to=vet_uploads, max_length=100)

    @property
    def has_extra_data(self):
        """True if has text or title."""
        return bool(self.title or self.text_color)

    def clean(self, *args, **kwargs):
        if self.pk or CarouselSlide.objects.count() < self.MAX_CAROUSEL_SLIDES:
            super().clean(*args, **kwargs)
        elif CarouselSlide.objects.count() >= self.MAX_CAROUSEL_SLIDES:
            msg = 'Cannot have more than {0} slides.'.format(self.MAX_CAROUSEL_SLIDES)
            raise ValidationError(msg)


class MedicalRecord(models.Model):
    """The history of a pet."""

    # TODO LIST:
    # Add attachment files, so they can attach studies
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()


class Patient(models.Model):
    """Is a pet."""

    # TODO LIST:
    # - Remove null=True if applicable
    SEX_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'))

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='pets', on_delete=models.CASCADE)
    name = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    date_of_birth = models.DateField(null=True)
    date_of_dead = models.DateField(null=True)
    # To Fill from Species model
    species = models.CharField(max_length=DEFAULT_MAX_LENGTH, null=True)
    # To Fill from Race model
    race = models.CharField(max_length=DEFAULT_MAX_LENGTH, null=True)
    sex = models.CharField(max_length=15, choices=SEX_CHOICES, default='male')
    miscellaneous = models.TextField(null=True)


class UserProfile(models.Model):
    """Is a vet or a customer."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    is_vet = models.BooleanField(default=False)

    city = models.CharField(null=True, max_length=DEFAULT_MAX_LENGTH)
    address = models.CharField(null=True, max_length=DEFAULT_MAX_LENGTH)
    date_of_birth = models.DateField(null=True)
    fix_phone = models.CharField(null=True, max_length=15)
    cell_phone = models.CharField(null=True, max_length=15)


class VaccinationRecord(models.Model):
    """The vaccination record of a pet."""

    # TODO LIST:
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    vaccinate_date = models.DateField(null=True)
    next_vaccinate = models.DateField()
    # To fill from vaccine kinds
    vaccine = models.CharField(max_length=DEFAULT_MAX_LENGTH)
    vaccine_data = models.CharField(max_length=DEFAULT_MAX_LENGTH)
