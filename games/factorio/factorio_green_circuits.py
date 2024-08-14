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


def green_circuits(target):
    prod = F(14, 10)
    green_circuits = target
    green_circuits_production_cycles = target / prod
    iron_plates = green_circuits_production_cycles
    copper_cables = green_circuits_production_cycles * 3
    green_circuits_production = green_circuits_production_cycles / 2
    print(f"{green_circuits:8.3f} green circuits")
    print(f"{iron_plates:8.3f} iron plates for green circuits")
    print(f"{copper_cables:8.3f} copper cables for green circuits")
    copper_plates = copper_cables / 2 / prod
    print(f"{copper_plates:8.3f} copper plates for copper cables")
    copper_cables_production = copper_cables / 4
    print(f"{green_circuits_production:8.3f} green circuits production")
    print(f"{copper_cables_production:8.3f} copper cables production")


def main():
    green_circuits(target=45)


if __name__ == "__main__":
    main()
