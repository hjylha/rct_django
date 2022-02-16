
from .models import RideType, RideName

def get_ridetype(ride_name: str) -> RideType:
    try:
        ridename = RideName.objects.get(name=ride_name)
    except RideName.DoesNotExist:
        ridename = None
    if ridename:
        return ridename.ridetype
    return None


def is_valid_ridetype(ride_name: str) -> bool:
    if get_ridetype(ride_name):
        return True
    return False


def get_EIN_values(ridetype: RideType) -> tuple[int, int, int]:
    return (ridetype.excitement_value, ridetype.intensity_value, ridetype.nausea_value)


def get_EIN_values_by_ridename(ride_name: str) -> tuple[int, int, int]:
    ridetype = get_ridetype(ride_name)
    if ridetype:
        return get_EIN_values(ridetype)
    return None


def get_ridenames_for_ridetype(ridetype: RideType) -> tuple[RideName]:
    return tuple(rn for rn in RideName.objects.all() if rn.ridetype == ridetype)


def get_dict_of_ridetypes_and_ridenames() -> dict:
    everything = dict()
    ridenames = RideName.objects.all()
    for ridename in ridenames:
        if ridename.ridetype.name in everything:
            everything[ridename.ridetype.name][1].append(ridename)
        else:
            everything[ridename.ridetype.name] = [ridename.ridetype, [ridename]]
    return everything

