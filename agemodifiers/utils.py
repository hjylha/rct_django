from .models import AgeModifier


def get_start_ages() -> tuple[int]:
    age_modifiers = AgeModifier.objects.all()
    ages = set()
    for modifier in age_modifiers:
        ages.add(modifier.age_start)
    ages = list(ages)
    ages.sort()
    return tuple(ages)


def get_sorted_age_modifiers(in_og: bool = False) -> tuple[AgeModifier]:
    sorted_age_modifiers = []
    for age in get_start_ages():
        sorted_age_modifiers.append(
            AgeModifier.objects.get(in_og=in_og, age_start=age))
    return tuple(sorted_age_modifiers)
