import random
from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent.parent / "datasets"


def generate_random_large_range(
    n: int = 100_000,
    min_val: int = 1,
    max_val: int = 1000,
    filename: str = "random.txt",
) -> Path:
    """
    Generate a dataset of n random integers in [min_val, max_val]
    and save it under src/datasets/<filename>.

    Returns the Path to the generated file.
    """
    DATASETS_DIR.mkdir(parents=True, exist_ok=True)

    path = DATASETS_DIR / filename

    rng = random.Random(42)

    with path.open("w") as f:
        for _ in range(n):
            value = rng.randint(min_val, max_val)
            f.write(f"{value}\n")

    return path

def sort_dataset_file(
    input_filename: str = "random.txt",
    output_filename: str = "sorted.txt",
) -> Path:
    """
    Read the dataset from src/datasets/<input_filename>,
    sort the numbers, and write them to src/datasets/<output_filename>,
    one number per line.

    Returns the Path to the sorted output file.
    """
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


if __name__ == "__main__":
    random_path = generate_random_large_range()
    print(f"Generated random dataset at: {random_path}")

    sorted_path = sort_dataset_file()
    print(f"Sorted dataset written to: {sorted_path}")
