from collections import namedtuple
import sys

Item = namedtuple("Item", ['index', 'value', 'weight'])


def greedy1(items, capacity):
    value = 0
    weight = 0
    taken = [0]*len(items)
    
    items = sorted(items, key=lambda item: item[1], reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    return value, taken

def greedy2(items, capacity):
    value = 0
    weight = 0
    taken = [0]*len(items)

    items = sorted(items, key=lambda item: item[2], reverse=False)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    return value, taken

def greedy3(items, capacity):
    value = 0
    weight = 0
    taken = [0]*len(items)

    items = sorted(items, key=lambda item: item[1]/item[2], reverse=True)

    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
    
    return value, taken

def dynamic_programming(items, capacity):
    n = len(items)
    K = [[0 for _ in range(capacity + 1)] for _ in range(n+1)]
    taken = [0]*n
    
    for i in range(n + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                K[i][w] = 0
            elif items[i-1].weight <= w:
                K[i][w] = max(items[i-1].value + K[i-1][w-items[i-1].weight], K[i-1][w])
            else:
                K[i][w] = K[i-1][w] 
    res = K[n][w]
    w = capacity
    for i in range(n, 0, -1):
        if res <= 0:
            break
        if res == K[i-1][w]:
            continue
        else:
            taken[i-1] = 1
            res = res - items[i-1].value
            w = w - items[i-1].weight

    return K[n][capacity], taken

def branch_and_bound(items, capacity):
    pass

def solve(input_data, func):
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value, taken = func(items, capacity)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    func_mapping = {'greedy1': greedy1, 'greedy2': greedy2, 'greedy3': greedy3,
        'dp':dynamic_programming}
    funcs = ['greedy1', 'greedy2', 'greedy3', 'dp']
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        
        for func in funcs: 
            print(solve(input_data, func_mapping[func]))
    else:
        print('This test requires an input file. Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0')
