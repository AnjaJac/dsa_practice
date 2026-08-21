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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

class Animal:
    """ Base class for all creatures living in the river"""
    # Default strength range: subclass override this to guarantee
    #species-level guardrails
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
    #Bear is always stronger than fish
    STRENGTH_RANGE = (6.0, 10.0)

class Fish(Animal):
    # Fish is always eaten by the bear
    STRENGTH_RANGE = (1.0, 5.0)

# RIver ecosystem
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
            if animal is None or id(animal) in already_moved:
                continue        # cell emptied earlier, or animal
                                # already handeled this round

            already_moved.add(id(animal))

            direction = random.choice([-1, 0, 1])
            j = i + direction
            if direction == 0 or j < 0 or j >= self.size:
                continue

            target = self.cells[j]

            if target is None:
                # Move into an empty cell
                self.cells[j] = animal
                self.cells[i] = None
            elif type(target) is type(animal):
                # Same species collision
                already_moved.add(id(target))
                if target.gender != animal.gender:
                    # Different genders -> reproduce
                    empties = self._empty_indices()
                    if empties:
                        k = random.choice(empties)
                        self.cells[k] = type(animal)()
                else:
                    # Same gender -> stronger survives
                    if animal.strength > target.strength:
                        # Aggressor (attacker) wins
                        self.cells[j] = animal
                        self.cells[i] = None
                    elif target.strength > animal.strength:
                        #Defender wins
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

# Visualization: river state to png
def save_river_image(river, step, filename="river_snapshot.png"):
    """Render the real River object's current cell contents as a colored
    grid: brown for Bear, blue for Fish, white for empty. This reads
    river.cells directly, so the picture always matches whatever the
    simulation actually produced, not a separate reimplementation."""
    n = river.size
    fig, ax = plt.subplots(figsize=(12, 2.2))
    for i, c in enumerate(river.cells):
        if c is None:
            color, label = "#f0f0f0", ""
        elif isinstance(c, Bear):
            color, label = "#8B4513", "B"
        else:
            color, label = "#3B7DD8", "F"
        ax.add_patch(mpatches.Rectangle((i, 0), 1, 1, facecolor=color,
                                         edgecolor="black", linewidth=0.8))
        if label:
            ax.text(i + 0.5, 0.5, label, ha="center", va="center",
                     color="white", fontsize=9, fontweight="bold")
 
    ax.set_xlim(0, n)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.axis("off")
    b, f = river.counts()
    ax.set_title(f"River state after step {step} (n = {n} cells, "
                 f"bears={b}, fish={f})", fontsize=11)
 
    bear_patch = mpatches.Patch(color="#8B4513", label="Bear")
    fish_patch = mpatches.Patch(color="#3B7DD8", label="Fish")
    empty_patch = mpatches.Patch(facecolor="#f0f0f0", edgecolor="black", label="Empty (None)")
    ax.legend(handles=[bear_patch, fish_patch, empty_patch], loc="upper center",
              bbox_to_anchor=(0.5, -0.05), ncol=3, frameon=False)
 
    plt.tight_layout()
    plt.savefig(filename, dpi=150, bbox_inches="tight")
    plt.close(fig)

# Demo/driver code

def run_simulation(river_size=30, num_bears=6, num_fish=10, steps=15,
                    snapshot_step=None, snapshot_file="river_snapshot.png"):
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
        if snapshot_step is not None and step == snapshot_step:
            save_river_image(river, step, snapshot_file)
            print(f" (saved a snapshot image of this step to a {snapshot_file}\n)")
if __name__ == "__main__":
    random.seed(42)     # fixed seed so this run is reproducible run to run
    run_simulation(snapshot_step=4)