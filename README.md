# DSA Project Problems

This folder holds a set of data structures and algorithms practice assignments, written in Python. Each file is a separate assignment, named after the problem number from the textbook (for example P-2.37 or P-6.36). The sections below explain each one and give the exact command to run it.

## Setup

This project uses Python 3.12.4 (see `.python-version`). A local virtual environment folder, `dsa_env`, is set up but not tracked in git.

Before running anything, install the one outside package this project needs: matplotlib. It is used by the timing chart assignment and the maze assignment.

```
pip install matplotlib
```

Or, using the requirements file in this folder:

```
pip install -r requirements.txt
```

The other assignments (P-2.37, P-4.24, P-6.36) only use the Python standard library, so no extra install is needed for those.

## P-2.37: Bear/Fish River Simulation

File: `P-2-37.py`

This program simulates a river of cells that hold bears, fish, or nothing. On each time step, every animal tries to move one step left, right, or stay in place. The rules work like this:

- A bear moving onto a fish kills the fish and takes its spot.
- A fish moving onto a bear dies.
- Two animals of the same species and the same gender fight: the one with more strength survives and takes the spot, the loser disappears.
- Two animals of the same species but different gender both stay in place, and a new animal of that species is born in a random empty cell.

The program prints the state of the river and the bear and fish counts after each step.

Run it with:

```
python3 P-2-37.py
```

## P-3.55: Timing prefix_average1, prefix_average2, prefix_average3

File: `P-3-55.py`

This program compares three ways of computing prefix averages of a list of numbers: `prefix_average1` (a nested loop, quadratic time), `prefix_average2` (a loop with `sum()` and slicing, still quadratic time), and `prefix_average3` (a single loop with a running total, linear time). It times each one on lists of growing size, prints a table of the results, and saves a chart of running time versus input size to `prefix_average_timing.png`. Because the chart uses a log scale on both axes, the quadratic methods should look like steeper lines than the linear one.

Run it with:

```
python3 P-3-55.py
```

## P-4.24: Solving Summation Puzzles

File: `P-4-24.py`

This program solves summation puzzles such as `pot + pan = bib`, where each letter stands for a digit from 0 to 9 and no two letters share a digit. It tries every possible digit assignment by recursion until it finds one that makes the sum correct, skipping any assignment that would put a 0 at the start of a number. It solves three puzzles in a row and prints the digit for each letter, along with the time it took to solve each one.

Run it with:

```
python3 P-4-24.py
```

## P-6.36: FIFO Capital Gain Calculator

File: `P-6-36.py`

This program reads stock transactions from standard input, one per line, in the form `buy x shares at $y each` or `sell x shares at $y each`. It uses a first in, first out rule: when shares are sold, the oldest shares bought are the ones counted as sold. It keeps track of share lots in a queue that the program builds by hand (not Python's built in deque), and prints the total capital gain or loss at the end.

To run it and type transactions by hand, use:

```
python3 P-6-36.py
```

Then type each transaction line, and press Ctrl-D on its own line when you are done, to signal the end of input.

To run it against one of the test files in this folder instead, redirect the file into the program:

```
python3 P-6-36.py < transactions.txt
```

### Transaction test files

Each of these files feeds a different case into P-6.36. Run each one with the same pattern: `python3 P-6-36.py < filename.txt`.

**transactions.txt**
Command: `python3 P-6-36.py < transactions.txt`
Checks: a normal mixed case, where one sell pulls shares from more than one buy lot at different prices.
Expected result: `Total capital gain: $940.00`

**transactions1.txt**
Command: `python3 P-6-36.py < transactions1.txt`
Checks: a plain loss, selling all shares below the price they were bought at.
Expected result: `Total capital loss: $2,000.00`

**transactions2.txt**
Command: `python3 P-6-36.py < transactions2.txt`
Checks: two separate buy lots at the exact same price, sold together in one sell. This makes sure the two lots are still treated as separate queue entries and not merged.
Expected result: `Total capital gain: $0.00`

**transactions3.txt**
Command: `python3 P-6-36.py < transactions3.txt`
Checks: a sell that uses up the exact number of shares held, across two lots, so the queue becomes completely empty at the end.
Expected result: `Total capital gain: $970.00`

**transactions4.txt**
Command: `python3 P-6-36.py < transactions4.txt`
Checks: the queue emptying out fully after one buy and sell pair, then being used again for a second, separate buy and sell pair.
Expected result: `Total capital gain: $225.00`

**transactions5.txt**
Command: `python3 P-6-36.py < transactions5.txt`
Checks: a longer, mixed sequence of buys and sells, where sells often span more than one lot and lots are left over at the end.
Expected result: `Total capital gain: $1,530.00`

**overselling6.txt**
Command: `python3 P-6-36.py < overselling6.txt`
Checks: trying to sell more shares than have been bought so far.
Expected result: the program stops with an error. It raises `ValueError: Trying to sell more shares than have been bought.` and prints a traceback. This is the correct, expected behavior for this file, not a bug.

**messyformat7.txt**
Command: `python3 P-6-36.py < messyformat7.txt`
Checks: messy but still valid input: mixed capital and lowercase words (`Buy`, `SELL`), extra spaces between words, the singular word `share` instead of `shares`, and blank lines mixed in between transactions.
Expected result: `Total capital loss: $240.00`

## P-14.80: Maze Generation and Solving

File: `P-14-80.py`

This program builds a maze inside an n by n grid of cells. It gives every wall between two neighbor cells a random weight, then finds a minimum spanning tree of the resulting graph using Jarnik-Prim's algorithm. Every wall that is part of that tree gets removed, which carves out the maze and guarantees there is exactly one path between any two cells. It then solves the maze from the top left cell to the bottom right cell using a breadth first search, and saves a picture of the maze with the solution path drawn in red.

The file `mymaze.png` in this folder is an example output from this program, showing a 20 by 20 maze with its solution path.

Command line options:

- `-n`: the size of the grid, as a number of cells per side. The maze will be `n` by `n` cells. Default is 15.
- `--seed`: a whole number used to seed the random generator. Using the same seed with the same `-n` value always produces the same maze. Leave it out to get a different maze each time.
- `-o` or `--output`: the file name to save the maze picture to. Default is `maze.png`.

Example command, making a 20 by 20 maze with a fixed seed, saved to `mymaze.png`:

```
python3 P-14-80.py -n 20 --seed 42 -o mymaze.png
```

Run with defaults:

```
python3 P-14-80.py
```

## Common Problems

- If you run `python3 P-6-36.py` with no file redirected into it, the program waits for you to type transaction lines. Press Ctrl-D on its own line (Ctrl-Z then Enter on Windows) to end input. If nothing happens after you run the command, this is likely why.
- If `matplotlib` is not installed, `P-3-55.py` and `P-14-80.py` will fail with an import error. Run `pip install matplotlib` first.
- Running P-6.36 on `overselling6.txt` is supposed to crash with a `ValueError`. That is the test working as intended, not a broken program.
- If you use `python` instead of `python3` and get a "command not found" error, try `python3` instead, or check that your virtual environment is active.
- Running `P-14-80.py` without `--seed` gives a different maze layout every time, so your picture will not match `mymaze.png` exactly. Pass the same `--seed` value to get the same maze again.
