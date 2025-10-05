# -*- coding: utf-8 -*-

from fractions import Fraction

from recipes import Recipe


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
