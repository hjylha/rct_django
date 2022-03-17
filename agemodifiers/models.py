from enum import unique
from django.db import models

# Create your models here.


class AgeModifier(models.Model):
    in_og = models.BooleanField()
    age_start = models.PositiveSmallIntegerField()
    age_end = models.PositiveSmallIntegerField(null=True)
    multiplier = models.PositiveSmallIntegerField()
    divisor = models.PositiveSmallIntegerField()
    addition = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        version = 'Classic' if self.in_og else 'OpenRCT2'
        return f'{version}: {self.age_start} - {self.age_end}: {self.multiplier}/{self.divisor} + {self.addition}'
