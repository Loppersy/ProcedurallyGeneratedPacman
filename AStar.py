class AStar(object):
    def __init__(self, start, goal, grid):
        self.start = start
        self.goal = goal
        self.grid = grid
        self.open = []
        self.closed = []
        self.path = []
        self.g = 0
        self.h = 0
        self.f = 0
        self.current = None

    def get_path(self):
        self.open.append(self.start)
        while len(self.open) > 0:
            self.current = self.open[0]
            for cell in self.open:
                if cell.f < self.current.f:
                    self.current = cell
            if self.current == self.goal:
                while self.current != self.start:
                    self.path.append(self.current)
                    self.current = self.current.parent
                return self.path[::-1]
            self.open.remove(self.current)
            self.closed.append(self.current)
            for cell in self.current.neighbors:
                if cell in self.closed:
                    continue
                if cell not in self.open:
                    self.open.append(cell)
                cell.parent = self.current
                cell.g = self.current.g + 1
                cell.h = self.heuristic(cell)
                cell.f = cell.g + cell.h
        return None

    def heuristic(self, cell):
        return abs(cell.x - self.goal.x) + abs(cell.y - self.goal.y)