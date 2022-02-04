'''Scripts to get ride data and age modifiers from OpenRCT2 source'''
from .utils import this_folder_path
from .utils import get_age_modifiers_from_file, get_ride_data_from_files, get_ride_names_from_file
from agemodifiers.models import AgeModifier
from ridetypes.models import RideType, RideName


def get_age_modifiers():
    age_mod = get_age_modifiers_from_file()
    start_age = 0
    for row in age_mod['new']:
        kwargs = {
            'in_og': False,
            'age_start': start_age,
            'age_end': row[0],
            'multiplier': row[1],
            'divisor': row[2],
            'addition': row[3]
        }
        AgeModifier.objects.create(**kwargs)
        start_age = row[0] if row[0] > start_age else None
    start_age = 0
    for row in age_mod['old']:
        kwargs = {
            'in_og': True,
            'age_start': start_age,
            'age_end': row[0],
            'multiplier': row[1],
            'divisor': row[2],
            'addition': row[3]
        }
        AgeModifier.objects.create(**kwargs)
        start_age = row[0] if row[0] > start_age else None


def get_ride_types():
    rides = get_ride_data_from_files()
    for ride, data in rides.items():
        kwargs = {
            'name': ride,
            'ridebonusvalue': data[1],
            'excitement_value': data[0][0],
            'intensity_value': data[0][1],
            'nausea_value': data[0][2]
        }
        RideType.objects.create(**kwargs)


def get_ride_names():
    ride_names = get_ride_names_from_file()
    for row in ride_names:
        ridetype = RideType.objects.get(name=row[2])
        kwargs = {
            'name': row[0],
            'is_visible': row[1],
            'ridetype': ridetype
        }
        if row[3]:
            kwargs['excitement_modifier'] = row[3]
        if row[4]:
            kwargs['intensity_modifier'] = row[4]
        if row[5]:
            kwargs['nausea_modifier'] = row[5]
        RideName.objects.create(**kwargs)
