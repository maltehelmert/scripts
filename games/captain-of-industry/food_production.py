#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from fractions import Fraction


RAW_FOODS = ["corn", "egg", "fruit", "potato", "vegetables"]
REFINED_FOODS = ["bread", "cake", "meat", "sausage", "snack", "tofu"]
ALL_FOODS = RAW_FOODS + REFINED_FOODS


class Recipe(defaultdict):
    def __init__(self, data=(), /, title=None):
        defaultdict.__init__(self, int)
        self.update(data)
        self.title = title

    def copy(self):
        return Recipe(self, title=self.title)

    def __add__(self, other):
        result = self.copy()
        for key, value in other.items():
            result[key] += value
        return result

    def set_title(self, title):
        self.title = title

    def dump(self):
        if self.title:
            print(f"{self.title}:")
        for key, value in sorted(self.items()):
            print(f"    {key:31} {float(value):10.4f} {value}")


def get_crop_info(crop):
    infos = {
        "potato": (108, Fraction(63, 2), 3, 58),
        "corn": (160, 48, 4, 66),
        "wheat": (191, 63, 6, 58),
        "tree sapling": (324, 72, 12, 60),
        "soybean": (144, 60, 4, 22),
        "sugar cane": (432, 135, 9, 198),
        "vegetables": (128, 42, 4, 60),
        "fruit": (319, 72, 8, 80),
        "canola": (84, 27, 3, 36),
    }
    return infos[crop]


def get_farm_kind_info(kind):
    infos = {
        "Irrigated Farm": (1, 1),
        "Greenhouse": (Fraction(112, 100), Fraction(125, 100)),
        "Greenhouse II": (Fraction(125, 100), Fraction(150, 100)),
    }
    return infos[kind]


def get_farm_description(kind, fertility_percentage, schedule):
    schedule_desc = "".join(crop[:2].title() for crop in schedule)
    return f"{kind} ({schedule_desc}, {fertility_percentage}%)"


def get_farm_info(kind, fertility_percentage, schedule):
    assert 100 <= fertility_percentage <= 140
    fertility_multiplier = Fraction(fertility_percentage, 100)
    bonus_fertility = fertility_percentage - 100
    cost_multiplier, harvest_multiplier = get_farm_kind_info(kind)
    total_water = 0
    total_fertilizer = 0
    total_months = 0
    title = f"{kind} growing {', '.join(schedule)} at {fertility_percentage}%"
    total_harvest = Recipe(title=title)
    for index, crop in enumerate(schedule):
        water, fertilizer, months, harvest = get_crop_info(crop)
        total_water += water * cost_multiplier
        adjusted_fertilizer = fertilizer * cost_multiplier
        if schedule[index - 1] == crop:
            # Apply penalty for lack of crop rotation.
            adjusted_fertilizer *= Fraction(3, 2)
        # The following bonus fertilizer cost for fertility above 100%
        # is based on a formula given in the wiki, with the constant 0.06
        # adjusted from 0.002 on the wiki to better match the data. In my tests
        # it was usually the same as the numbers shown in the UI after rounding,
        # with a discrepancy of 0.1 sometimes.
        adjusted_fertilizer *= (1 + 2 * Fraction(bonus_fertility, 100))
        adjusted_fertilizer += Fraction(6, 100) * bonus_fertility * months
        total_fertilizer += adjusted_fertilizer
        total_months += months
        adjusted_harvest = harvest * harvest_multiplier
        if adjusted_harvest.denominator == 2:
            adjusted_harvest += Fraction(1, 2)
            ## We round up the harvest if it has a fractional part of
            ## 0.5, which is the only fractional part that occurs (and
            ## that only for Greenhouse, never for Irrigated Farm or
            ## Greenhouse II). Note that the harvest cannot be
            ## fractional because a discrete number of crops are
            ## harvested. (It could of course alternate between
            ## harvests to simulate rounding, but the way the numbers
            ## are displayed suggests otherwise.)
        assert adjusted_harvest.denominator == 1
        adjusted_harvest *= fertility_multiplier
        # I don' bother with rounding here because I think fertility
        # level is not an exact science anyway. For example, I think
        # it can drop below the exact percentage because (with
        # advanced fertilizers) it can only move in increments of 2 or
        # more at a time. And there may also be a delay between
        # fertility dropping and being adjusted that already affects
        # plant growth. Best not require that the harvest is within
        # better than 1-2% precision.
        total_harvest[crop] += adjusted_harvest
    harvest_per_month = Recipe(title=title)
    for key in total_harvest:
        harvest_per_month[key] = total_harvest[key] / total_months
    ## Note: the calculation here different from what was displayed in
    ## the game in one case by an amount around 0.08-0.09, which
    ## cannot be explained by regular rounding. The in-game numbers
    ## appeared implausible, so this may be implausible rounding. In
    ## any case, this is a margin of error we should generally allow
    ## for in our planning anyway.
    water_per_month = total_water / total_months
    fertilizer_per_month = total_fertilizer / total_months
    harvest_per_month["water"] = -water_per_month
    harvest_per_month["fertility points"] = -fertilizer_per_month
    farm_desc = get_farm_description(kind, fertility_percentage, schedule)
    harvest_per_month[farm_desc] += 1
    return harvest_per_month


def get_food_needed(what, num_pops):
    pop_k = Fraction(num_pops, 1000)
    need_per_k = {
        "bread": Fraction(20, 12),
        "cake": Fraction(25, 8),
        "corn": Fraction(30, 12),
        "egg": Fraction(30, 16),
        "fruit": Fraction(Fraction(63, 2), 8),
        "meat": Fraction(27, 16),
        "potato": Fraction(42, 12),
        "sausage": Fraction(Fraction(67, 2), 16),
        "snack": Fraction(26, 8),
        "tofu": Fraction(18, 16),
        "vegetables": Fraction(42, 8),
        }
    return pop_k * need_per_k[what]


def get_recipe(what, needed, /, tag=None):
    title = what
    if tag:
        title += f" ({tag})"
    def make_recipe(data):
        return Recipe(data, title=title)
    if what == "animal feed":
        multiplier = Fraction(needed, 144)
        return make_recipe({
            "Mixer II (animal feed)": multiplier,
            "animal feed": multiplier * 144,
            "corn": -multiplier * 120,
        })
    elif what == "bread":
        multiplier = Fraction(needed, 24)
        return make_recipe({
            "Baking Unit (bread)": multiplier,
            "bread": multiplier * 24,
            "flour": -multiplier * 16,
            "water": -multiplier * 8,
        })
    elif what == "cake":
        multiplier = Fraction(needed, 14)
        return make_recipe({
            "Baking Unit (cake)": multiplier,
            "cake": multiplier * 14,
            "flour": -multiplier * 10,
            "sugar": -multiplier * 4,
            "cooking oil": -multiplier * 2,
            "egg": -multiplier * 2,
            "fruit": -multiplier * 2,
        })
    elif what == "chicken carcass":
        multiplier = Fraction(needed, 10)
        return make_recipe({
            "Chicken Farm": multiplier,
            "chicken carcass": multiplier * 10,
            "egg": multiplier * Fraction(732, 100),
            "animal feed": -multiplier * Fraction(151, 10),
            "water": -multiplier * Fraction(181, 10),
        })
    elif what == "cooking oil":
        multiplier = Fraction(needed, 12)
        return make_recipe({
            "Mill (cooking oil)": multiplier,
            "cooking oil": multiplier * 12,
            "animal feed": multiplier * 4,
            "canola": -multiplier * 16,
            })
    elif what == "flour":
        multiplier = Fraction(needed, 16)
        return make_recipe({
            "Mill (flour)": multiplier,
            "flour": multiplier * 16,
            "animal feed": multiplier * 2,
            "wheat": -multiplier * 16,
            })
    elif what == "meat":
        multiplier = Fraction(needed, 15)
        return make_recipe({
            "Food Processor (meat)": multiplier,
            "meat": multiplier * 15,
            "meat trimmings": multiplier * 6,
            "chicken carcass": -multiplier * 30,
            "water": -multiplier * 9,
            "salt": -multiplier * 3,
        })
    elif what == "meat trimmings":
        multiplier = Fraction(needed, 27)
        return make_recipe({
            "Food Processor (meat trimmings)": multiplier,
            "meat trimmings": multiplier * 27,
            "chicken carcass": -multiplier * 30,
        })
    elif what == "sausage":
        multiplier = Fraction(needed, 24)
        return make_recipe({
            "Food Processor (sausage)": multiplier,
            "sausage": multiplier * 24,
            "meat trimmings": -multiplier * 24,
            "flour": -multiplier * 6,
            "salt": -multiplier * 9,
        })
    elif what == "snack":
        multiplier = Fraction(needed, 24)
        return make_recipe({
            "Food Processor (snack)": multiplier,
            "snack": multiplier * 24,
            "biomass": multiplier * 3,
            "corn": -multiplier * 24,
            "salt": -multiplier * 6,
            "cooking oil": -multiplier * 3,
            "plastic": -multiplier * 3,
        })
    elif what == "sugar":
        multiplier = Fraction(needed, 12)
        return make_recipe({
            "Food Processor (sugar)": multiplier,
            "sugar": multiplier * 12,
            "biomass": multiplier * 6,
            "sugar cane": -multiplier * 15,
            "water": -multiplier * 3,
            })
    elif what == "tofu":
        multiplier = Fraction(needed, 12)
        return make_recipe({
            "Food Processor (tofu)": multiplier,
            "tofu": multiplier * 12,
            "animal feed": multiplier * Fraction(9, 2),
            "soybean": -multiplier * 9,
            "water": -multiplier * 6,
            "sulfur": -multiplier * Fraction(3, 2),
            "limestone": -multiplier * Fraction(3, 2),
        })
    raise ValueError(what)


def get_food_processing(num_pops, full_chicken_farms, verbose=False):
    # If full_chicken_farms is set, we round up the chicken carcasses
    # to multiples of 10, so that we have full chicken farms.

    processing = Recipe(title=f"food processing for {num_pops} pops")

    def add_recipe(what, amount, tag=None):
        nonlocal processing
        recipe = get_recipe(what, amount, tag=tag)
        if verbose:
            recipe.dump()
        processing += recipe

    for food in REFINED_FOODS:
        add_recipe(food, get_food_needed(food, num_pops))

    intermediates = ["sugar", "flour", "cooking oil", "meat trimmings"]
    for what in intermediates:
        add_recipe(what, -processing[what])

    carcasses_needed = -processing["chicken carcass"]
    if full_chicken_farms:
        full_farms, remainder = divmod(carcasses_needed, 10)
        if remainder:
            full_farms += 1
        carcasses_needed = full_farms * 10
    add_recipe("chicken carcass", carcasses_needed)
    ## TODO: If we parametrize the production targets more, we need to
    ## change the assertion to more logic where we also deal with the
    ## case where egg production is more limited than chicken carcass
    ## production. (We then need to compute the number of farms based
    ## on the egg target.)
    assert processing["egg"] >= get_food_needed("egg", num_pops)

    # If there are excess chicken carcasses, they become meat trimmings.
    excess_carcasses = processing["chicken carcass"]
    if excess_carcasses:
        trimmings = excess_carcasses * Fraction(9, 10)
        add_recipe("meat trimmings", trimmings, "excess")

    add_recipe("animal feed", -processing["animal feed"])

    should_be_balanced = ["animal feed", "chicken carcass", "cooking oil", "flour", "sugar"]
    for what in should_be_balanced:
        assert processing[what] == 0, what
        del processing[what]

    if verbose:
        processing.dump()
    return processing


def get_food_consumption(num_pops):
    consumption = Recipe(title=f"food consumption for {num_pops} pops")
    for food in ALL_FOODS:
        consumption[food] = -get_food_needed(food, num_pops)
    return consumption


def get_farm_production(farms, verbose=False):
    production = Recipe(title=f"farm production ({len(farms)} farms)")
    for farm_kind, fertility, schedule in farms:
        recipe = get_farm_info(farm_kind, fertility, schedule)
        if verbose:
            recipe.dump()
        production += recipe
    return production


def get_new_farms():
    farms = [
        ("Greenhouse II", 100, ["corn", "wheat", "corn", "soybean"]),
        ("Greenhouse II", 100, ["corn", "wheat", "corn", "soybean"]),
        ("Greenhouse II", 100, ["corn", "wheat", "corn", "soybean"]),
        ("Greenhouse II", 100, ["corn", "wheat", "corn", "soybean"]),
        ("Greenhouse II", 100, ["corn", "wheat"]),
        ("Greenhouse II", 100, ["corn", "wheat", "corn", "sugar cane"]),
        ("Greenhouse II", 100, ["corn", "fruit"]),
        ("Greenhouse II", 100, ["canola", "canola", "canola", "fruit"]),
    ]
    return farms


def get_old_farms():
    farms = [
        ("Greenhouse II", 100, ["fruit", "vegetables"]),
        ("Greenhouse II", 100, ["fruit", "vegetables"]),
        ("Greenhouse II", 100, ["potato", "vegetables"]),
        ("Greenhouse II", 100, ["corn", "vegetables"]),
        ("Greenhouse II", 100, ["vegetables", "potato", "tree sapling"]),
        ("Greenhouse II", 100, ["corn", "potato"]),
    ]
    return farms


def get_middle_plateau_balance(num_pops):
    balance = Recipe(title="new farms and food processing balance")
    balance += get_farm_production(get_new_farms())
    balance += get_food_processing(num_pops=num_pops, full_chicken_farms=True, verbose=False)
    return balance


def get_lower_plateau_balance(num_pops):
    balance = Recipe(title="old farms and settlement balance")
    balance += get_farm_production(get_old_farms())
    balance += get_food_consumption(num_pops)
    return balance


def get_overall_food_balance(num_pops):
    balance = Recipe(title="overall food balance")
    balance += get_lower_plateau_balance(num_pops)
    balance += get_middle_plateau_balance(num_pops)
    return balance


# TODO:
## - Make get_food_processing() more general to allow arbitrary targets for the refined
##   foods.
## - In get_food_processing(), or in a new function built on top of a modified
##   get_food_processing(), allow setting two production targets:
##   - One with the current semantics, which gives the production we
##     eventually need in the steady state at the max designed population.
##     This is in particular used to decide how many of each building we need.
##   - A lower one that we can use to see how much excess will be generated
##     or input product will remain unused if we don't run thing in full throttle,
##     for example because population is still lower. This can then be used to
##     dimension the excess consumption buildings.
## - Add the excess steps that consume biomass and excess crops and
##   foods, producing fuel and organic fertilizer.
## - Add fertilizer production.

def main():
    num_pops = 5200 * Fraction(14, 10)
    num_pops = 8000
    # get_farm_production(get_new_farms()).dump()
    # get_farm_production(get_old_farms()).dump()
    get_lower_plateau_balance(num_pops).dump()
    get_middle_plateau_balance(num_pops).dump()
    get_overall_food_balance(num_pops).dump()


if __name__ == "__main__":
    main()
