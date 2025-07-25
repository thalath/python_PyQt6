import sys
import heapq
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QComboBox, QLabel, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsSimpleTextItem
)
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtCore import QTimer
import itertools

CELL_SIZE = 25

GRID_COLS = 30
GRID_ROWS = 20

class Cell(QGraphicsRectItem):
    def __init__(self, row, col):
        super().__init__(0, 0, CELL_SIZE, CELL_SIZE)
        self.row = row
        self.col = col
        
        self.setPos(col * CELL_SIZE, row * CELL_SIZE)
        self.setBrush(QColor("white"))
        self.setPen(QColor("red"))
        self.type = "empty"
        
        self.text_item = QGraphicsSimpleTextItem("", self)
        self.text_item.setFont(QFont("Arial", 8))
        self.text_item.setBrush(QColor("black"))
        self.text_item.setPos(3, 3)
        self.setAcceptHoverEvents(True)
        self._hover_text = None
        
    def set_type(self, cell_type):
        color_map = {
            "empty": "white",
            "wall": "black",
            "start": "green",
            "goal": "red",
            "visitted": "lightblue",
            "path": "yellow"
        }
        self.type = cell_type
        self.setBrush(QColor(color_map[cell_type]))
        if cell_type not in ("path", "visitted"):
            self.text_item.setText("")
        if self._hover_text:
            self.scene().removeItem(self._hover_text)
            self._hover_text = None
            
    def set_step_label(self, text):
        self.text_item.setText(str(text))

    def hoverEnterEvent(self, event):
        if self.type == "path" and self.text_item.text():
            self._hover_text = QGraphicsSimpleTextItem(f"Step: {self.text_item.text()}")
            self._hover_text.setFont(QFont("Arial", 10))
            self._hover_text.setBrush(QColor("blue"))
            self._hover_text.setZValue(1)
            self._hover_text.setPos(self.scenePos().x(), self.scenePos().y() - 20)
            self.scene().addItem(self._hover_text)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self._hover_text:
            self.scene().removeItem(self._hover_text)
            self._hover_text = None
        super().hoverLeaveEvent(event)

class Grid:
    def __init__(self, scene):
        self.scene = scene
        # self.cells = [[Cell(r,c) for c in range(GRID_COLS)] for r in range(GRID_ROWS)] 
        
        self.cells = []
        for r in range(GRID_ROWS):
            row = []
            for c in range(GRID_COLS):
                row.append(Cell(r, c))
            self.cells.append(row)
            
        for row in self.cells:
            for cell in row:
                self.scene.addItem(cell)
        self.start = None
        self.goal = None

    def reset(self):
        for row in self.cells:
            for cell in row:
                if cell.type in ("visitted", "path"):
                    cell.set_type('empty')

    def clear_all(self):
        for row in self.cells:
            for cell in row:
                cell.set_type("empty")
                cell.text_item.setText("")
        self.goal = None
        self.start = None
        
    def neighbors(self, cell):
        direction = [(-1, 0),(1,0),(0,-1),(0,1)]
        result = []
        for dr, dc in direction:
            r, c = cell.row + dr, cell.col + dc
            if 0 <= r < GRID_ROWS and 0 <= c < GRID_COLS:
                neighbor = self.cells[r][c]
                if neighbor.type != 'wall':
                    result.append(neighbor)
        return result

def heuristic(cell1, cell2):
    return abs(cell1.row - cell2.row) +  abs(cell1.col - cell2.col)

def astar(grid):
    start = grid.start
    goal = grid.goal
    open_set = []
    counter = itertools.count()

    heapq.heappush(open_set, (0, next(counter), start))
    came_from = {}
    cost_so_far = {start: 0}
    visitted_order = []

    while open_set:
        _,_, current = heapq.heappop(open_set)
        if current == goal:
            break
        for neighbor in grid.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal)
                heapq.heappush(open_set, (priority, next(counter), neighbor))
                came_from[neighbor] = current
                visitted_order.append(neighbor)
    return came_from, visitted_order

def greed_best_first(grid):
    start = grid.start
    goal = grid.goal
    open_set = []
    counter = itertools.count()

    heapq.heappush(open_set, (heuristic(start, goal), next(counter), start))
    came_from = {}
    visitted = set()
    visitted_order = []

    while open_set:
        _, _, current = heapq.heappop(open_set)
        if current == goal:
            break
        visitted.add(current)
        for neighbor in grid.neighbors(current):
            if neighbor not in visitted and neighbor not in [item[2] for item in open_set]:
                heapq.heappush(open_set, (heuristic(neighbor, goal), next(counter), neighbor))
                came_from[neighbor] = current
                visitted_order.append(neighbor)
    return came_from, visitted_order


class PathFindingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Pathfinding Visualizer")
        self.setWindowIcon(QIcon("idea.png"))
        
        self.scene = QGraphicsScene()
        self.grid = Grid(self.scene)

        self.view = QGraphicsView(self.scene)
        self.combo = QComboBox()
        self.combo.addItems(["I Love her 🫣", "she doesn't love me 😢"])
        self.run_btn = QPushButton("Run")
        self.run_btn.clicked.connect(self.run_search)
        self.clear_btn = QPushButton("Clear Grid")
        self.clear_btn.clicked.connect(self.clear_grid)
        self.step_label = QLabel("Step: 0")
        self.step_label.setStyleSheet(
        """
            font-family: Arial;
            font-size: 13px;
            font-weight: 650;
            color: darkblue;
        """
        )

        layout = QVBoxLayout()
        top_bar = QHBoxLayout()
        AT = QLabel("Algorithm:")
        # AT.setFont(QFont("Arial", 10))
        AT.setStyleSheet("""
            font-family: Arial;
            font-weight: 700;
            font-size: 14px;
            color: red;
        """)
        top_bar.addWidget(AT)
        top_bar.addWidget(self.combo)
        top_bar.addWidget(self.run_btn)
        top_bar.addWidget(self.clear_btn)
        top_bar.addWidget(self.step_label)

        layout.addLayout(top_bar)
        layout.addWidget(self.view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setFixedSize(GRID_COLS * CELL_SIZE + 2, GRID_ROWS * CELL_SIZE + 2)
        self.view.setRenderHint(self.view.renderHints())

        self.view.setMouseTracking(True)
        self.view.viewport().installEventFilter(self)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.step_visualization)
        self.search_step = []
        self.path = []
        self.step_counter = 0
        
    def eventFilter(self, source, event):
        if event.type() == event.Type.MouseButtonPress:
            pos = self.view.mapToScene(event.pos())
            col = int(pos.x() // CELL_SIZE)
            row = int (pos.y() // CELL_SIZE)
            if 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS:
                cell = self.grid.cells[row][col]
                if self.grid.start is None:
                    cell.set_type("start")
                    self.grid.start = cell
                elif self.grid.goal is None:
                    cell.set_type("goal")
                    self.grid.goal = cell
                elif cell.type == "empty":
                    cell.set_type("wall")
                elif cell.type == "wall":
                    cell.set_type("empty")
        return super().eventFilter(source, event)

    def run_search(self):
        self.grid.reset()
        algorithm = self.combo.currentText()
        if algorithm == "I Love her 🫣":
            came_from, steps = astar(self.grid)
        elif algorithm == "she doesn't love me 😢":
            came_from, steps = greed_best_first(self.grid)
        else:
            return 

        self.search_step = steps
        self.reconstruct_path(came_from)
        self.step_counter = 0
        self.step_label.setText("Steps: 0")
        self.timer.start(50)

    def clear_grid(self):
        self.grid.clear_all()
        self.step_label.setText("Steps: 0")
        self.search_step = []
        self.path = []
        self.step_counter = 0
        self.timer.stop()
        
    def step_visualization(self):
        if self.search_step:
            cell = self.search_step.pop(0)
            if cell not in (self.grid.start, self.grid.goal):
                cell.set_type("visitted")
                self.step_counter += 1
                cell.set_step_label(self.step_counter)
                self.step_label.setText(f"Steps: {self.step_counter}")

            if len(self.search_step) > 1:
                second = self.search_step[0]
                if second not in (self.grid.start, self.grid.goal):
                    second.setBrush(QColor("orange"))
            if len(self.search_step) > 2:
                third = self.search_step[1]
                if third not in (self.grid.start, self.grid.goal):
                    third.setBrush(QColor("pink"))

        elif self.path:
            cell = self.path.pop(0)
            if cell not in (self.grid.start, self.grid.goal):
                cell.set_type("path")
                self.step_counter += 1
                cell.set_step_label(self.step_counter)
                self.step_label.setText(f"Steps: {self.step_counter}")
        else:
            self.timer.stop()
            
    def reconstruct_path(self, came_from):
        current = self.grid.goal
        while current != self.grid.start:
            current = came_from.get(current)
            if current is None:
                break
            self.path.insert(0, current)
       
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PathFindingApp()
    window.show()
    sys.exit(app.exec())