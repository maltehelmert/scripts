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
    target: list
    duration: int

    def get_cycles_per_minute(self):
        return F(60, self.duration)

    def get_production_per_minute(self):
        amount_per_cycle, resource = self.target
        amount_per_minute = amount_per_cycle * self.get_cycles_per_minute()
        return amount_per_minute, resource


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

    def get_building(self):
        sources = [(self.number_of_houses, resource)
                   for resource in self.required_resources]
        duration = self.get_cycle_time()
        return Building(
            name=self.name,
            sources=sources,
            target=(1, self.get_virtual_resource()),
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
    sources, target = text.split("->")
    sources = parse_ingredients(sources.strip())
    target = parse_ingredient(target.strip())
    return sources, target


def parse_building(name, recipe_text, duration):
    sources, target = parse_recipe(recipe_text)
    return Building(name, sources, target, duration)


def filter_buildings(removed):
    return [building for building in BUILDINGS
            if building.name not in removed]


def get_buildings_default():
    return filter_buildings({
        "water pump",
        "sea water filter",
        "charcoal maker",
        "wood factory",
        "stone mine",
        "coal mine",
        "iron mine",
        })


def get_buildings_eden_isle():
    return get_buildings_default()


def get_buildings_crystal_cove():
    return get_buildings_default()


def get_buildings_harbor_islands():
    return get_buildings_default()


def get_buildings_coral_crescent():
    traders = [
        parse_building("trader A (apple)", "-> 1 apple", 2),
        parse_building("trader B (stone -> lumber)", "1 stone -> 1 lumber", 2),
        parse_building("trader C (stone tool -> cow)", "1 stone tool -> 1 cow", 2),
        parse_building("trader D (juice -> wheat)", "1 juice -> 1 wheat", 2),
    ]

    return traders + filter_buildings({
        "water well",
        "water pump",
        "sea water filter",
        "apple farm",
        "wheat farm",
        "cow farm",
        "lumber camp",
        "forester",
        "wood factory",
        "charcoal maker",
        "stone mine",
        "coal mine",
        "iron mine",
        })


def get_buildings_coral_haven():
    return filter_buildings({
        "water pump",
        "sea water filter",
        "charcoal maker",
        "wood factory",
        "stone mine",
        "coal mine",
        "iron quarry",
        })


def get_buildings_pearl_island():
    return get_buildings_default()


def get_buildings_dolphin_islands():
    return filter_buildings({
        "water pump",
        "sea water filter",
        "wood factory",
        "stone mine",
        "coal quarry",
        "coal mine",
        "iron mine",
        })


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
    parse_building("steel tool maker", "1 steel bar, 1 iron tool -> 2 steel tool", 15),
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
    parse_building("steel smelter", "1 coal, 1 iron bar -> 1 steel bar", 20),
    parse_building("library", "1 leather, 1 paper, 1 steel tool -> 2 book", 25),
    #
    CityCenter(
        name="city center I",
        number_of_houses=10,
        required_resources=["water", "apple", "wood furniture"],
        consumption_time_per_resource=50,
        # The game says 50 seconds. It may be worth measuring this.
    ).get_building(),
    CityCenter(
        name="city center II",
        number_of_houses=15,
        required_resources=["juice", "bread", "paper", "leather furniture"],
        consumption_time_per_resource=50,
        # The game says 50 seconds. It may be worth measuring this.
    ).get_building(),
    CityCenter(
        name="city center III",
        number_of_houses=20,
        required_resources=["milk", "sandwich", "book", "luxury furniture"],
        consumption_time_per_resource=60,
        # The game says 60 seconds. It may be worth measuring this.
    ).get_building(),
    CityCenter(
        name="native village center I",
        number_of_houses=10,
        required_resources=["apple", "stone tool"],
        consumption_time_per_resource=50,
        # Time is an estimate.
    ).get_building(),
    CityCenter(
        name="native village center II",
        number_of_houses=15,
        required_resources=["plank", "iron tool", "leather"],
        consumption_time_per_resource=55,
        # I measured 55-60 seconds; the game does not tell us.
    ).get_building(),
]


def add_to_tally(target, source):
    for key, value in source.items():
        target[key] += value


def get_index(buildings):
    # TODO: Change way this is called, with filters etc.?
    building_index = {}
    producer_index = {}
    for building in buildings:
        _, resource_produced = building.target
        if resource_produced in producer_index:
            existing = producer_index[resource_produced]
            print(f"skipping {building.name} in favour of {existing.name}")
        else:
            producer_index[resource_produced] = building
        building_index[building.name] = building
    return building_index, producer_index


def get_requirements(amount, resource, producer_index, given):
    ingredients = defaultdict(int)
    buildings = defaultdict(int)
    if resource in given:
        ingredients[f"{resource} [given]"] += amount
    else:
        ingredients[resource] += amount
        #
        producer = producer_index[resource]
        amount_produced, item_produced = producer.target
        assert item_produced == resource
        #
        num_production_cycles = F(amount, amount_produced)
        work_needed = producer.duration * num_production_cycles
        num_buildings = work_needed / 60
        #
        buildings[producer.name] += num_buildings
        for needed_per_cycle, ingredient in producer.sources:
            needed = num_production_cycles * needed_per_cycle
            rec_ingredients, rec_buildings = get_requirements(needed, ingredient, producer_index, given)
            add_to_tally(ingredients, rec_ingredients)
            add_to_tally(buildings, rec_buildings)
    return ingredients, buildings


def print_buildings():
    for building in BUILDINGS:
        print(building)


def print_tally(tally, indent=""):
    for element, amount in tally.items():
        print(f"{indent}{amount:8.3f} {element} [exact: {amount.numerator}/{amount.denominator}]")


def get_needs(build, building_index, producer_index):
    needs_list = []
    for amount, kind in parse_ingredients(build):
        if kind in building_index:
            building = building_index[kind]
            per_building, resource = building.get_production_per_minute()
            needs_list.append((amount * per_building, resource))
        elif kind in producer_index:
            needs_list.append((amount, kind))
        else:
            raise ValueError(kind)
    return needs_list


def analyze_build(build, buildings, given=set()):
    print(f"analyzing build for {build}...")
    if given:
        print(f"assuming as given resources: {', '.join(sorted(given))}")

    building_index, producer_index = get_index(buildings)
    needs_list = get_needs(build, building_index, producer_index)

    total_ingredients = defaultdict(int)
    total_buildings = defaultdict(int)
    for amount, need in needs_list:
        ingredient_tally, building_tally = get_requirements(amount, need, producer_index, given)
        add_to_tally(total_ingredients, ingredient_tally)
        add_to_tally(total_buildings, building_tally)
    print("ingredients production per minute:")
    print_tally(total_ingredients, "  ")
    print("buildings needed:")
    print_tally(total_buildings, "  ")


def production_time(tile_fraction, base_time):
    # This multiplier has been determined empirically based on the
    # production times shown in the game.

    # The times shown in the game are whole numbers instead of the
    # fractional values shown here. The computed numbers match the numbers
    # shown in the game if we mangle the fractional values as follows:
    #
    # - First, round to one decimal digit.
    # - Then, round to the nearest integer, breaking ties in favour
    #   of even numbers.
    #
    # In Python, this corresponts to x -> round(round(x, 1)).
    #
    # For example, 3.47 and 3.53 are mapped to 4 (to 3.5, then 4),
    # and 4.47 and 4.53 are also mapped to 4 (to 4.5, then 4).
    #
    # The weird intermediate step of rounding to one decimal digit only
    # makes a difference for wheat farms; for the other buildings, we
    # never get a value where it makes a difference. Hence we call this
    # transformation `wheat_adjustment`.
    #
    # A possible explanation is that the games uses 10 ticks per
    # second and therefore internally rounds to one decimal digit for
    # the exact values, and then the further rounding is for display
    # purposes only.
    #
    # In contrast to this, the *efficiency percentages* shown in the
    # game are truncated, not rounded. Exception: For cow farms, 26 of
    # the 50 values shown are actually 1% less than we would expect,
    # but this can be explained by floating point precision issues, as
    # all of these are exact percentages, and if the game interally gets,
    # say, 95.999% instead of the correct 96%, this would truncate to 95%.

    # All numbers were verified against the values in the game for the
    # following buildings:
    #
    # 6 tiles: (one type of) quarry
    # 9 tiles: water well, (one type of) mine, sea water filter
    # 16 tiles: water pump
    # 35 tiles (out of 39 available): sand collector
    # 35 tiles (out of 42 available): apple farm
    # 50 tiles (out of 71 available): cow farm
    # 95 tiles (out of 112 available): wheat farm

    # I experimentally confirmed that the production times are
    # definitely fractional, but I couldn't resolve if there is some
    # form of rounding to frames or not. The production rate of a 55%
    # water well was calculated as 19.44s and measured as somewhere
    # between 19.40s and 19.44s (roughly 19.42s) in an experiment
    # timing it against a 100% water well running for ~75 minutes on
    # triple speed.

    multiplier = (1 - tile_fraction) * 4 + 1
    return base_time * multiplier


def print_production_stats(name, max_tiles, base_time, num_produced):
    print(f"production stats for {name}:")
    for num_tiles in reversed(range(1, max_tiles + 1)):
        percent = int(num_tiles / max_tiles * 100)
        time = production_time(num_tiles / max_tiles, base_time)
        upm = num_produced * (60 / time)
        upmt = upm / num_tiles
        unit = "unit" if num_produced == 1 else "units"
        tiles_width = len(str(max_tiles))
        print(f"{num_tiles:{tiles_width}}/{max_tiles} tiles = {percent:3d}%:", end=" ")
        print(f"{num_produced} {unit} per {time:5.2f}s,", end=" ")
        print(f"{upm:5.3f} UPM, {upmt:5.3f} UPM/tile")
        if round(round(time, 1)) != round(time):
            # I just put this here to verify the point that this rounding step
            # only makes a difference for wheat farms.
            # There is no game logic reason why this should be the case, so if this fails
            # in the future, this does not imply the calculation is wrong.
            assert name == "wheat farm", name


def print_all_production_stats():
    print_production_stats("water well", 9, 7, 1)
    print()
    print_production_stats("quarry", 6, 20, 2)
    print()
    print_production_stats("mine", 9, 10, 3)
    print()
    print_production_stats("sea water filter", 9, 20, 2)
    print()
    print_production_stats("water pump", 16, 5, 3)
    print()
    print_production_stats("sand collector", 35, 20, 1)
    print()
    print_production_stats("apple farm", 35, 10, 2)
    print()
    print_production_stats("cow farm", 50, 15, 2)
    print()
    print_production_stats("wheat farm", 95, 10, 2)
    print()


def main():
    if False:
        analyze_build("1 native village center I", get_buildings_eden_isle())
        analyze_build("2 city center II", get_buildings_crystal_cove())
        analyze_build("2 city center II, 1 native village center II", get_buildings_harbor_islands())
        analyze_build("3 city center II", get_buildings_coral_crescent())
        analyze_build("2 city center III", get_buildings_coral_haven())
        analyze_build("2 city center II, 1 native village center I, 1 native village center II",
                      get_buildings_pearl_island())
        analyze_build("3 city center III", get_buildings_dolphin_islands())

    if False:
        print_all_production_stats()

    if False:
        print_production_stats("water well", 9, 7, 1)


    analyze_build("3 city center III",
                  get_buildings_dolphin_islands(),
                  given={"bread", "cow", "coal",
                         "stone tool", "juice", "lumber",
                         "iron tool", "steel tool",
                         "sandwich", "diamond", "milk",
                         "book", "luxury furniture",
                         })


if __name__ == "__main__":
    main()
