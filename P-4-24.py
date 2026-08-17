"""
P-4.24: Solving summation puzzles by enumerationg 
and testing all possible configurations (Multiple recursion, Section 4.4.3)

A summation puzzle assigns a unique digit (0-9) to each distinct letter
appearing in an equation like
    pot + pan = bib

so that the resulting arithmetic is correct. We solve it exactly the way
Code Fragment 4.14 (PuzzleSolve) describes: recursively build up a 
k-length sequence S of digit assignments (one digit per distinct letter),
drawn without repetition from the universe U = {0, 1, ..., 9}, and test each 
complete assignment for correctness.

We solve the three puzzles from Section 4.4.3:
    pot + pan = bib
    dog + cat = pig
    boy + girl = baby
"""

import time

# Recursive solver - code fragment 4.14 (PuzzleSolver)

def puzzle_solver(word1, word2, word3):
    """
    Solves a summation puzzle of the form word1 + word2 == word3.

    Returns(assignment, letters) where:
         - assignment is a dict mapping each distinct letter to a digit
         0-9, or None if no solution exists
         - letters is the list of distinct letters, in the order they were
         assigned (i.e., the order corresponding to position is S)
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

    solution = {"assignment": None} # mutable box so the recursion can write into it and short-circuit

    def word_value(word, assignment):
        value = 0
        for ch in word:
            value = value * 10 + assignment[ch]
        return value
    def is_solution(assignment):
        return word_value(word1, assignment) + word_value(word2, assignment)\
        == word_value(word3, assignment)

    def puzzle_solve(k, S, U):
        """
        Enumerate all k-length extensions of S using elements of U,
        without repetition, exactly as in Code Fragment 4.14.
        """
        if solution["assignment"] is not None:
            return                              # a solution was already found

        current_letter = letters[len(S)]        # the letter this call assigns
        for e in sorted(U):
            # Prune: a leading letter can never be assigned the digit 0.
            if e == 0 and current_letter in leading_letters:
                continue

            S.append(e)             # add e to the end of S
            U.remove(e)             # e is now being used

            if k == 1:
                assignment = dict(zip(letters, S))
                if is_solution(assignment):
                    solution["assignment"] = assignment
            else:
                puzzle_solve(k-1, S, U)
            S.pop()                 # remove e from the end of S
            U.add(e)                # e is now considered unused

            if solution["assignment"] is not None:
                return              # stop enumerating once solved
    puzzle_solve(len(letters), [], set(range(10)))
    return solution["assignment"], letters

# Driver: Solve three puzzles form Section 4.4.3

def show_puzzle(word1, word2, word3):
    print(f"{word1} + {word2} = {word3}")
    start = time.perf_counter()
    assignment, letters = puzzle_solver(word1, word2, word3)
    elapsed = time.perf_counter() - start

    if assignment is None:
        print("No solution found!")
    else:
        mapping = ", ".join(f"{ch}={assignment[ch]}" for ch in letters)
        print(f"  Digits: {mapping}")

        def value(word):
            v = 0
            for ch in word:
                v = v * 10 + assignment[ch]
            return v

        v1, v2, v3 = value(word1), value(word2), value(word3)
        print(f" Check : {v1} + {v2} = {v3} ({'correct if v1 + v2 == v3 else WRONG'})")

    print(f"Solved in {elapsed: .3f}s\n")

if __name__ == "__main__":
    show_puzzle("pot", "pan", "bib")
    show_puzzle("dog", "cat", "pig")
    show_puzzle("boy", "girl", "baby")
