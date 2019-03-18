from django.db import models
import re

# Create your models here.

class Dog(models.Model):
    SELECTION_LEVELS = (
        ('HIG', 'High'),
        ('MED', 'Medium'),
        ('LOW', 'Low'),
    )
    COAT_LEVELS = (
        ('SHO', 'Short'),
        ('MED', 'Medium'),
        ('LON', 'Long'),
    )
    SIZE_LEVELS = (
        ('GIA', 'Giant'),
        ('LAR', 'Large'),
        ('MED', 'Medium'),
        ('SMA', 'Small'),
        ('MIN', 'Miniature'),
    )

    breed_name = models.CharField(max_length=50, default='Doge')
    activity_level = models.CharField(
        max_length=3,
        choices=SELECTION_LEVELS,
        default='LOW',
    )
    coat_length = models.CharField(
        max_length=3,
        choices=SELECTION_LEVELS,
        default='LOW',
    )
    drools = models.BooleanField(default=True)
    goodChildren = models.BooleanField(default=True)
    grooming = models.CharField(
        max_length=3,
        choices=SELECTION_LEVELS,
        default='LOW',
    )
    intelligence = models.CharField(
        max_length=3,
        choices=SELECTION_LEVELS,
        default='LOW',
    )
    shedding = models.CharField(
        max_length=3,
        choices=SELECTION_LEVELS,
        default='LOW',
    )
    size = models.CharField(
        max_length=3,
        choices=SIZE_LEVELS,
        default='MED',
    )
    img_path = models.CharField(max_length=50, default='none.jpg')

    def __str__(self):
        return self.breed_name

