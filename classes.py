import heapq

#Класс графа с весами
class SquareGrid:
    __width = 4
    __height = 4

    walls = []
    weights = {}

    def width(self):
        return __width

    def height(self):
        return __height

    def in_bounds(self, id):
        (x,y) = id
        return 0 <= x <= self.__width and 0 <= y <self.__height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0:
            results.reverse()
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)

#Очередь с приоритетами
class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]
