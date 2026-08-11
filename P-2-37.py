"""
P-2.37: Bear/Fish River Ecosystem Simulation
(with gender and strength)

This program extends the basic bear/fish river simulation
from P-2.36 to having a base class Animal with a Boolean gender field,
and a floating-point strength field.

Rules for one time step:
    - Each animal attempts to move to an adjacent cell (left, right, or stay).
    - If it moves into an empty (None) cell, it simply moves there.
        Terminology: 
            - animal attempting to move is the "aggressor";
            - animal already sitting in the destination cell 
            is "defender"
        The assignment doesn't fully spell out where the survivor
        ends up, so using common-sense convention that a winner earned
        by attacking takes the loser's spot, while a winner who
        successfully defended simply stays in the same spot (holds
        its ground).
    - Different species (Bear vs. Fish):
         * Bear is the aggressor -> fish dies, bear moves into that cell.
         * Fish aggressor (unfortunate termin for ths case) -> fish dies
         (it swam into a predator)
    - Same species, different gender -> both stays into its own respective place
    -> new animal of that species is created in a random empty (previously None)
    cell in the river.
    - Same species, same gender -> only animal with the larger strength
    value survives:
        * aggressor wins: moves into defender's cell;
        * defender wins: stays in its current cell - the aggressor 
        simpy disappears.
    - Fish always has a lower strength then the Bear.
"""
import random

class Animal:
    """ Base class for all creatures living in the river"""
    STRENGTH_RANGE = (1.0, 10.0)

    def __init__(self, gender=None, strength=None):
        self.gender = gender if gender is not None else random.choice([True, False])
        low, high = self.STRENGTH_RANGE
        self.strength = (
            strength if strength is not None else round(random.uniform(low, high), 2)
        )

    def __repr__(self):
        g = "M" if self.gender else "F"
        return f"{self.__class__.__name__[0]}({g},{self.strength: .1f})"

class Bear(Animal):
    STRENGTH_RANGE = (6.0, 10.0)

class Fish(Animal):
    STRENGTH_RANGE = (1.0, 5.0)


class River:
    def __init__(self, size, num_bears, num_fish):
        self.size = size
        self.cells = [None] * size
        self._populate(Bear, num_bears)
        self._populate(Fish, num_fish)

    def _populate(self, species, count):
        empty = [i for i in range(self.size) if self.cells[i] is None]
        random.shuffle(empty)
        for i in empty[:count]:
            self.cells[i] = species()

    def _empty_indices(self):
        return [i for i in range(self.size) if self.cells[i] is None]

    def time_step(self):
        """Advance the simulation by a single time step, in place."""
        order = [i for i in range(self.size) if self.cells[i] is not None]
        random.shuffle(order)
        already_moved = set()

        for i in order:
            animal = self.cells[i]
            if animal is None or id(animal) is already_moved:
                continue

            already_moved.add(id(animal))

            direction = random.choice([-1, 0, 1])
            j = i * direction
            if direction == 0 or j < 0 or j >= self.size:
                continue

            target = self.cells[j]

            if target is None:
                self.cells[j] = animal
                self.cells[i] = None
            elif type(target) is type(animal):
                already_moved.add(id(target))
                if target.gender != animal.gender:
                    empties = self._empty_indices()
                    if empties:
                        k = random.choice(empties)
                        self.cells[k] = type(animal)()
                else:
                    if animal.strength > target.strength:
                        self.cells[j] = animal
                        self.cells[i] = None
                    elif target.strength > animal.strength:
                        self.cells[i] = None
            else:
                if isinstance(animal, Bear) and isinstance(target, Fish):
                    self.cells[j] = animal
                    self.cells[i] = None
                elif isinstance(animal, Fish) and isinstance(target, Bear):
                    self.cells[i] = None

    def counts(self):
        bears = sum( 1 for c in self.cells if isinstance(c, Bear))
        fish = sum(1 for c in self.cells if isinstance(c, Fish))
        return bears, fish

    def __str__(self):
        symbols = []
        for c in self.cells:
            if c is None:
                symbols.append(".")
            else:
                symbols.append(repr(c))
        return " ".join(symbols)

def run_simulation(river_size=30, num_bears=6, num_fish=10, steps=15):
    river = River(river_size, num_bears, num_fish)

    print("Initial state:")
    print(river)
    b, f = river.counts()
    print(f"bears={b}, fish={f}\n")

    for step in range(1, steps + 1):
        river.time_step()
        b, f = river.counts()
        print(f"Step {step: 2d}: bears={b}, fish={f}")
        print(river)
        print()
if __name__ == "__main__":
    run_simulation()