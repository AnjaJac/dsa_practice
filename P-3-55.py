"""
P-3.55: Experimental analysis of prefix_average1, prefix_average2, and prefix_average3
from section 3.3.3 of the book

I am timing all three implementations across a range of input sizes
and plotting their running times on log-log chart. On a log-log plot,
an algorithm that runs in O(n^k) time appears as a roughly a straight line 
with slope k, so I am expecting:
    - prefix_average1 (quadratic, nested loops) -> slope ~2
    - prefix_average2 (quadratic, via sum() + slicing) -> slope ~2
    - prefix_average3 (linear, running total)  -> slope ~1
Running this file directly prints timing table to the console and saves 
a log-log chart to prefix_average_timing.png
"""
import random
import time

import matplotlib
matplotlib.use("Agg") # render to file, no GUI needed
import matplotlib.pyplot as plt

# The three algorithms from the book - logic from the textbook

def prefix_average1(S):
    """Returns a list such that, for all j,
       A[j] equals average of S[0],...,S[j].
    """
    n = len(S)
    A = [0] * n
    for j in range(n):
        total = 0
        for i in range(j + 1):
            total += S[i]
        A[j] = total / (j + 1)
    return A

def prefix_average2(S):
    """
    Returns list such that, for all j,
    A[j] equals average of S[0],...,S[j].
    """
    n = len(S)
    A = [0] * n
    for j in range(n):
        A[j] = sum(S[0:j + 1]) / (j + 1)
    return A

def prefix_average3(S):
    """
    Returns a list such that, for every j,
    A[j] equals to average of S[0],...,S[j].
    """
    n = len(S)
    A = [0] * n
    total = 0
    for j in range(n):
        total += S[j]
        A[j] = total / (j + 1)
    return A

# Timing harness

def time_function(func, S, trials=3):
    """
    Returns the best (minimum) wall-clock time, in seconds, of
    trials calls to func(S). Taking the minimum reduces noise from OS scheduling,
    beckground processes, etc. -- a standard technique for micro-benchmarks.
    """
    best = float("inf")
    for _ in range(trials): # choosing "_" as an iterator is a standard practice when it's used as a mean of going through the loop
        start = time.perf_counter()
        func(S)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best

def run_experiment(sizes, trials=3):
    """
    Times all three algorithms across the given list of input sizes.
    Returns a dictionary: {algorithm_name: [time_for_each_size]}.
    """
    algorithms = {
        "prefix_average1": prefix_average1,
        "prefix_average2": prefix_average2,
        "prefix_average3": prefix_average3,
    }
    results = {name: [] for name in algorithms}
    print(f"{'n':>8} | {'avg1 (s)':>12} | {'avg2 (s)':>12} | {'avg3 (s)':>12}")
    print( "-" * 52)

    for n in sizes:
        S = [random.random() for _ in range(n)]
        row = []
        for name, func in algorithms.items():
            t = time_function(func, S, trials=trials)
            results[name].append(t)
            row.append(t)
        print(f"{n:>8} | {row[0]:>12.6f} | {row[1]:>12.6f} | {row[2]:>12.6f}")
    return results

def plot_results(sizes, results, filename="prefix_average_timing.png"):
    plt.figure(figsize=(8, 6))
    markers = {"prefix_average1": "o", "prefix_average2": "s", "prefix_average3" : "^"}

    for name, times in results.items():
        plt.plot(sizes, times, marker=markers[name], label=name)

    plt.xscale("log")
    plt.yscale("log")
    plt.xlabel("Input size n (log scale)")
    plt.ylabel("Running time in seconds (log scale)")
    plt.title("Running time of prefix_average1/2/3 vs. Input size")
    plt.legend()
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    print(f"\nChart saved to {filename}")


if __name__ == "__main__":
    # Sizes grow geometrically, so points are evenly spaced on a log axis.
    # The quadratic algorithms make very large n impractically slow, so I
    # capped the range accordingly.
    sizes = [50, 100, 200, 400, 800, 1600, 3200, 6400]
    results = run_experiment(sizes, trials=3)
    plot_results(sizes, results)