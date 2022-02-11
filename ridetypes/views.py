from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import RideType, RideName
from .utils import get_ridenames_for_ridetype

# Create your views here.


def ridetype_overview_view(request, *args, **kwargs):
    ridetypes = RideType.objects.all()
    ridedata = [(rt, get_ridenames_for_ridetype(rt)) for rt in ridetypes]
    # all_ridenames = tuple(get_ridenames_for_ridetype(rt) for rt in ridetypes)
    context = {
        'ridedata': ridedata
        # 'ridetypes': ridetypes,
        # 'all_ridenames': all_ridenames
        }
    return render(request, 'ridetypes/ridetype_overview.html', context)


def individual_ridetype_view(request, name, *args, **kwargs):
    ridetype = get_object_or_404(RideType, name=name)
    # more verbose way of doing this
    # try:
    #     ridetype = RideType.objects.get(name=name)
    # except RideType.DoesNotExist:
    #     raise Http404
    context = {'ridetype': ridetype}
    return render(request, 'ridetypes/ridetype_view.html', context)