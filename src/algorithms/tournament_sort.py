import math

def tourney_sort(array): # takes in an array, outputs the array sorted from smallest to largest
    output = [] # create return array
    n = len(array)
    tree_size = 1
    while tree_size < n:
        tree_size *= 2

    tree = [(float('inf'), float('inf'))] * (tree_size * 2)

    for i in range(n):
        tree[tree_size + i] = (array[i], i)

    for i in range(tree_size - 1, 0, -1):
        tree[i] = min(tree[(i * 2)], tree[(i * 2) + 1])

    for i in range(n):
        winner = tree[1]
        output.append(winner[0])
        j = tree_size + winner[1]

        tree[j] = (float('inf'), float('inf')) # setting values to inf ensures they won't interfere again. any relevant number will always 'win' at being smaller than infinity

        while j > 1:
            j //= 2
            tree[j] = min(tree[j * 2], tree[j * 2 + 1])

    return output
