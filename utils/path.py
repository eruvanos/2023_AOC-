import math
from collections import deque, UserDict
from dataclasses import dataclass
from io import StringIO
from operator import attrgetter
from typing import List, Optional, Set, Dict

from utils.data import PriorityQueue
from utils.vector import Vec2, manhattan_neighbors


def manhattan(start: Vec2, target: Vec2):
    (x1, y1) = start
    (x2, y2) = target
    return abs(x1 - x2) + abs(y1 - y2)


def flip(pos):
    return pos[1], pos[0]


class Graph:
    """Abstraction of graph"""

    def neighbors(self, current: Vec2) -> List:
        """List coordinates of all valid neighbors"""
        raise NotImplementedError()

    def cost(self, current: Vec2, neighbor: Vec2) -> int:
        """Provides costs to the neighbor"""
        raise NotImplementedError()


class GridGraph(Graph):
    """Graph using manhattan distance for cost function"""

    def cost(self, current: Vec2, neighbor: Vec2):
        return manhattan(current, neighbor)


class ArrayGraph(GridGraph):
    """
    GridGraph implementation backed by an array like obj used like obj[x][y].
    Uses manhattan neighbors.
    """

    def __init__(self, map):
        self._map = map

    def get(self, pos: Vec2, default=None):
        x, y = pos
        if self.has(pos):
            return self._map[x][y]
        else:
            return default

    def width(self):
        return len(self._map[0])

    def height(self):
        return len(self._map)

    def has(self, pos: Vec2):
        x, y = pos
        return 0 <= x < len(self._map) and 0 <= y < len(self._map[x])

    def neighbors(self, current: Vec2) -> List:
        return [n for n in manhattan_neighbors(current) if self.has(n)]

    def __iter__(self):
        """
        :return: a iterator of every field with its value (x,y,value)
        """
        for x, cs in enumerate(self._map):
            for y, c in enumerate(cs):
                if c < min(self.get(n) for n in self.neighbors(Vec2(x, y))):
                    yield x, y, c


class MapGraph(GridGraph, UserDict):
    """
    Graph implementation backed by a map used like Dict[Vec2, Any].

    For search algorithms, only not blocked nodes should be added.
    """

    def neighbors(self, current: Vec2) -> List:
        return [n for n in manhattan_neighbors(current) if n in self.data]

    @property
    def max_y(self):
        return max(map(attrgetter("y"), self.data))

    @property
    def min_y(self):
        return min(map(attrgetter("y"), self.data))

    @property
    def max_x(self):
        return max(map(attrgetter("x"), self.data))

    @property
    def min_x(self):
        return min(map(attrgetter("x"), self.data))

    def __repr__(self):
        text = StringIO()

        for y in range(self.min_y, self.max_y + 1):
            text.write(f"{y:03.0f} ")
            for x in range(self.min_x, self.max_x + 1):
                text.write(self.get(Vec2(x, y), "."))
            text.write("\n")

        return text.getvalue()

    def to_string(self, y_reversed=False):
        text = StringIO()

        y_range = range(self.min_y, self.max_y + 1)

        if y_reversed:
            y_range = reversed(y_range)

        for y in y_range:
            text.write(f"{y:03.0f} ")
            for x in range(self.min_x, self.max_x + 1):
                text.write(self.get(Vec2(x, y), "."))
            text.write("\n")

        return text.getvalue()

class SetGraph(GridGraph):
    """
    Graph implementation backed by a Set[Vec2]
    """

    def __init__(self, data: Set[Vec2]):
        self.data = data

    def neighbors(self, current: Vec2) -> List:
        return [n for n in manhattan_neighbors(current) if n in self.data]

    @property
    def max_y(self):
        return max(map(attrgetter("y"), self.data))

    def __repr__(self):
        text = StringIO()

        min_x = min(map(attrgetter("x"), self.data))
        min_y = min(map(attrgetter("y"), self.data))
        max_x = max(map(attrgetter("x"), self.data))
        max_y = self.max_y

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                text.write("." if Vec2(x, y) in self.data else "#")
            text.write("\n")

        return text.getvalue()


def _reconstruct_path(came_from, goal):
    current = goal
    path = [current]
    while came_from[current]:
        current = came_from[current]
        path.append(current)
    path.reverse()  # optional
    return path[1:]


@dataclass
class PathResult:
    path: Optional[List[Vec2]]
    came_from: Dict[Vec2, Vec2]


def a_star_search(graph: Graph, start: Vec2, goal: Vec2) -> PathResult:
    """Implementation of A* algorithm.

    The algorithm uses a guess function (in this case manhattan distance) to prioritise path.
    """
    if start == goal:
        return PathResult([], {})

    frontier = PriorityQueue()
    frontier.put((0, start))

    came_from = {start: None}
    cost_so_far = {start: (0, None)}

    while not frontier.empty():
        current = frontier.get()[1]

        if current == goal:
            return PathResult(path=_reconstruct_path(came_from, goal), came_from=came_from)

        neighbors = graph.neighbors(current)
        for neighbor in neighbors:
            new_cost = cost_so_far[current][0] + graph.cost(current, neighbor)
            if neighbor not in cost_so_far or (new_cost, flip(current)) < cost_so_far[neighbor]:
                cost_so_far[neighbor] = (new_cost, flip(current))
                priority = new_cost + manhattan(goal, neighbor)

                frontier.put((priority, neighbor))
                came_from[neighbor] = current

    return PathResult(None, came_from)


def breadth_first_search(graph: Graph, pos: Vec2, targets: Set[Vec2]) -> PathResult:
    """
    Breadth-first search (BFS) is an algorithm for searching a graph for a node that satisfies a given property.

    This implementation support search for multiple targets, returning path to the closest one (manhatten distance)
    """
    if pos in targets:
        return PathResult([], {})

    todo = deque()
    came_from = {pos: None}

    todo.append((0, pos))

    found = []
    max_depth = math.inf
    while todo:
        depth, current = todo.popleft()
        if depth > max_depth:
            break

        neighbors = graph.neighbors(current)
        for neighbor in neighbors:
            if neighbor not in came_from:
                todo.append((depth + 1, neighbor))
                came_from[neighbor] = current

                if neighbor in targets:
                    max_depth = min(depth, max_depth)
                    found.append(neighbor)

    if not found:
        return PathResult(None, came_from)

    found.sort(key=lambda p: flip(p))
    return PathResult(_reconstruct_path(came_from, found[0]), came_from)
