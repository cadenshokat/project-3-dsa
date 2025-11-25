def merge_sort(values):
    # If a sub-array is too small to sort then just return the value
    if len(values) <= 1:
        return values

    middle = len(values) // 2
    left_half = values[:middle]
    right_half = values[middle:]

    left_sorted = merge_sort(left_half)
    right_sorted = merge_sort(right_half)

    return merge(left_sorted, right_sorted)


def merge(left_array, right_array):
    merged = []

    left_pos = 0
    right_pos = 0

    # Sort into a merged array by comparing values from the two sub-arrays
    while left_pos < len(left_array) and right_pos < len(right_array):
        left = left_array[left_pos]
        right = right_array[right_pos]

        if left <= right:
            merged.append(left)
            left_pos += 1
        else:
            merged.append(right)
            right_pos += 1

    # Add the rest of the values that haven't already been compared
    if left_pos < len(left_array):
        merged.extend(left_array[left_pos:])

    if right_pos < len(right_array):
        merged.extend(right_array[right_pos:])

    return merged


def read_numbers(filename):
    numbers = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            numbers.append(int(line))

    return numbers


def main():
    numbers = read_numbers("../datasets/random.txt")

    sorted_numbers = merge_sort(numbers)
    print("Result:", sorted_numbers)

if __name__ == "__main__":
    main()