import cv2

class Cell:
    def __init__(self, x, y, size):
        '''
        x: x coordinate of the cell
        y: y coordinate of the cell
        is_empty: boolean value to determine if the cell is empty
        marker: the marker object that is in the cell
        '''
        self.x = x
        self.y = y
        self.is_empty = True
        self.size = size
        self.marker = None
        self.observers = []

    def attach_observer(self, observer):
        self.marker_observers.append(observer)

    def detach_observer(self, observer):
        self.marker_observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def marker_check(self, marker):
        if marker.marker_center[0] > self.x and marker.marker_center[0] < self.x + self.size[0] and marker.marker_center[1] > self.y and marker.marker_center[1] < self.y + self.size[1]:
            self.marker_detected(marker)
        else:
            self.marker_removed()

    def marker_detected(self, marker):
        self.marker = marker
        self.is_empty = False
        if self.observers:
            self.notify_observers()

    def marker_removed(self):
        self.is_empty = True
        self.marker = None
        self.notify_observers()
        
    def draw_cell(self, image, color):
        if self.is_empty:
            image = cv2.rectangle(image, (int(self.x), int(self.y)), (int(self.x + self.size[0]), int(self.y + self.size[1])), color, 1)
        else:
            image = cv2.rectangle(image, (int(self.x), int(self.y)), (int(self.x + self.size[0]), int(self.y + self.size[1])), color, -1)
        # cv2.rectangle(image, (int(self.x), int(self.y)), (int(self.x + self.size[0]), int(self.y + self.size[1])), color, 1)
        return image
    
    def get_marker(self):
        return self.marker

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Board(metaclass=SingletonMeta):
    '''
    width: width of the board
    height: height of the board
    cells: list of cells that make up the board
    '''
    def __init__(self):
        self.cells = []
        
    def draw_board(self, image):
        # Draw the cells
        for cell in self.cells:
            image = cell.draw_cell(image, (255, 255, 255))
        return image

    def get_cells(self):
        return self.cells
    
class BoardFactory():
    def __init__(self, width, height, grid_dims):
        self.width = width
        self.height = height
        self.grid_dims = grid_dims
        # 6:9 ratio

    def make_board(self):
        board = Board()
        # Divide the board into the cells
        # if we have the width and the number of cells, we divide the width by the number of cells
        unit_width = self.width / self.grid_dims[0]
        unit_height = self.height / self.grid_dims[1]

        for i in range(self.grid_dims[0]):
            for j in range(self.grid_dims[1]):
                board.cells.append(Cell(i * unit_width, j * unit_height, (unit_width, unit_height)))

        return board