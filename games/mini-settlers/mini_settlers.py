#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction


class F(Fraction):
    def __format__(self, *args, **kwargs):
        return format(float(self), *args, **kwargs)
    def __add__(self, other):
        return F(super().__add__(other))
    def __radd__(self, other):
        return F(super().__radd__(other))
    def __sub__(self, other):
        return F(super().__sub__(other))
    def __rsub__(self, other):
        return F(super().__rsub__(other))
    def __mul__(self, other):
        return F(super().__mul__(other))
    def __rmul__(self, other):
        return F(super().__rmul__(other))
    def __truediv__(self, other):
        return F(super().__truediv__(other))
    def __rtruediv__(self, other):
        return F(super().__rtruediv__(other))


@dataclass
class Building:
    name: str
    sources: list
    targets: list
    duration: int


@dataclass
class CityCenter:
    name: str
    number_of_houses: int
    required_resources: list
    consumption_time_per_resource: int

    def get_cycle_time(self):
        return self.consumption_time_per_resource * len(self.required_resources)

    def get_virtual_resource(self):
        return "needs of " + self.name

    def get_virtual_building_for_house(self):
        return self.get_virtual_building(num_houses=1)

    def get_virtual_building_for_center(self):
        return self.get_virtual_building(num_houses=self.number_of_houses)

    def get_virtual_building(self, num_houses):
        sources = [(num_houses, resource) for resource in self.required_resources]
        duration = self.get_cycle_time()
        return Building(
            name=self.name,
            sources=sources,
            targets=[(1, self.get_virtual_resource())],
            duration=duration,
        )


def parse_ingredient(text):
    amount_text, ingredient = text.split(None, 1)
    return int(amount_text.strip()), ingredient.strip()


def parse_ingredients(text):
    if text:
        return [parse_ingredient(part.strip()) for part in text.split(",")]
    else:
        return []


def parse_recipe(text):
    sources, targets = text.split("->")
    sources = parse_ingredients(sources.strip())
    targets = parse_ingredients(targets.strip())
    return sources, targets


def parse_building(name, recipe_text, duration):
    sources, targets = parse_recipe(recipe_text)
    return Building(name, sources, targets, duration)


def filter_preferred(buildings):
    # Filter our buildings with alt recipes we don't want to use in
    # our calculations.
    removed = {
        "water pump",
        "sea water filter",
        "charcoal maker",
        "wood factory",
        "stone mine",
        "coal mine",
        "iron mine",
        }
    return [building for building in buildings
            if building.name not in removed]


def filter_coral_crescent(buildings):
    removed = {
        "water well",
        "water pump",
        "sea water filter",
        "apple farm",
        "wheat farm",
        "cow farm",
        "lumber camp",
        "forester",
        "wood factory",
        #
        "charcoal maker",
        "stone mine",
        }
    buildings = [building for building in buildings
                 if building.name not in removed]
    TRADERS = [
        parse_building("trader A (apple)", "-> 1 apple", 2),
        parse_building("trader B (stone -> lumber)", "1 stone -> 1 lumber", 2),
        parse_building("trader C (stone tool -> cow)", "1 stone tool -> 1 cow", 2),
        parse_building("trader D (juice -> wheat)", "1 juice -> 1 wheat", 2),
    ]

    return buildings + TRADERS


BUILDINGS = [
    parse_building("water well", "-> 1 water", 7),
    parse_building("water pump", "1 bread -> 3 water", 5), # alt
    parse_building("sea water filter", "1 coal -> 2 water", 20), # alt
    #
    parse_building("apple farm", "1 water -> 2 apple", 10),
    parse_building("juice maker", "1 plank, 1 apple -> 2 juice", 15),
    parse_building("wheat farm", "1 water -> 2 wheat", 10),
    parse_building("bakery", "2 wheat, 1 coal -> 2 bread", 20),
    parse_building("cow farm", "1 water, 1 wheat -> 2 cow", 15),
    parse_building("milk factory", "1 cow, 1 glass -> 2 milk", 20),
    parse_building("butcher", "1 cow, 1 iron tool -> 2 meat", 20),
    parse_building("restaurant", "1 bread, 1 meat -> 2 sandwich", 20),
    #
    parse_building("lumber camp", "1 apple, 1 tree -> 1 lumber", 15),
    parse_building("saw mill", "1 lumber -> 2 wood", 10),
    parse_building("forester", "1 water -> 1 tree", 10),
    parse_building("carpenter workshop", "1 wood, 1 stone tool -> 2 plank", 25),
    parse_building("charcoal maker", "1 apple, 1 lumber -> 2 coal", 15), # alt
    parse_building("wood factory", "1 bread, 1 tree -> 2 wood", 20), # alt
    parse_building("wood beam workshop", "1 iron tool, 1 plank -> 2 wood beam", 40),
    #
    parse_building("stone quarry", "1 apple -> 2 stone", 20),
    parse_building("stone mine", "1 bread -> 3 stone", 10), # alt
    parse_building("coal quarry", "1 apple -> 2 coal", 20),
    parse_building("coal mine", "1 bread -> 3 coal", 10), # alt
    parse_building("iron quarry", "1 bread -> 2 iron ore", 20),
    parse_building("iron mine", "1 bread -> 3 iron ore", 10), # alt
    parse_building("sand collector", "1 juice -> 1 sand", 20),
    parse_building("diamond mine", "1 meat, 1 steel tool -> 3 diamond", 10),
    #
    parse_building("stone tool maker", "1 stone, 1 wood -> 2 stone tool", 7),
    parse_building("iron tool maker", "1 iron bar, 1 stone tool -> 2 iron tool", 10),
    parse_building("steel tool maker", "1 steel beam, 1 iron tool -> 2 steel tool", 15),
    #
    parse_building("wood furniture maker", "1 lumber, 1 stone tool -> 2 wood furniture", 15),
    parse_building("leather furniture maker", "1 leather, 1 wood furniture -> 1 leather furniture", 15),
    parse_building("luxury furniture maker", "1 diamond, 1 leather furniture -> 1 luxury furniture", 25),
    #
    parse_building("stone blocker", "1 stone, 1 stone tool -> 2 stone block", 25),
    parse_building("stone masonry", "1 iron tool, 1 stone block -> 2 stone tile", 40),
    parse_building("iron smelter", "1 coal, 2 iron ore -> 2 iron bar", 15),
    parse_building("paper factory", "1 wood, 1 iron tool -> 2 paper", 30),
    parse_building("leather maker", "1 cow, 1 iron tool -> 2 leather", 20),
    parse_building("glass maker", "1 sand, 1 coal -> 2 glass", 25),
    parse_building("steel smelter", "1 coal, 1 iron bar -> 1 steel beam", 20),
    parse_building("library", "1 leather, 1 paper, 1 steel tool -> 2 book", 25),
]


CITY_CENTER_I = CityCenter(
    name="city center I",
    number_of_houses=10,
    required_resources=["water", "apple", "wood furniture"],
    consumption_time_per_resource=50,
    # The game says 50 seconds. It may be worth measuring this.
)


CITY_CENTER_II = CityCenter(
    name="city center II",
    number_of_houses=15,
    required_resources=["juice", "bread", "paper", "leather furniture"],
    consumption_time_per_resource=50,
    # The game says 50 seconds. It may be worth measuring this.
)


CITY_CENTER_III = CityCenter(
    name="city center III",
    number_of_houses=20,
    required_resources=["milk", "sandwich", "book", "luxury furniture"],
    consumption_time_per_resource=60,
    # The game says 60 seconds. It may be worth measuring this.
)


NATIVE_TOWN_CENTER_II = CityCenter(
    name="native town center II",
    number_of_houses=15,
    required_resources=["plank", "iron tool", "leather"],
    consumption_time_per_resource=55,
    # I measured 55-60 seconds; the game does not tell us.
)


def scale_tally(tally, factor):
    return {key: value * factor for key, value in tally.items()}


def add_to_tally(source, target):
    for key, value in source.items():
        target[key] += value


def get_producers(buildings):
    producers = {}
    for building in buildings:
        assert len(building.targets) == 1
        target = building.targets[0][1]
        if target in producers:
            existing = producers[target]
            print(f"skipping {building.name} in favour of {existing.name}")
        else:
            producers[target] = building
    return producers


def get_requirements(resource, producers, given):
    producer = producers[resource]
    production_time = producer.duration
    (amount_produced, item_produced), = producer.targets
    assert item_produced == resource
    multiplier = F(1, amount_produced)
    ingredients = defaultdict(int)
    buildings = defaultdict(int)
    if resource in given:
        ingredients[f"{resource} [given]"] += 1
    else:
        ingredients[resource] += 1
        buildings[producer.name] += multiplier * production_time
        for amount_needed, ingredient in producer.sources:
            factor = multiplier * amount_needed
            rec_ingredients, rec_buildings = get_requirements(ingredient, producers, given)
            add_to_tally(scale_tally(rec_ingredients, factor), ingredients)
            add_to_tally(scale_tally(rec_buildings, factor), buildings)
    return ingredients, buildings


def print_buildings():
    for building in BUILDINGS:
        print(building)


def print_tally(tally, indent=""):
    for element, amount in tally.items():
        print(f"{indent}{amount:8.3f} {element} [exact: {amount.numerator}/{amount.denominator}]")


def analyze_scenario(scenario, filter_func=filter_preferred, given=set()):
    print("analyzing scenario...")
    if given:
        print(f"assuming as given ingredients: {', '.join(sorted(given))}")
    SECONDS_PER_MINUTE = 60
    virtual_buildings = [center.get_virtual_building_for_center()
                         for amount, center in scenario]
    producers = get_producers(filter_func(BUILDINGS + virtual_buildings))
    total_ingredients = defaultdict(int)
    total_buildings = defaultdict(int)
    for amount, center in scenario:
        need = center.get_virtual_resource()
        ingredients, buildings = get_requirements(need, producers, given)
        ingredients_multiplier = amount * F(SECONDS_PER_MINUTE, center.get_cycle_time())
        buildings_multiplier = amount * F(1, center.get_cycle_time())
        add_to_tally(scale_tally(ingredients, ingredients_multiplier), total_ingredients)
        add_to_tally(scale_tally(buildings, buildings_multiplier), total_buildings)
    print("ingredients production per minute:")
    print_tally(total_ingredients, "  ")
    print("buildings needed:")
    print_tally(total_buildings, "  ")


def analyze_house(center, filter_func=filter_preferred, given=set()):
    print(f"analyzing 1 house of {center.name}...")
    if given:
        print(f"assuming as given ingredients: {', '.join(sorted(given))}")
    virtual_buildings = [center.get_virtual_building_for_house()]
    producers = get_producers(filter_func(BUILDINGS + virtual_buildings))
    need = center.get_virtual_resource()
    ingredients, buildings = get_requirements(need, producers, given)
    print("ingredients needed per house per cycle:")
    print_tally(ingredients, "  ")
    print("building production seconds needed per house per cycle:")
    print_tally(buildings, "  ")


def analyze_build(need, filter_func=filter_preferred, given=set()):
    print(f"analyzing build for {need}...")
    if given:
        print(f"assuming as given ingredients: {', '.join(sorted(given))}")
    producers = get_producers(filter_func(BUILDINGS))
    ingredients, buildings = get_requirements(need, producers, given)
    print("ingredients needed per resource produced:")
    print_tally(ingredients, "  ")
    print("building production seconds needed per resource produced:")
    print_tally(buildings, "  ")


def main():
    SCENARIO_HARBOR_ISLANDS = [
        (2, CITY_CENTER_II),
        (1, NATIVE_TOWN_CENTER_II),
    ]
    SCENARIO_CORAL_CRESCENT = [
        (3, CITY_CENTER_II),
    ]
    SCENARIO_CORAL_HAVEN = [
        (2, CITY_CENTER_III),
    ]
    # analyze_house(NATIVE_TOWN_CENTER_II)
    # analyze_scenario(SCENARIO_HARBOR_ISLANDS)
    # analyze_house(CITY_CENTER_II, filter_coral_crescent)
    # analyze_scenario(SCENARIO_CORAL_CRESCENT, filter_coral_crescent)
    # analyze_build("iron tool", filter_coral_crescent, given={"bread"})
    analyze_scenario(SCENARIO_CORAL_HAVEN)


if __name__ == "__main__":
    main()
