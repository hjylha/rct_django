from pyexpat import model
from django import forms

from .models import Ride


class RideAddForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['ridename', 'excitement_rating', 'intensity_rating', 'nausea_rating', 'model_name']