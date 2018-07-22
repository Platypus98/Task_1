from classes import *
import collections
import heapq


def draw_tile(graph, id, style):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'path' in style and id in style['path']: r = "*"
    if 'start' in style and id == style['start']: r = "O"
    if 'goal' in style and id == style['goal']: r = "X"
    if id in graph.walls: r = "#"
    return r

#Функция отрисовки графа
def draw_grid(graph, **style):
    for y in range(5):
        for x in range(5):
            print("%%-%ds" % 2 % draw_tile(graph, (x, y), style), end="")
        print()

#Манхэттенское расстояние
def heuristic_manh(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

#Расстояние Чебышева
def heuristic_cheb(a,b):
    (x1, y1) = a
    (x2, y2) = b
    return max(abs(x1 - x2), abs(y1 - y2))


def search_path_heuristic_manh(graph, start, goal):
    count_of_nodes = 0
    frointer = PriorityQueue()
    frointer.put(start, 0)
    came_from = {}  #came_from - словарь, {"координаты ячейки": "из какой ячейки туда пришли"}
    cost_so_far = {} #cost_so_far - словарь, {"координаты ячейки": "количество шагов от старта"}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frointer.empty():
        current = frointer.get() #Берется первый элемент в куче

        if current == goal:
            break

        for next in graph.neighbors(current): #Проводится итерация по соседям
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_manh(goal, next) #Приоритет исследования ячейки
                frointer.put(next, priority)
                came_from[next] = current


    return came_from, cost_so_far

def search_path_heuristic_cheb(graph, start, goal):
    count_of_nodes = 0
    frointer = PriorityQueue()
    frointer.put(start, 0)
    came_from = {}  #came_from - словарь, {"координаты ячейки": "из какой ячейки туда пришли"}
    cost_so_far = {} #cost_so_far - словарь, {"координаты ячейки": "количество шагов от старта"}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frointer.empty():
        current = frointer.get() #Берется первый элемент в куче

        if current == goal:
            break

        for next in graph.neighbors(current): #Проводится итерация по соседям
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic_cheb(goal, next) #Приоритет исследования ячейки
                frointer.put(next, priority)
                came_from[next] = current


    return came_from, cost_so_far

def construct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path



init_graph = [] #Входной массив
mass_walls = [] #Массив с координатами стен
goal = ""
start = ""
print("Введите разметку поля. Каждую новую строку следует записывать на новой строке. Символы необходимо разделять пробелом. # - стена. X - точка назначения. O(буква) - точка старта.")
print('''Например:\n
. . . . X \n
. # # # . \n
. . . . . \n
. . . # . \n
. O . . . \n
        ''')
print("Введите разметку:")


for _ in range(5):
    init_graph.append(input().rstrip().lstrip())

for i in range(5):
    if "X" in init_graph[i]:
        new_mass = init_graph[i].split(" ")
        goal = (new_mass.index("X"), i)

    if "O" in init_graph[i]:
        new_mass = init_graph[i].split(" ")
        start = (new_mass.index("O"), i)

    if "#" in init_graph[i]:
        new_mass = init_graph[i].split(" ")
        for j in range(5):
            if new_mass[j] == "#":
                mass_walls.append((j, i))

if goal == "" or start == "":
    print("Разметка введена неправильно. Выход из программы ...")
    exit()

g = SquareGrid() #Создание графа
g.walls = mass_walls

#Манхэттенское рассояние
came_from, cost_so_far = search_path_heuristic_manh(g, start, goal)
print("Количество исследованных вершин по эвристике 'Манхэттенское расстояние' - {0}(включая начальную и конечную)".format(len(cost_so_far)))
try:
    draw_grid(g, path = construct_path(came_from, start, goal), start = start, goal= goal) #Вывод графа
except KeyError:
    print("Маршрут не найден")
print()

#Расстояние Чебышева
came_from, cost_so_far = search_path_heuristic_cheb(g, start, goal)
print("Количество исследованных вершин по эвристике 'Расстояние Чебышева' - {0}(включая начальную и конечную)".format(len(cost_so_far)))
try:
    draw_grid(g, path = construct_path(came_from, start, goal), start = start, goal= goal) #Вывод графа
except KeyError:
    print("Маршрут не найден")
