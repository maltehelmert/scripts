#! /usr/bin/env python3
# -*- coding: utf-8 -*-

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


def coal_to_plastic(coal_for_liquefaction, print=print):
    refinery_prod = F(13, 10)
    chem_plant_prod = F(13, 10)

    coal_for_liquefaction = F(coal_for_liquefaction)
    oil_refineries = coal_for_liquefaction / 2
    steam = oil_refineries * 10
    heavy_oil_from_liquefaction = oil_refineries * (18 - 5) * refinery_prod
    light_oil_from_liquefaction = oil_refineries * 4 * refinery_prod
    petroleum_gas_from_liquefaction = oil_refineries * 2 * refinery_prod
    print(f"{oil_refineries:8.3f} oil refineries for liquefaction")
    print(f"{coal_for_liquefaction:8.3f} coal for liquefaction")
    print(f"{steam:8.3f} steam for liquefaction")
    print(f"{heavy_oil_from_liquefaction:8.3f} heavy oil from liquefaction")
    print(f"{light_oil_from_liquefaction:8.3f} light oil from liquefaction")
    print(f"{petroleum_gas_from_liquefaction:8.3f} petroleum gas from liquefaction")
    #
    print()
    water_for_steam = steam
    offshore_pumps_for_steam = water_for_steam / 1200
    boilers = steam / 60
    solid_fuel_for_boilers = boilers * 3 / 20
    print(f"{water_for_steam:8.3f} water for steam")
    print(f"{offshore_pumps_for_steam:8.3f} offshore pumps for steam")
    print(f"{boilers:8.3f} boilers")
    print(f"{solid_fuel_for_boilers:8.3f} solid fuel for boilers")
    #
    print()
    chemical_plants_for_solid_fuel = solid_fuel_for_boilers * 2 / chem_plant_prod
    light_oil_for_solid_fuel = chemical_plants_for_solid_fuel * 5
    print(f"{chemical_plants_for_solid_fuel:8.3f} chemical plants for solid fuel")
    print(f"{light_oil_for_solid_fuel:8.3f} light oil for solid fuel")
    light_oil_balance = light_oil_from_liquefaction - light_oil_for_solid_fuel
    print(f"{light_oil_balance:8.3f} light oil balance")
    #
    print()
    print(f"{heavy_oil_from_liquefaction:8.3f} heavy oil before cracking")
    print(f"{light_oil_balance:8.3f} light oil before cracking")
    print(f"{petroleum_gas_from_liquefaction:8.3f} petroleum gas before cracking")
    #
    chemical_plants_for_heavy_oil_cracking = heavy_oil_from_liquefaction / 20
    water_for_heavy_oil_cracking = chemical_plants_for_heavy_oil_cracking * 15
    offshore_pumps_for_heavy_oil_cracking = water_for_heavy_oil_cracking / 1200
    light_oil_from_heavy_oil_cracking = chemical_plants_for_heavy_oil_cracking * 15 * chem_plant_prod
    print()
    print(f"{chemical_plants_for_heavy_oil_cracking:8.3f} chemical plants for heavy oil cracking")
    print(f"{water_for_heavy_oil_cracking:8.3f} water for heavy oil cracking")
    print(f"{offshore_pumps_for_heavy_oil_cracking:8.3f} offshore pumps for heavy oil cracking")
    print(f"{light_oil_from_heavy_oil_cracking:8.3f} light oil from heavy oil cracking")
    light_oil_after_heavy_oil_cracking = light_oil_balance + light_oil_from_heavy_oil_cracking
    print(f"{light_oil_after_heavy_oil_cracking:8.3f} light oil after heavy oil cracking")
    #
    chemical_plants_for_light_oil_cracking = light_oil_after_heavy_oil_cracking / 15
    water_for_light_oil_cracking = chemical_plants_for_light_oil_cracking * 15
    offshore_pumps_for_light_oil_cracking = water_for_light_oil_cracking / 1200
    petroleum_gas_from_light_oil_cracking = chemical_plants_for_light_oil_cracking * 10 * chem_plant_prod
    print()
    print(f"{chemical_plants_for_light_oil_cracking:8.3f} chemical plants for light oil cracking")
    print(f"{water_for_light_oil_cracking:8.3f} water for light oil cracking")
    print(f"{offshore_pumps_for_light_oil_cracking:8.3f} offshore pumps for light oil cracking")
    print(f"{petroleum_gas_from_light_oil_cracking:8.3f} petroleum gas from light oil cracking")
    petroleum_gas_after_light_oil_cracking = petroleum_gas_from_liquefaction + petroleum_gas_from_light_oil_cracking
    print(f"{petroleum_gas_after_light_oil_cracking:8.3f} petroleum gas after light oil cracking")
    print()
    water_total = water_for_steam + water_for_heavy_oil_cracking + water_for_light_oil_cracking
    print(f"{water_total:8.3f} water total")
    print()
    chemical_plants_for_plastic = petroleum_gas_after_light_oil_cracking / 20
    coal_for_plastic = chemical_plants_for_plastic
    plastic = chemical_plants_for_plastic * 2 * chem_plant_prod
    print(f"{chemical_plants_for_plastic:8.3f} chemical plants for plastic")
    print(f"{coal_for_plastic:8.3f} coal for plastic")
    print(f"{plastic:8.3f} plastic")
    coal_total = coal_for_liquefaction + coal_for_plastic
    print(f"{coal_total:8.3f} coal total")
    coal_for_liquefaction_ratio = coal_for_liquefaction / coal_total
    return coal_for_liquefaction_ratio


def get_coal_for_liquefaction_ratio():
    return coal_to_plastic(1, print=lambda *args, **kwards: None)


COAL_FOR_LIQUEFACTION_RATIO = get_coal_for_liquefaction_ratio()

def main():
    coal_to_plastic(coal_for_liquefaction=180)
    # coal_to_plastic(coal_for_liquefaction=180 * COAL_FOR_LIQUEFACTION_RATIO)


if __name__ == "__main__":
    main()
