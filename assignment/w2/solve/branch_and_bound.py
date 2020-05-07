from recordclass import recordclass
from collections import deque
import heapq

Item = recordclass('Item', 'index value weight')
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
        if len(self._queue) is 0:
            return True
        else:
            return False
    
    def length(self):
        return len(self._queue)

def bound(u, capacity, item_count, items):
    if (u.weight >= capacity):
        return 0
    else:
        result = u.value
        j = u.level + 1
        totweight = u.weight

        while(j < item_count and totweight + items[j].weight <= capacity):
            totweight = totweight + items[j].weight
            result = result + items[j].value
            j = j + 1
        
        k = j
        if (k <= item_count -1):
            result = result + (capacity - totweight)*items[k].value/items[k].weight

        return result

def solve_it_branch_bound_breadth_first(input_data):
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    # sorting Item on basis of value per unit
    # weight.
    items = sorted(items, key=lambda Item: Item.weight/Item.value)

    # make a queue for traversing the node
    v = Node(level = -1, value = 0, weight = 0, items = [])
    Q = deque([])
    Q.append(v)

    # One by one extract an item from decision tree
    # compute profit of all children of extracted item
    # and keep saving maxProfit
    maxValue = 0
    bestItems = []

    while(len(Q) != 0):
        # Dequeue a node
        v = Q[0]

        Q.popleft()
        u = Node(level=None, weight=None, value=None, items = [])

        u.level = v.level + 1
        u.weight = v.weight + items[u.level].weight
        u.value = v.value + items[u.level].value
        u.items = list(v.items)
        u.items.append(items[u.level].index)

        if (u.weight <= capacity and u.value > maxValue):
            maxValue = u.value
            bestItems = u.items

        bound_u = bound(u, capacity, item_count, items)

        if (bound_u > maxValue):
            Q.append(u)

    taken = [0]*len(items)
    for i in range(len(bestItems)):
        taken[bestItems[i]] = 1
    
    # output_data = str(maxValue) + ' ' + str(0) + '\n'
    # output_data += ' '.join(map(str, taken))
    return maxValue, taken