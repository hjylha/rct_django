
from django.db import models
from django.urls import reverse

# Create your models here.


class RideType(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # visible_name = models.CharField(max_length=64)
    ridebonusvalue = models.PositiveSmallIntegerField()
    excitement_value = models.PositiveSmallIntegerField()
    intensity_value = models.PositiveSmallIntegerField()
    nausea_value = models.SmallIntegerField()
    default_excitement = models.PositiveIntegerField(blank=True, null=True)
    default_intensity = models.PositiveIntegerField(blank=True, null=True)
    default_nausea = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name}: {self.excitement_value}/{self.intensity_value}/{self.nausea_value}, RBV: {self.ridebonusvalue}'

    def get_absolute_url(self):
        return reverse('ridetypes:ridetype-detail', kwargs={'name': self.name})


# class Alias(models.Model):
#     name = models.CharField(max_length=64)
#     og_ride_type = models.ForeignKey(RideType, on_delete=models.CASCADE)
#     excitement_modifier = models.IntegerField(null=True)
#     intensity_modifier = models.IntegerField(null=True)
#     nausea_modifier = models.IntegerField(null=True)
#     is_visible = models.BooleanField()

#     def __str__(self) -> str:
#         if self.is_visible:
#             return str(self.name)
#         return str(self.og_ride_type.visible_name)


class RideName(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_visible = models.BooleanField()
    ridetype = models.ForeignKey(RideType, on_delete=models.CASCADE)
    excitement_modifier = models.PositiveIntegerField(default=0)
    intensity_modifier = models.PositiveIntegerField(default=0)
    nausea_modifier = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        vis = 'visible' if self.is_visible else 'not visible'
        return f'{self.name}: {vis}'


# class BaseRide(models.Model):
#     ridetype = models.ForeignKey(RideType, on_delete=models.CASCADE)
#     names = models.ManyToManyField(RideName)
