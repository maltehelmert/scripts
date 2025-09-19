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

    def __iadd__(self, other):
        for key, value in other.items():
            self[key] += value
        return self

    def set_title(self, title):
        self.title = title

    def dump(self):
        if self.title:
            print(f"{self.title}:")
        for key, value in sorted(self.items()):
            print(f"    {key:35} {float(value):10.4f} {value}")


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
            # We round up the harvest if it has a fractional part of
            # 0.5, which is the only fractional part that occurs (and
            # that only for Greenhouse, never for Irrigated Farm or
            # Greenhouse II). Note that the harvest cannot be
            # fractional because a discrete number of crops are
            # harvested. (It could of course alternate between
            # harvests to simulate rounding, but the way the numbers
            # are displayed suggests otherwise.)
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
    # Note: the calculation here differed from what was displayed in
    # the game in one case by an amount around 0.08-0.09, which cannot
    # be explained by regular rounding. The in-game numbers appeared
    # implausible, so this may be a rounding bug or similar in game.
    # In any case, this is a margin of error we should generally allow
    # for in our planning anyway.
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


def get_excess_recipe(what, amount):
    title = f"excess {what} consumption"
    def make_recipe(data):
        return Recipe(data, title=title)
    def make_digester(consumed, fuel, compost):
        multiplier = Fraction(amount, consumed)
        recipe = Recipe(title=title)
        recipe["Anaerobic Digester"] = multiplier
        recipe[f"Anaerobic Digester ({what})"] = multiplier
        recipe[what] = -amount
        recipe["fuel"] = multiplier * fuel
        recipe["compost"] = multiplier * compost
        return recipe
    if what == "fruit":
        return make_digester(12, 12, 1)
    elif what == "wheat":
        return make_digester(12, 12, 1)
    elif what == "corn":
        return make_digester(14, 14, 1)
    elif what == "soybean":
        return make_digester(12, 12, 1)
    elif what == "sugar cane":
        return make_digester(12, 8, 1)
    elif what == "meat trimmings":
        return make_digester(8, 4, 2)
    elif what == "egg":
        return make_digester(12, 12, 1)
    elif what == "biomass":
        multiplier = Fraction(amount, 24)
        return make_recipe({
            "Mixer II (biomass to compost)": multiplier,
            "biomass": -multiplier * 24,
            "compost": multiplier * 16,
            })
    elif what == "canola":
        return make_recipe({
            "Remains at Farm (canola)": amount,
            what: -amount})
    raise ValueError(what)


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


def get_chicken_farms_needed(recipe, use_whole_chicken_farms):
    carcasses = -recipe["chicken carcass"]
    eggs = -recipe["egg"]
    farm_demand = max(Fraction(carcasses, 10),
                      Fraction(eggs, Fraction(732, 100)))
    if use_whole_chicken_farms:
        full_farms, remainder = divmod(farm_demand, 1)
        return full_farms + int(remainder > 0)
    else:
        return farm_demand


def get_food_processing(min_consumption, max_consumption, use_whole_chicken_farms):
    min_processing = Recipe(title=f"food processing (min load)")
    max_processing = Recipe(title=f"food processing (max load)")

    for processing, consumption in [(min_processing, min_consumption),
                                    (max_processing, max_consumption)]:
        for food, amount in consumption.items():
            if food in REFINED_FOODS:
                processing += get_recipe(food, -amount)

        intermediates = ["sugar", "flour", "cooking oil", "meat trimmings"]
        for what in intermediates:
            processing += get_recipe(what, -processing[what])

    farms_needed = get_chicken_farms_needed(max_consumption + max_processing,
                                            use_whole_chicken_farms)

    for processing in [min_processing, max_processing]:
        processing += get_recipe("chicken carcass", farms_needed * 10)
        # Excess chicken carcasses become meat trimmings.
        excess_carcasses = processing["chicken carcass"]
        if excess_carcasses:
            trimmings = excess_carcasses * Fraction(9, 10)
            processing += get_recipe("meat trimmings", trimmings, tag="excess")

        processing += get_recipe("animal feed", -processing["animal feed"])

        should_be_balanced = ["animal feed", "chicken carcass", "cooking oil", "flour", "sugar"]
        for what in should_be_balanced:
            assert processing[what] == 0, what
            del processing[what]

    return min_processing, max_processing


def get_excess_conversion(farms, min_pops, max_pops, use_whole_chicken_farms):
    farm_production = get_farm_production(farms)
    min_consumption = get_food_consumption(min_pops, REFINED_FOODS + ["egg"])
    max_consumption = get_food_consumption(max_pops, REFINED_FOODS + ["egg"])
    min_processing, max_processing = get_food_processing(
        min_consumption, max_consumption, use_whole_chicken_farms)
    min_balance = Recipe(farm_production + min_processing + min_consumption, title="min balance")
    max_balance = Recipe(farm_production + max_processing + max_consumption, title="max balance")

    excess_products = ["biomass", "canola", "egg", "meat trimmings",
                       "corn", "soybean", "sugar cane", "wheat", "fruit"]
    for balance in [min_balance, max_balance]:
        for what, amount in balance.items():
            if amount > 0 and what[0].islower():
                assert what in excess_products
    conversion = Recipe(title=f"excess conversion ({min_pops}-{max_pops} pops)")
    for what in excess_products:
        min_value, max_value = sorted([min_balance[what], max_balance[what]])
        if what == "biomass":
            assert max_balance[what] >= min_balance[what]
        else:
            assert min_balance[what] >= max_balance[what]
        value = max(min_balance[what], max_balance[what])
        conversion += get_excess_recipe(what, value)
    return conversion


def get_food_consumption(num_pops, foods=ALL_FOODS):
    consumption = Recipe(title=f"food consumption for {num_pops} pops")
    for food in foods:
        consumption[food] = -get_food_needed(food, num_pops)
    return consumption


def get_farm_production(farms):
    production = Recipe(title=f"farm production ({len(farms)} farms)")
    for farm_kind, fertility, schedule in farms:
        recipe = get_farm_info(farm_kind, fertility, schedule)
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
        ("Greenhouse II", 100, ["corn", "vegetables"]),
    ]
    return farms


def get_combined_farms():
    farms = [
        ("Greenhouse II", 100, ["corn", "potato"]),
        ("Greenhouse II", 100, ["corn", "soybean"]),
        ("Greenhouse II", 100, ["soybean", "corn"]),
        ("Greenhouse II", 100, ["corn", "wheat"]),
        #
        ("Greenhouse II", 100, ["corn", "wheat"]),
        ("Greenhouse II", 100, ["wheat", "corn"]),
        ("Greenhouse II", 100, ["wheat", "corn"]),
        ("Greenhouse II", 100, ["corn", "vegetables"]),
        #
        ("Greenhouse II", 100, ["canola", "fruit", "canola", "vegetables"]),
        ("Greenhouse II", 100, ["canola", "fruit"]),
        ("Greenhouse II", 100, ["corn", "fruit", "corn", "sugar cane"]),
        ("Greenhouse II", 100, ["fruit", "vegetables"]),
        #
        ("Greenhouse II", 100, ["vegetables", "fruit"]),
        ("Greenhouse II", 100, ["potato", "vegetables"]),
        ("Greenhouse II", 100, ["potato", "corn", "vegetables"]),
    ]
    return farms


def get_middle_plateau_balance(num_pops):
    consumption = get_food_consumption(num_pops)
    min_processing, max_processing = get_food_processing(
        consumption, consumption,
        use_whole_chicken_farms=True)
    balance = Recipe(title=f"new farms and food processing balance ({num_pops} pops)")
    balance += get_farm_production(get_new_farms())
    balance += max_processing
    return balance


def get_lower_plateau_balance(num_pops):
    balance = Recipe(title=f"old farms and settlement balance ({num_pops} pops)")
    balance += get_farm_production(get_old_farms())
    balance += get_food_consumption(num_pops)
    return balance


def get_overall_food_balance(num_pops):
    balance = Recipe(title=f"overall food balance ({num_pops} pops)")
    balance += get_lower_plateau_balance(num_pops)
    balance += get_middle_plateau_balance(num_pops)
    return balance


def get_combined_food_balance(num_pops):
    consumption = get_food_consumption(num_pops)
    min_processing, max_processing = get_food_processing(
        consumption, consumption,
        use_whole_chicken_farms=True)
    balance = Recipe(title=f"combined farms and food processing balance ({num_pops} pops)")
    balance += get_farm_production(get_combined_farms())
    balance += max_processing
    balance += get_food_consumption(num_pops)
    return balance


def main():
    # min_pops = 4400 * Fraction(14, 10)
    # max_pops = 5200 * Fraction(14, 10)
    # max_pops = 8000
    min_pops = 5200 * Fraction(14, 10)
    max_pops = 6400 * Fraction(14, 10)
    max_pops = 9000
    num_pops = max_pops

    get_food_consumption(num_pops).dump()
    # get_farm_production(get_new_farms()).dump()
    # get_farm_production(get_old_farms()).dump()
    get_farm_production(get_combined_farms()).dump()
    # get_lower_plateau_balance(num_pops).dump()
    # get_middle_plateau_balance(num_pops).dump()
    get_combined_food_balance(num_pops).dump()
    # get_excess_conversion(get_combined_farms(), min_pops, max_pops,
    #                       use_whole_chicken_farms=True).dump()


if __name__ == "__main__":
    main()
