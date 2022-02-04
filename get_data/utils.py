from pathlib import Path

import requests

'''functions to get ride values and age modifiers from openrct2 source'''
this_folder_path = Path(__file__).parent
# openrct2_path = Path('C:\\Ohjelmointiprojekteja\\c++projects\\OpenRCT2')
openrct2_path = this_folder_path.parent.parent.parent / 'c++projects' / 'OpenRCT2'

openrct2_url = 'https://raw.githubusercontent.com/OpenRCT2/OpenRCT2/develop/src/openrct2/'

# get data
# from openRCT2 source
# ..\OpenRCT2\src\openrct2\ride
# ride data
# subfolders with .h files:
# coaster\meta
# gentle\meta
# shops\meta   (probably not needed)
# thrill\meta
# transport\meta
# water\meta
# in files RideName.h:
# EIN multipliers:
# SET_FIELD(RatingsMultipliers, { 48, 28, 7 }),
# RideBonusValue:
# SET_FIELD(BonusValue, 65),

# age modifiers:
# RideRatings.cpp
# static const row ageTableNew[] = {
# };
# static const row ageTableOld[] = {
# };

# get ratings multipliers from a line of text, if they are there
def get_ratings_multipliers(line_of_text : str) -> tuple:
    if 'RatingsMultipliers' in line_of_text:
        numbers = '1234567890'
        start_index = None
        for i, char in enumerate(line_of_text):
            if char in numbers:
                if start_index is None:
                    start_index = i
                end_index = i
        EIN = line_of_text[start_index:end_index + 1].split(',')
        for i, value in enumerate(EIN):
            EIN[i] = int(value.strip())
        return tuple(EIN)
    return None

# get bonusvalue of a ride from a line of text, if it is there
def get_rides_bonusvalue(line_of_text : str) -> int:
    if 'BonusValue' in line_of_text:
        numbers = '1234567890'
        start_index = None
        for i, char in enumerate(line_of_text):
            if char in numbers:
                if start_index is None:
                    start_index = i
                end_index = i
        return int(line_of_text[start_index:end_index+1])
    return None

# get ratings modifiers and bonusvalue from file
def get_ride_data_from_file(file):
    EIN, bonusvalue = None, None
    for line in file:
        if EIN is None:
            EIN = get_ratings_multipliers(line)
        if bonusvalue is None:
            bonusvalue = get_rides_bonusvalue(line)
        if EIN is not None and bonusvalue is not None:
            return (EIN, bonusvalue)

# changing AirPoweredVerticalCoaster into Air Powered Vertical Coaster
def add_spaces_to_ride_names(ride_wo_spaces : str) -> str:
    ride_name = ride_wo_spaces
    i = 1
    while True:
        try:
            char, char_next = ride_name[i], ride_name[i + 1]
            if char.isupper() and char_next.islower():
                ride_name = ride_name[:i] + ' ' + ride_name[i:]
                i += 1
            i += 1
        except IndexError:
            return ride_name

# get EIN modifiers and bonusvalue for all rides with files (except shops)
def get_ride_data_from_files():
    rides = dict()
    # ..\OpenRCT2\src\openrct2\ride
    ride_path = openrct2_path / 'src' / 'openrct2' / 'ride'
    ride_url = f'{openrct2_url}ride'
    # skip 'shops' folder for now
    folders = ['coaster', 'gentle', 'thrill', 'transport', 'water']
    for folder in folders:
        curr_path = ride_path / folder / 'meta'
        curr_url = f'{ride_url}/{folder}/meta'
        # get data from ride_name.h files
        files = curr_path.glob('*.h')
        for file in files:
            # print(file)
            # ride_name = add_spaces_to_ride_names(file.stem)
            # with open(file) as f:
                # ride_data = get_ride_data_from_file(f)
            # ride_name = file.stem
            file_url = f'{curr_url}/{file.name}'
            req = requests.get(file_url)
            ride_data = get_ride_data_from_file(req.text.split('\n'))
            rides[file.stem] = ride_data
            print(f'Found {file.stem}: {ride_data}')
    return rides

# get age modifiers from line
def get_age_modifiers_from_line(line : str) -> tuple:
    values0 = line.split('}')[0].split('{')[1].split(',')
    return tuple([int(value.strip()) for value in values0])

# get age modifiers from a file
# static const row ageTableNew[] = {
# };
# static const row ageTableOld[] = {
# };
def get_age_table(file_lines) -> dict:
    reading, new_table_done = False, False
    new_table = []
    old_table = []
    for line in file_lines:
        if reading:
            if '};' in line:
                reading = False
                if new_table_done:
                    break
                else:
                    new_table_done = True
            else:
                if new_table_done:
                    old_table.append(get_age_modifiers_from_line(line))
                else:
                    new_table.append(get_age_modifiers_from_line(line))
        else:
            if 'ageTableNew[]' in line:
                reading = True
            elif 'ageTableOld[]' in line:
                reading = True
    return {'new': new_table, 'old': old_table}

# get age modifiers from RideRatings.cpp
def get_age_modifiers_from_file() -> dict:
    # file_path = openrct2_path / 'src' / 'openrct2' / 'ride' / 'RideRatings.cpp'
    # with open(file_path, 'r') as f:
    #     return get_age_table(f)
    file_path = f'{openrct2_url}ride/RideRatings.cpp'
    file = requests.get(file_path)
    file_lines = file.text.split('\n')
    return get_age_table(file_lines)


# name,1/0,og_name,str(e),str(i),str(n)\n -> (name, True/False, og_name, e, i, n)
def read_ride_name_line(line: str) -> tuple:
    items = line.strip().split(',')
    # name is easy
    row = [items[0]]
    # visibility needs a check
    next = True if items[1] == '1' else False
    row.append(next)
    # ridetype name is easy
    row.append(items[2])
    # modifiers
    for mod in items[3:]:
        if mod:
            row.append(int(mod))
        else:
            row.append(None)
    return tuple(row)


def get_ride_names_from_file():
    ride_names = []
    with open(this_folder_path / 'data/ride_names.csv', 'r') as f:
        for line in f:
            ride_names.append(read_ride_name_line(line))
    return ride_names