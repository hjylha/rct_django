from django.shortcuts import render

from .models import Ride
from ridetypes.models import RideName
from .forms import RideAddForm
from .utils import get_EIN, calculate_ride_value
from ridetypes.utils import get_EIN_values_by_ridename

# Create your views here.

# raw html
def ride_add_view(request, *args, **kwargs):
    if request.method == 'POST':
        print(f'POST-request: {request.POST}')
        print(f'User: {request.user}, {type(request.user)}')
        # ridename = RideName.objects.get(name=request.POST.get('ridename'))
        keys = ['excitement_rating', 'intensity_rating', 'nausea_rating', 'model_name']
        data = {key: request.POST.get(key)[0] for key in keys}
        data['ridename'] = RideName.objects.get(name=request.POST.get('ridename'))
        data['user'] = request.user
        data['ridetype'] = data['ridename'].ridetype
        print(f'data to save: {data}')
        Ride.objects.create(**data)
    context = {}
    return render(request, 'add_ride.html', context)

# django form
# def ride_add_view(request, *args, **kwargs):
#     form = RideAddForm(request.POST or None)
#     if form.is_valid:
#         # form.save()
#         # print(form)
#         print('form is valid')
#     context = {'form': form}
#     return render(request, 'add_ride.html', context)


def calculator_view(request, *args, **kwargs):
    context = {'ride_name': '', 'ride_value': 0}
    if request.method == 'POST':
        # print(f'POST-request: {request.POST}')
        ride_name = request.POST.get('ridename')
        # print(f'Ride name: {ride_name}, type: {type(ride_name)}')
        keys = ['excitement_rating', 'intensity_rating', 'nausea_rating']
        EIN_str = [int(request.POST.get(key)[0]) for key in keys]
        EIN = get_EIN(EIN_str)
        EIN_values = get_EIN_values_by_ridename(ride_name)
        # print(f'EIN ratings: {EIN}')
        ride_value = calculate_ride_value(EIN_values, EIN)
        if EIN_values is None:
            context['ride_name'] = None
        context['ride_value'] = ride_value
    return render(request, 'calculator.html', context)