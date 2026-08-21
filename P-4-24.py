"""
P-4.24: Solving summation puzzles by enumerating and testing all possible
configurations (multiple recursion, Section 4.4.3).

A summation puzzle assigns a unique digit (0-9) to each distinct letter
appearing in an equation like

        pot + pan = bib

so that the resulting arithmetic is correct. We solve it exactly the way
Code Fragment 4.14 (PuzzleSolve) describes: recursively build up a
k-length sequence S of digit assignments (one digit per distinct letter),
drawn without repetition from the universe U = {0, 1, ..., 9}, and test
each complete assignment for correctness.

We solve the three puzzles from Section 4.4.3:
    pot + pan = bib
    dog + cat = pig
    boy + girl = baby

We also measure, with the solver's own node counter, how much the
leading-zero pruning rule (see solve_puzzle below) actually cuts down the
search, and plot the result to prefix a report figure.
"""

import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# The recursive solver (Code Fragment 4.14, PuzzleSolve)
def solve_puzzle(word1, word2, word3, use_pruning=True):
    """Solve a summation puzzle of the form word1 + word2 == word3.

    use_pruning: when True (the default), a leading letter is never
    assigned the digit 0 (the standard convention for these puzzles, and
    not something the assignment states directly -- see the report for
    why I added it). When False, every digit is tried for every letter,
    which lets us measure exactly how much that rule helps.

    Returns (assignment, letters, nodes_visited) where:
        - assignment is a dict mapping each distinct letter to a digit
          0-9, or None if no solution exists
        - letters is the list of distinct letters, in the order they were
          assigned (i.e., the order corresponding to positions in S)
        - nodes_visited is how many times the recursion assigned a digit
          to a letter before stopping (a direct measure of search size)
    """
    letters = sorted(set(word1 + word2 + word3))
    if len(letters) > 10:
        raise ValueError(
            f"Puzzle has {len(letters)} distinct letters; at most 10 digits "
            "are available (0-9), so no valid assignment can exist."
        )

    # Standard convention for these puzzles: a number's leading letter
    # can't be assigned 0 (no numbers with leading zeros, e.g. "0ib").
    leading_letters = {word1[0], word2[0], word3[0]}

    solution = {"assignment": None, "nodes": 0}  # mutable box so the
                                                   # recursion can write
                                                   # into it and short-circuit

    def word_value(word, assignment):
        value = 0
        for ch in word:
            value = value * 10 + assignment[ch]
        return value

    def is_solution(assignment):
        return word_value(word1, assignment) + word_value(word2, assignment) \
            == word_value(word3, assignment)

    def puzzle_solve(k, S, U):
        """Enumerate all k-length extensions of S using elements of U,
        without repetition, exactly as in Code Fragment 4.14."""
        if solution["assignment"] is not None:
            return                      # a solution was already found

        current_letter = letters[len(S)]     # the letter this call assigns
        for e in sorted(U):
            # Prune: a leading letter can never be assigned the digit 0.
            if use_pruning and e == 0 and current_letter in leading_letters:
                continue

            solution["nodes"] += 1      # count this as one search node
            S.append(e)                 # add e to the end of S
            U.remove(e)                 # e is now being used

            if k == 1:
                assignment = dict(zip(letters, S))
                if is_solution(assignment):
                    solution["assignment"] = assignment
            else:
                puzzle_solve(k - 1, S, U)

            S.pop()                     # remove e from the end of S
            U.add(e)                    # e is now considered unused

            if solution["assignment"] is not None:
                return                   # stop enumerating once solved

    puzzle_solve(len(letters), [], set(range(10)))
    return solution["assignment"], letters, solution["nodes"]



# Driver: solve the three puzzles from Section 4.4.3

def show_puzzle(word1, word2, word3):
    print(f"{word1} + {word2} = {word3}")
    start = time.perf_counter()
    assignment, letters, nodes = solve_puzzle(word1, word2, word3)
    elapsed = time.perf_counter() - start

    if assignment is None:
        print("  No solution found.")
    else:
        mapping = ", ".join(f"{ch}={assignment[ch]}" for ch in letters)
        print(f"  Digits:  {mapping}")

        def value(word):
            v = 0
            for ch in word:
                v = v * 10 + assignment[ch]
            return v

        v1, v2, v3 = value(word1), value(word2), value(word3)
        print(f"  Check:   {v1} + {v2} = {v3}  ({'correct' if v1 + v2 == v3 else 'WRONG'})")

    print(f"  Solved in {elapsed:.3f}s, visiting {nodes:,} search nodes\n")



# Measure and plot the effect of the leading-zero pruning rule

def compare_pruning(puzzles, filename="pruning_comparison.png"):
    """For each (word1, word2, word3) puzzle, solve it once with pruning
    and once without, using the solver's own node counter, and plot the
    two search sizes side by side."""
    labels = []
    without_pruning = []
    with_pruning = []

    print("Measuring the effect of leading-zero pruning:")
    for word1, word2, word3 in puzzles:
        _, _, nodes_off = solve_puzzle(word1, word2, word3, use_pruning=False)
        _, _, nodes_on = solve_puzzle(word1, word2, word3, use_pruning=True)
        labels.append(f"{word1}+{word2}={word3}")
        without_pruning.append(nodes_off)
        with_pruning.append(nodes_on)
        print(f"  {word1}+{word2}={word3}: without pruning = {nodes_off:,} nodes, "
              f"with pruning = {nodes_on:,} nodes")

    x = range(len(puzzles))
    width = 0.35
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar([i - width / 2 for i in x], without_pruning, width,
           label="Without leading-zero pruning", color="#d9534f")
    ax.bar([i + width / 2 for i in x], with_pruning, width,
           label="With leading-zero pruning", color="#5cb85c")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Recursive nodes visited until a solution is found")
    ax.set_title("Effect of the leading-zero pruning rule on search size")
    ax.legend()
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"\nChart saved to {filename}")


if __name__ == "__main__":
    puzzles = [("pot", "pan", "bib"), ("dog", "cat", "pig"), ("boy", "girl", "baby")]

    for word1, word2, word3 in puzzles:
        show_puzzle(word1, word2, word3)

    compare_pruning(puzzles)