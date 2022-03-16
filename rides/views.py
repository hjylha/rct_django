from django.shortcuts import render

from .models import Ride
from ridetypes.models import RideName
from .forms import RideAddForm
from .utils import calculate_all_max_prices, format_age_ranges, get_EIN, calculate_ride_value, price_as_string, price_color
from ridetypes.utils import is_valid_ridetype, get_EIN_values_by_ridename

# Create your views here.

#### VIEWS TO ADD RIDES
#
# raw html
# def ride_add_view(request, *args, **kwargs):
#     if request.method == 'POST':
#         print(f'POST-request: {request.POST}')
#         print(f'User: {request.user}, {type(request.user)}')
#         # ridename = RideName.objects.get(name=request.POST.get('ridename'))
#         keys = ['excitement_rating', 'intensity_rating', 'nausea_rating', 'model_name']
#         data = {key: request.POST.get(key)[0] for key in keys}
#         data['ridename'] = RideName.objects.get(name=request.POST.get('ridename'))
#         # data['user'] = request.user
#         data['ridetype'] = data['ridename'].ridetype
#         print(f'data to save: {data}')
#         Ride.objects.create(**data)
#     context = {}
#     return render(request, 'add_ride.html', context)

# django form
def ride_add_view(request, *args, **kwargs):
    form = RideAddForm(request.POST or None)
    if form.is_valid:
        # form.save()
        print(type(form))
        print('form is valid')
    context = {'form': form}
    return render(request, 'rides/add_ride.html', context)


#### VIEWS TO CALCULATE PRICES AND STUFF
# 
# 
def ride_name_html_input(ride_name: str = '') -> str:
    if ride_name:
        return f'''<tr>
                <td>Ride name</td>
                <td><input type="text" name="ridename" id="ridename_id" value="{ride_name}"/></td>
            </tr>'''
    return '''<tr>
                <td>Ride name</td>
                <td><input type="text" name="ridename"/></td>
            </tr>'''

def rating_html_input(rating_name: str, rating: int) -> str:
    rating_name_ = '_'.join(rating_name.split(' ')).lower()
    if rating:
        return f'''<tr>
                    <td>{rating_name}</td>
                    <td><input type="number" name="{rating_name_}" value="{rating/100}" step="0.01"/></td>
                </tr>'''
    return f'''<tr>
                <td>{rating_name}</td>
                <td><input type="number" name="{rating_name_}" step="0.01"/></td>
            </tr>'''

def ein_rating_html_input(ein_ratings: tuple[int, int, int]) -> str:
    e_input = rating_html_input('Excitement rating', ein_ratings[0])
    i_input = rating_html_input('Intensity rating', ein_ratings[1])
    n_input = rating_html_input('Nausea rating', ein_ratings[2])
    return '\n'.join([e_input, i_input, n_input])

def select_html(selection_text: str, selection_name: str, lines: tuple[str]) -> str:
    selection_id = f'{selection_name}_id'
    lines_together = '\n'.join(lines)
    return f'''<tr>
                <td>{selection_text}</td>
                <td>
                    <select id="{selection_id}" name="{selection_name}">
                        {lines_together}
                    </select>
                </td>
            </tr>'''

def entry_price_select_html(entry_price: str = 'free') -> str:
    text = 'Park Entrance Fee'
    name = 'free_entry'
    options = ['<option value="free">Free Entry</option>', '<option value="paid">Pay-for-Entry</option>']
    if entry_price == 'paid':
        return select_html(text, name, options[::-1])
    return select_html(text, name, options)

def version_select_html(version: str = 'openrct') -> str:
    text = 'Version of the game'
    name = 'version'
    options = ['<option value="openrct">OpenRCT2</option>', '<option value="classic">RCT Classic/RCT2 original</option>']
    if version == 'classic':
        return select_html(text, name, options[::-1])
    return select_html(text, name, options)

def ages_select_html(age_selection: str = 'All') -> str:
    text = 'Show ages under'
    name = 'ages'
    age_options = ['40', '88', '120', 'All']
    if age_selection:
        age_options.remove(age_selection)
        new_age_options = [age_selection] + age_options
    else:
        new_age_options = [age_options[-1]] + age_options[:3]
    options = [f'<option value="{age}">{age}</option>' for age in new_age_options]
    return select_html(text, name, options)


def show_price_row_html(price_line: dict) -> str:
    return f'''<tr>
            <td>
                {format_age_ranges(price_line['age_start'], price_line['age_end'])}
            </td>
            <td style="color: {price_color(price_line['unique_price'])}">
                {price_as_string(price_line['unique_price'])}
            </td>
            <td style="color: {price_color(price_line['price'])}">
                {price_as_string(price_line['price'])}
            </td>
        </tr>'''

def show_prices_html(prices: list[dict], max_age: int = 250) -> str:
    return '\n'.join([show_price_row_html(line) for line in prices if line['age_start'] < max_age])


def calculator_view(request, *args, **kwargs):
    ridenames = tuple(rn.name for rn in RideName.objects.all() if rn.is_visible)
    # set defaults
    context = {
        'ridenames': ridenames,
        'ride_name': '',
        # 'excitement_rating': 0,
        # 'intensity_rating': 0,
        # 'nausea_rating': 0,
        'ein_rating_inputs': ein_rating_html_input((0, 0, 0)),
        'free_entry': 'free',
        # 'version': 'openrct',
        # 'ages': 'All',
        'ride_value': 0,
        'ride_name_input': ride_name_html_input(),
        'entry_price_select_html': entry_price_select_html(),
        'version_select_html': version_select_html(),
        'age_select_html': ages_select_html(),
        'price_table_html': show_prices_html(calculate_all_max_prices((0, 0, 0), (0, 0, 0), True,))
        }
    f_entry = True
    # print(f'request: {request}')
    # print(*args)
    # print(**kwargs)
    if request.method == 'POST':
        # print(f'POST-request: {request.POST}')
        ride_name = request.POST.get('ridename')
        if ride_name and not is_valid_ridetype(ride_name):
            context['ride_name'] = None

        
        keys = ['excitement_rating', 'intensity_rating', 'nausea_rating']
        EIN_str = [request.POST.get(key) for key in keys]

        EIN = get_EIN(EIN_str)
        context['ein_rating_inputs'] = ein_rating_html_input(EIN)
        EIN_values = get_EIN_values_by_ridename(ride_name)
        # print(f'EIN ratings: {EIN}')
        # print(f'EIN multipliers: {EIN_values}')
        ride_value = calculate_ride_value(EIN_values, EIN)
        # if EIN_values is None:
        #     context['ride_name'] = ''
        # else:
        #     context['ride_name'] = ride_name
        # more_keys = ['free_entry', 'ride_value']
        # for key in more_keys:
        #     context[key] = request.POST.get(key)
        context['ride_value'] = ride_value
        # context['free_entry'] = request.POST.get('free_entry')
        # print(context['ride_name'])
        context['ride_name_input'] = ride_name_html_input(context['ride_name'])
        version = request.POST.get('version')
        context['version_select_html'] = version_select_html(version)
        ages = request.POST.get('ages')
        context['age_select_html'] = ages_select_html(ages)
        free_entry = request.POST.get('free_entry')
        context['entry_price_select_html'] = entry_price_select_html(free_entry)
        if free_entry != 'free':
            # context['free_entry'] = None
            f_entry = False
        in_og = True if version == 'classic' else False
        prices = calculate_all_max_prices(EIN, EIN_values, f_entry, True, in_og)
        try:
            max_age = int(ages)
        except ValueError:
            max_age = 250
        context['price_table_html'] = show_prices_html(prices, max_age)
        # print(context['ride_name'])
    if request.method == 'GET':
        # print(f'GET-request{request.GET}')
        ride_name = request.GET.get('ridename')
        
        keys = ['excitement_rating', 'intensity_rating', 'nausea_rating']
        EIN_str = [request.GET.get(key) for key in keys]

        EIN = get_EIN(EIN_str)
        context['ein_rating_inputs'] = ein_rating_html_input(EIN)
        EIN_values = get_EIN_values_by_ridename(ride_name)
        ride_value = calculate_ride_value(EIN_values, EIN)
        if EIN_values is None:
            context['ride_name'] = ''
        else:
            context['ride_name'] = ride_name
        context['ride_value'] = ride_value
        context['ride_name_input'] = ride_name_html_input(context['ride_name'])
        version = request.GET.get('version')
        context['version_select_html'] = version_select_html(version)
        ages = request.GET.get('ages')
        context['age_select_html'] = ages_select_html(ages)
        free_entry = request.GET.get('free_entry')
        context['entry_price_select_html'] = entry_price_select_html(free_entry)
        if free_entry != 'free':
            # context['free_entry'] = None
            f_entry = False
        in_og = True if version == 'classic' else False
        prices = calculate_all_max_prices(EIN, EIN_values, f_entry, True, in_og)
        try:
            max_age = int(ages)
        except ValueError:
            max_age = 250
        except TypeError:
            max_age = 250
        context['price_table_html'] = show_prices_html(prices, max_age)
    return render(request, 'rides/calculator.html', context)