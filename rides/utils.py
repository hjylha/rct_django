
from agemodifiers.models import AgeModifier
from agemodifiers.utils import get_sorted_age_modifiers


# check the given ein ratings
def get_EIN(ein_input: tuple[str, str, str]) -> tuple[int, int, int]:
    EIN = []
    for item in ein_input:
        try:
            rating = int(100 * float(item))
        except ValueError:
            # for now ignore the error and set rating to 0
            rating = 0
        except TypeError:
            rating = 0
        EIN.append(rating)
    return tuple(EIN)


# CALCULATING PRICES
#
# EIN multipliers as 3-tuple, EIN as 3-tuple (of integers)
def calculate_ride_value(EIN_multipliers: tuple, EIN: tuple) -> int:
    ride_value = 0
    if EIN_multipliers and EIN:
        for ein, ein_m in zip(EIN, EIN_multipliers):
            ride_value += (ein * ein_m) // 1024
    return ride_value


# apply age modifiers to ride value
def apply_age_to_ride_value(ride_value: int, age_modifier: AgeModifier) -> int:
    multiplier = age_modifier.multiplier
    divisor = age_modifier.divisor
    add = age_modifier.addition
    return (ride_value * multiplier) // divisor + add


# if there are many rides of the same type, value drops to 3/4
def apply_many_rides_modifier(modified_value: int) -> int:
    return modified_value - modified_value // 4


# if guests have to pay for entering the park value drops to 1/4
def apply_pay_for_entry(modified_value: int) -> int:
    return modified_value // 4


# maximal price is 2*modified_value/10, or maybe that's the first unacceptable price?
def maximize_price(modified_value: int, w_restriction: bool = True) -> int:
    # price in cents or whatever (so we are dealing with integers)
    # max_price = 2 * modified_value * 10
    value = min(2000, 20 * modified_value) if w_restriction else 20 * \
        modified_value
    return value


# calculate max prices in cases of unique ride and many similar rides
def calc_max_prices(EIN: tuple, EIN_multipliers: tuple, age_modifier: AgeModifier, free_entry: bool, w_restriction: bool = True) -> tuple:
    ride_value = calculate_ride_value(EIN_multipliers, EIN)
    # print(ride_value)
    modified_value = apply_age_to_ride_value(ride_value, age_modifier)
    # print(modified_value)
    if not free_entry:
        modified_value = apply_pay_for_entry(modified_value)
    modified_value_nonunique = apply_many_rides_modifier(modified_value)
    return (maximize_price(modified_value, w_restriction), maximize_price(modified_value_nonunique, w_restriction))


def calculate_all_max_prices(EIN: tuple[int, int, int], EIN_multipliers: tuple[int, int, int], free_entry: bool, w_restriction: bool = True, in_og: bool = False) -> list[dict]:
    prices = []
    for age_modifier in get_sorted_age_modifiers(in_og):
        price_u, price = calc_max_prices(
            EIN, EIN_multipliers, age_modifier, free_entry, w_restriction)
        price_info = {'age_start': age_modifier.age_start,
                      'age_end': age_modifier.age_end,
                      'unique_price': price_u,
                      'price': price}
        prices.append(price_info)
    return prices


# FORMATTING PRICE TABLE
#
# if len(word) < num_of_letters, add two spaces for each 'missing' letter
def add_double_spaces(word: str, num_of_letters: int) -> str:
    # if len(word) >= num_of_letters:
    #     return word
    formatted_word = word
    for _ in range(num_of_letters - len(word)):
        formatted_word += '  '
    return formatted_word


# how to show age1 - age2 as a string
def format_age_ranges(age1: int, age2: int) -> str:
    text1 = add_double_spaces(str(age1), 3)
    text2 = add_double_spaces(str(age2), 3)
    return f'{text1}  ...  {text2}'


# divide by 100 and add spaces
def price_as_string(price: int) -> str:
    price_s = str(price)
    if price == 0:
        return '  0.00'
    if price < 100:
        return f'  0.{price_s}'
    if price < 1000:
        return f'  {price_s[0]}.{price_s[1:]}'
    return f'{price_s[:2]}.{price_s[2:]}'


# the better the price, the greener the price
# but mostly just kinda random color decisions
def price_color_01(price: int) -> tuple:
    # zero price is red
    if price == 0:
        return (1, 0, 0, 1)
    # turn price to a number between 0 and 100
    mult = price // 20
    # high prices are green
    if mult > 49:
        mult = (mult - 50) // 2
        return (0, 0.75 + 0.01*mult, 0, 1)
    # less green, maybe blue
    if mult > 19:
        return (0, 0.4 + 0.01*mult, 0.8 - 0.01*mult, 1)
    # adding some red perhaps
    if mult > 4:
        return (0.4 - 0.01*mult, 0.02 * mult, 0.8 - 0.01*mult, 1)
    # more red for prices under 1 euro/dollar/etc
    mult *= 2
    return (0.9 - 0.05*mult, 0, 0.4 + 0.05 * mult, 1)


def color_as_rgb256(color_tuple: tuple[float]) -> str:
    colors = [str(int(color * 255)) for color in color_tuple[:3]]
    return f'rgb({", ".join(colors)})'


def price_color(price: int) -> str:
    return color_as_rgb256(price_color_01(price))
