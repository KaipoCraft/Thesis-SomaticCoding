import cv2

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_empty = True
        
        
    def draw_cell(self, image, color):
        cv2.rectangle(image, (self.x, self.y), (self.x + self.width, self.y + self.height), color, 1)
        return image

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = [[Cell(x, y) for x in range(self.width)] for y in range(self.height)]

    def make_board(self, image):
        # Divide the image into cell objects
        #TODO make the size of the cells dynamic
        for i in range(self.height):
            for j in range(self.width):
                self.cells[i][j].draw_cell(image, (255, 255, 255))


    def get_cells(self):
        return self.cells