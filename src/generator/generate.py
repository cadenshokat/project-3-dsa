import random
from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent.parent / "datasets"


def generate_random_large_range(
    n: int = 100_000,
    min_val: int = 1,
    max_val: int = 1000,
    filename: str = "random.txt",
    seed: int | None = None,
) -> Path:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    path = DATASETS_DIR / filename

    rng = random.Random(seed) if seed is not None else random

    with path.open("w") as f:
        for _ in range(n):
            value = rng.randint(min_val, max_val)
            f.write(f"{value}\n")

    return path

def sort_dataset_file(
    input_filename: str = "random.txt",
    output_filename: str = "sorted.txt",
) -> Path:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    input_path = DATASETS_DIR / input_filename
    output_path = DATASETS_DIR / output_filename

    with input_path.open("r") as f:
        nums = [int(line.strip()) for line in f if line.strip()]

    nums.sort()

    with output_path.open("w") as f:
        for value in nums:
            f.write(f"{value}\n")

    return output_path

def generate_reverse_sorted_dataset(
    input_filename: str = "random.txt",
    output_filename: str = "reversed.txt",
) -> Path:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    input_path = DATASETS_DIR / input_filename
    output_path = DATASETS_DIR / output_filename

    with input_path.open("r") as f:
        nums = [int(line.strip()) for line in f if line.strip()]

    nums.sort(reverse=True)

    with output_path.open("w") as f:
        for value in nums:
            f.write(f"{value}\n")

    return output_path


def generate_almost_sorted_dataset(
    input_filename: str = "random.txt",
    output_filename: str = "almost_sorted.txt",
    noise_fraction: float = 0.10,
    seed: int | None = None
) -> Path:
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    input_path = DATASETS_DIR / input_filename
    output_path = DATASETS_DIR / output_filename

    with input_path.open("r") as f:
        nums = [int(line.strip()) for line in f if line.strip()]

    nums.sort()

    n = len(nums)
    swaps = int(n * noise_fraction)

    rng = random.Random(seed) if seed is not None else random

    for _ in range(swaps):
        i = rng.randrange(n)
        j = rng.randrange(n)
        nums[i], nums[j] = nums[j], nums[i]

    with output_path.open("w") as f:
        for value in nums:
            f.write(f"{value}\n")

    return output_path


if __name__ == "__main__":
    random_path = generate_random_large_range()
    print(f"Generated random dataset at: {random_path}")

    sorted_path = sort_dataset_file()
    print(f"Sorted dataset written to: {sorted_path}")

    reversed_path = generate_reverse_sorted_dataset()
    print(f"Reversed dataset written to: {reversed_path}")

    almost_sorted_path = generate_almost_sorted_dataset()
    print(f"Almost-sorted dataset written to: {almost_sorted_path}")
