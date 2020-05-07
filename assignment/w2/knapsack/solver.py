#!/usr/bin/python
# -*- coding: utf-8 -*-
import heapq
from collections import namedtuple
from recordclass import recordclass
from collections import deque

# from branch_and_bound import solve_it_branch_bound_breadth_first
Item = namedtuple("Item", ['index', 'value', 'weight'])
Node = recordclass('Node', 'level value weight items')
PQNode = recordclass('PQNode', 'level value weight bound items')

class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self._queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self._queue)[-1]
    
    def empty(self):
        if (len(self._queue) is 0):
            return True
        else:
            return False
    
    def length(self):
        return len(self._queue)

def branch_and_bound_breadth_first(items, capacity, item_count):
    items = sorted(items, key=lambda Item: Item.weight/Item.value)

    # make a queue to traversing the node
    v = Node(level = -1, value = 0, weight = 0, items = [])
    Q = deque([])
    Q.append(v)

    maxValue = 0
    bestItems = []

    while(len(Q) != 0):
        v = Q[0]

        Q.popleft()
        u = Node(level = None, weight = None, value = None, items = [])
        u.level = v.level + 1
        u.weight = v.weight + items[u.level].weight
        u.value = v.value + items[u.level].value
        u.items = list(v.items)
        u.items.append(items[u.level].index)

        if(u.weight <= capacity and u.value > maxValue):
            maxValue = u.value
            bestItems = u.items
        
        bound_u = bound(u, capacity, item_count, items)

        if (bound_u > maxValue):
            Q.append(u)
        
        u = Node(level = None, weight = None, value = None, items = [])
        u.level = v.level + 1
        u.weight = v.weight
        u.value = v.value
        u.items = list(v.items)

        bound_u = bound(u, capacity, item_count, items)
        if(bound_u > maxValue):
            Q.append(u)
    
    taken = [0]*len(items)
    for i in range(len(bestItems)):
        taken[bestItems[i]] = 1
    
    return maxValue, taken

def branch_and_bound_best_first(items, capacity, item_count):
    items = sorted(items, key=lambda Item: Item.value/Item.weight, reverse=True)

    v = PQNode(level = -1, value = 0, weight = 0, bound = 0, items = [])
    v.bound = bound(v, capacity, item_count, items)
    Q = PriorityQueue()
    Q.push(v, v.bound)

    maxValue = 0
    bestItems = []

    while not Q.empty():
        v = Q.pop()
        if(v.bound > maxValue):
            u = PQNode(level = None, weight = None, value = None, bound = None, items = [])
            u.level = v.level + 1
            u.weight = v.weight + items[u.level].weight
            u.value = v.value + items[u.level].value
            u.items = list(v.items)
            u.items.append(items[u.level].index)

            if(u.weight <= capacity and u.value > maxValue):
                maxValue = u.value
                bestItems = u.items
            
            u.bound = bound(u, capacity, item_count, items)

            if(u.bound > maxValue):
                Q.push(u, u.bound)
            
            u = PQNode(level = None, weight = None, value = None, bound = None, items = [])
            u.level = v.level + 1
            u.weight = v.weight
            u.value = v.value
            u.items = list(v.items)

            u.bound = bound(u, capacity, item_count, items)

            if(u.bound > maxValue):
                Q.push(u, u.bound)
            
            taken = [0]*len(items)
            for i in range(len(bestItems)):
                taken[bestItems[i]] = 1

    return maxValue, taken

def bound(u, capacity, item_count, items):
    if(u.weight >= capacity):
        return 0
    else:
        result = u.value
        j = u.level + 1
        totweight = u.weight

        while(j < item_count and totweight + items[j].weight <= capacity):
            totweight += items[j].weight
            result += items[j].value
            j = j + 1
        
        k = j
        if(k <= item_count - 1):
            result = result + (capacity - totweight)*items[k].value / items[k].weight

    return result

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

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # a trivial greedy algorithm for filling the knapsack
    # it takes items in-order until the knapsack is full
    value = 0
    # weight = 0
    taken = [0]*len(items)
    # if len(items) < 60:
       
    # for item in items:
    #     if weight + item.weight <= capacity:
    #         taken[item.index] = 1
    #         value += item.value
    #         weight += item.weight

    # value, taken = dynamic_programming(items, capacity)
    # value, taken = solve_it_branch_bound_breadth_first(input_data)
    value, taken = branch_and_bound_breadth_first(items, capacity, item_count)
    # value, taken = branch_and_bound_best_first(items, capacity, item_count)

    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

