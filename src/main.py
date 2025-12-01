import time
import os
import sys
from pathlib import Path
from algorithms.merge_sort import merge_sort
from algorithms.quick_sort import quick_sort
from algorithms.tournament_sort import tourney_sort

def load_dataset(filename: str) -> list[int]:
    base_dir = Path(__file__).resolve().parent
    datasets_dir = base_dir / "datasets"
    path = datasets_dir / filename

    if not path.exists():
        raise FileNotFoundError(f"Dataset file not found: {path}")

    text = path.read_text().strip()

    tokens = text.splitlines()

    numbers: list[int] = []
    for t in tokens:
        t = t.strip()
        if t:
            numbers.append(int(t))

    return numbers


ALGORITHMS: dict[str, dict] = {
    "1": {
        "name": "Tournament Sort",
        "fn": tourney_sort,
        "complexity": "O(n log n)",
    },
    "2": {
        "name": "Merge Sort",
        "fn": merge_sort,
        "complexity": "O(n log n)",
    },
    "3": {
        "name": "Quick Sort",
        "fn": quick_sort,
        "complexity": "O(n log n) average, O(n^2) worst",
    },
}

DATASETS: dict[str, dict] = {
    "1": {
        "name": "Random",
        "filename": "random.txt",
        "description": "100k numbers in [1, x], fully random",
    },
    "2": {
        "name": "Sorted",
        "filename": "sorted.txt",
        "description": "Start from random, sort ascending",
    },
    "3": {
        "name": "Reverse Sorted",
        "filename": "reversed.txt",
        "description": "Start sorted ascending, then reverse",
    },
    "4": {
        "name": "Almost Sorted",
        "filename": "almost_sorted.txt",
        "description": "Sorted with a small percentage of random swaps",
    },
}

def time_algorithm(algorithm_fn, data: list[int]) -> tuple[list[int], float]:
    arr = data.copy()

    start = time.perf_counter()
    result = algorithm_fn(arr)
    end = time.perf_counter()

    if result is None:
        result = arr

    time_ms = (end - start) * 1000.0
    return result, time_ms

def print_options():
    print("\n")
    for key, info in ALGORITHMS.items():
        print(f"  {key}. {info['name']} ({info['complexity']})")
    print("  4. Open UI (requires pygame - 'pip install pygame')")
    print("  5. Quit\n")

def choose_algorithm() -> str:
    print_options()
    while True:
        choice = input("Select an option or algorithm by number: ").strip()
        if choice == "4":
            os.system('python visuals.py')
            print_options()
        elif choice == "5":
            sys.exit(0)
        elif choice in ALGORITHMS:
            return choice
        else: 
            print("Invalid choice, please try again.")


def choose_dataset() -> str:
    print("\nAvailable Datasets:")
    for key, info in DATASETS.items():
        print(f"  {key}. {info['name']} ({info['description']})")

    while True:
        choice = input("Select a dataset by number: ").strip()
        if choice in DATASETS:
            return choice
        print("Invalid choice, please try again.")


def main():
    print("=== Sorting Algorithm Comparison Tool ===")

    algo_choice = choose_algorithm()
    dataset_choice = choose_dataset()

    algo_info = ALGORITHMS[algo_choice]
    dataset_info = DATASETS[dataset_choice]

    print(f"\nYou selected algorithm: {algo_info['name']}")
    print(f"Complexity: {algo_info['complexity']}")
    print(f"Dataset: {dataset_info['name']} ({dataset_info['filename']})")

    print("\nLoading dataset...")
    numbers = load_dataset(dataset_info["filename"])
    print(f"Loaded {len(numbers)} numbers.")

    print("\nRunning algorithm, please wait...")
    sorted_numbers, time_ms = time_algorithm(algo_info["fn"], numbers)

    is_sorted = all(sorted_numbers[i] <= sorted_numbers[i + 1]
                    for i in range(len(sorted_numbers) - 1))

    print("\n=== Results ===")
    print(f"Algorithm: {algo_info['name']}")
    print(f"Dataset: {dataset_info['name']}")
    print(f"n: {len(numbers)}")
    print(f"Time: {time_ms:.3f} ms")
    print(f"Sorted OK: {is_sorted}")
    print(f"First 10 elements: {sorted_numbers[:10]}")
    print(f"Last 10 elements: {sorted_numbers[-10:]}")


if __name__ == "__main__":
    main()
