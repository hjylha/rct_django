from django.db import models
from django.contrib.auth.models import User

from ridetypes.models import RideType, RideName

# Create your models here.

class Ride(models.Model):
    ridetype = models.ForeignKey(RideType, on_delete=models.CASCADE)
    ridename = models.ForeignKey(RideName, on_delete=models.CASCADE)
    excitement_rating = models.PositiveIntegerField()
    intensity_rating = models.PositiveIntegerField()
    nausea_rating = models.PositiveIntegerField()
    # maybe the ride model has been saved, so its name might be useful
    model_name = models.CharField(max_length=64, blank=True, null=True)
    # user who submitted this ride and set of ratings
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f'{self.ridename}: {self.excitement_rating}/{self.intensity_rating}/{self.nausea_rating}'
