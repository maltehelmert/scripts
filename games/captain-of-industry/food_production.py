#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from fractions import Fraction


class Recipe(defaultdict):
    def __init__(self, data=()):
        defaultdict.__init__(self, int)
        self.update(data)
    def __add__(self, other):
        result = Recipe({})
        for key, value in self.items():
            result[key] += value
        for key, value in other.items():
            result[key] += value
        return result


def print_recipe(recipe, tag=None):
    if tag:
        print(f"{tag}:")
    for key, value in sorted(recipe.items()):
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
    total_harvest = Recipe()
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
    harvest_per_month = Recipe()
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


def get_recipe(what, needed):
    if what == "animal feed":
        multiplier = Fraction(needed, 144)
        return Recipe({
            "Mixer II (animal feed)": multiplier,
            "animal feed": multiplier * 144,
            "corn": -multiplier * 120,
        })
    elif what == "bread":
        multiplier = Fraction(needed, 24)
        return Recipe({
            "Baking Unit (bread)": multiplier,
            "bread": multiplier * 24,
            "flour": -multiplier * 16,
            "water": -multiplier * 8,
        })
    elif what == "cake":
        multiplier = Fraction(needed, 14)
        return Recipe({
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
        return Recipe({
            "Chicken Farm": multiplier,
            "chicken carcass": multiplier * 10,
            "egg": multiplier * Fraction(732, 100),
            "animal feed": -multiplier * Fraction(151, 10),
            "water": -multiplier * Fraction(181, 10),
        })
    elif what == "cooking oil":
        multiplier = Fraction(needed, 12)
        return Recipe({
            "Mill (cooking oil)": multiplier,
            "cooking oil": multiplier * 12,
            "animal feed": multiplier * 4,
            "canola": -multiplier * 16,
            })
    elif what == "flour":
        multiplier = Fraction(needed, 16)
        return Recipe({
            "Mill (flour)": multiplier,
            "flour": multiplier * 16,
            "animal feed": multiplier * 2,
            "wheat": -multiplier * 16,
            })
    elif what == "meat":
        multiplier = Fraction(needed, 15)
        return Recipe({
            "Food Processor (meat)": multiplier,
            "meat": multiplier * 15,
            "meat trimmings": multiplier * 6,
            "chicken carcass": -multiplier * 30,
            "water": -multiplier * 9,
            "salt": -multiplier * 3,
        })
    elif what == "meat trimmings":
        multiplier = Fraction(needed, 27)
        return Recipe({
            "Food Processor (meat trimmings)": multiplier,
            "meat trimmings": multiplier * 27,
            "chicken carcass": -multiplier * 30,
        })
    elif what == "sausage":
        multiplier = Fraction(needed, 24)
        return Recipe({
            "Food Processor (sausage)": multiplier,
            "sausage": multiplier * 24,
            "meat trimmings": -multiplier * 24,
            "flour": -multiplier * 6,
            "salt": -multiplier * 9,
        })
    elif what == "snack":
        multiplier = Fraction(needed, 24)
        return Recipe({
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
        return Recipe({
            "Food Processor (sugar)": multiplier,
            "sugar": multiplier * 12,
            "biomass": multiplier * 6,
            "sugar cane": -multiplier * 15,
            "water": -multiplier * 3,
            })
    elif what == "tofu":
        multiplier = Fraction(needed, 12)
        return Recipe({
            "Food Processor (tofu)": multiplier,
            "tofu": multiplier * 12,
            "animal feed": multiplier * Fraction(9, 2),
            "soybean": -multiplier * 9,
            "water": -multiplier * 6,
            "sulfur": -multiplier * Fraction(3, 2),
            "limestone": -multiplier * Fraction(3, 2),
        })
    raise ValueError(what)


def calculate_food_production(num_pops, round_up_chicken_farms, farms):
    # If round_up_chicken_farms is set, we round up the chicken
    # carcasses to multiples of 10, so that we have full chicken
    # farms.

    print(f"food production for {num_pops} pops...")
    production = Recipe()

    raw_foods = ["corn", "egg", "fruit", "potato", "vegetables"]
    refined_foods = ["bread", "cake", "meat", "sausage", "snack", "tofu"]
    all_foods = raw_foods + refined_foods

    def add_recipe(what, amount, extra_tag=None):
        nonlocal production
        recipe = get_recipe(what, amount)
        title = what
        if extra_tag:
            title += f" ({extra_tag})"
        print_recipe(recipe, title)
        production += recipe

    for food in refined_foods:
        add_recipe(food, get_food_needed(food, num_pops))

    intermediates = ["sugar", "flour", "cooking oil", "meat trimmings"]
    for what in intermediates:
        add_recipe(what, -production[what])

    carcasses_needed = -production["chicken carcass"]
    if round_up_chicken_farms:
        full_farms, remainder = divmod(carcasses_needed, 10)
        if remainder:
            full_farms += 1
        carcasses_needed = full_farms * 10
    add_recipe("chicken carcass", carcasses_needed)
    assert production["egg"] >= get_food_needed("egg", num_pops)

    # If there are excess chicken carcasses, they become meat trimmings.
    excess_carcasses = production["chicken carcass"]
    if excess_carcasses:
        trimmings = excess_carcasses * Fraction(9, 10)
        add_recipe("meat trimmings", trimmings, "excess")

    add_recipe("animal feed", -production["animal feed"])
    print_recipe(production, "production balance")

    consumption = Recipe()
    for food in all_foods:
        consumption[food] = -get_food_needed(food, num_pops)
    print_recipe(consumption, "settlement food consumption")

    balance = production + consumption
    should_be_balanced = [
        "animal feed", "bread", "cake", "chicken carcass", "cooking oil",
        "flour", "meat", "sausage", "snack", "sugar", "tofu"]
    for what in should_be_balanced:
        assert balance[what] == 0, what
        del balance[what]
    print_recipe(balance, "overall balance before farms")

    for farm_kind, fertility, schedule in farms:
        recipe = get_farm_info(farm_kind, fertility, schedule)
        description = f"{farm_kind} growing {', '.join(schedule)} at {fertility}%"
        print_recipe(recipe, description)
        balance += recipe

    print_recipe(balance, "final balance")


def do_new_farms():
    num_pops = 5200 * Fraction(14, 10)
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
    calculate_food_production(
        num_pops=num_pops, round_up_chicken_farms=True, farms=farms)


def do_old_farms():
    num_pops = 5200 * Fraction(14, 10)
    farms = [
        ("Greenhouse II", 100, ["fruit", "vegetables"]),
        ("Greenhouse II", 100, ["fruit", "vegetables"]),
        ("Greenhouse II", 100, ["potato", "vegetables"]),
        ("Greenhouse II", 100, ["corn", "vegetables"]),
        ("Greenhouse II", 100, ["vegetables", "potato", "tree sapling"]),
        ("Greenhouse II", 100, ["corn", "potato"]),
    ]

    consumption = Recipe()
    for food in ["fruit", "vegetables", "potato", "corn"]:
        consumption[food] = -get_food_needed(food, num_pops)
    print_recipe(consumption, "settlement food consumption")

    balance = Recipe(consumption)
    for farm_kind, fertility, schedule in farms:
        recipe = get_farm_info(farm_kind, fertility, schedule)
        description = f"{farm_kind} growing {', '.join(schedule)} at {fertility}%"
        print_recipe(recipe, description)
        balance += recipe
    print_recipe(balance, "balance")


# TODO:
#
# 1. Make it possible to select which food consumptions to consider to
#    make it possible to have all excess fruit at the top farm being
#    considered an excess product rather than an export product. (For
#    this, should probably split calculate_food_production into
#    multiple functions. See also the unnecessary code duplication
#    between do_new_farms() vs. do_old_farms()).
#
# 2. Add the excess steps that consume biomass and excess crops and
#    foods, producing fuel and organic fertilizer.
#
# 3. Add fertilizer production.

def main():
    do_new_farms()
    # do_old_farms()

if __name__ == "__main__":
    main()
