
def get_EIN(ein_input: tuple[str, str, str]) -> tuple[int, int, int]:
    EIN = []
    for item in ein_input:
        try:
            rating = int(100 * float(item))
        except ValueError:
            # for now ignore the error and set rating to 0
            rating = 0
        EIN.append(rating)
    return tuple(EIN)



# EIN multipliers as 3-tuple, EIN as 3-tuple (of integers)
def calculate_ride_value(EIN_multipliers : tuple, EIN : tuple) -> int:
    ride_value = 0
    if EIN_multipliers and EIN:
        for i in range(len(EIN)):
            ride_value += (EIN[i] * EIN_multipliers[i]) // 1024
    return ride_value

# apply age modifiers to ride value
def apply_age_to_ride_value(ride_value : int, age_modifiers : dict) -> int:
    multiplier = age_modifiers['multiplier']
    divisor = age_modifiers['divisor']
    add = age_modifiers['addition']
    return (ride_value * multiplier) // divisor + add

# if there are many rides of the same type, value drops to 3/4
def apply_many_rides_modifier(modified_value : int) -> int:
    return modified_value - modified_value // 4

# if guests have to pay for entering the park value drops to 1/4
def apply_pay_for_entry(modified_value : int) -> int:
    return modified_value // 4

# maximal price is 2*modified_value/10, or maybe that's the first unacceptable price?
def maximize_price(modified_value : int) -> int:
    # price in cents or whatever (so we are dealing with integers)
    # max_price = 2 * modified_value * 10
    return min(2000, 20 * modified_value)

# calculate max prices in cases of unique ride and many similar rides
def calc_max_prices(EIN : tuple, EIN_multipliers : tuple, age_modifier : dict, free_entry : bool) -> tuple:
    ride_value = calculate_ride_value(EIN_multipliers, EIN)
    # print(ride_value)
    modified_value = apply_age_to_ride_value(ride_value, age_modifier)
    # print(modified_value)
    if not free_entry:
        modified_value = apply_pay_for_entry(modified_value)
    modified_value_nonunique = apply_many_rides_modifier(modified_value)
    return (maximize_price(modified_value), maximize_price(modified_value_nonunique))