def quick_sort(values):
    if len(values) <= 1:
        return values

    pivot_index = len(values) // 2
    pivot = values[pivot_index]

    left = []
    middle = []
    right = []

    for v in values:
        if v < pivot:
            left.append(v)
        elif v > pivot:
            right.append(v)
        else:
            middle.append(v)

    return quick_sort(left) + middle + quick_sort(right)


def read_numbers(filename):
    numbers = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            numbers.append(int(line))

    return numbers


def main():
    numbers = read_numbers("../datasets/random.txt")

    sorted_numbers = quick_sort(numbers)
    print("Result:", sorted_numbers)


if __name__ == "__main__":
    main()
