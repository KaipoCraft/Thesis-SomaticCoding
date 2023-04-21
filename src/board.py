import cv2
import singleton

class Cell:
    def __init__(self, x, y, id, size):
        '''
        x: x coordinate of the cell
        y: y coordinate of the cell
        is_empty: boolean value to determine if the cell is empty
        marker: the marker object that is in the cell
        '''
        self.x = x
        self.y = y
        self.id = id
        self.is_empty = True
        self.size = size
        self.marker = None
        # self.observers = []
        self.neighbors = ((self.x-1, self.y), (self.x, self.y-1), (self.x+1, self.y), (self.x, self.y+1)) # Left, Top, Right, Bottom

    # def attach_observer(self, observer):
    #     self.observers.append(observer)
    # def detach_observer(self, observer):
    #     self.observers.remove(observer)
    # def notify_observers(self):
    #     for observer in self.observers:
    #         observer.cell_update(self)

    def check_for_markers(self, marker):
        '''
        Check if the marker is in the cell
        Params:
            marker: the marker object that is being checked
        '''
        if marker.marker_center[0] > self.x and marker.marker_center[0] < self.x + self.size[0] and marker.marker_center[1] > self.y and marker.marker_center[1] < self.y + self.size[1]:
            self.marker_detected(marker)
        elif self.marker != None:
            self.marker_removed()

    def marker_detected(self, marker):
        '''
        Run this if a marker is detected in the cell
        Params:
            marker: the marker object that is in the cell
        '''
        self.is_empty = False
        self.marker = marker
        self.marker.set_current_cell(self.get_id())   # Set the marker's current cell to this cell
        # self.notify_observers()         # Notify the observers with up to date info
            
    def marker_removed(self):
        '''
        Run this if a marker is removed from the cell
        Params:
            marker: the marker object that has been removed from the cell
        '''
        self.is_empty = True
        self.marker.set_current_cell(None)   # Set the marker's current cell to None
        self.marker = None
        # self.notify_observers()         # Notify the observers with up to date info
        
    def draw_cell(self, image, color):
        #TODO fix this, it seems to only want to draw one thicker rectangle at a time
        if self.is_empty:
            border_thickness = 1
        else:
            border_thickness = 5
        cv2.rectangle(image, (int(self.x), int(self.y)), (int(self.x + self.size[0]), int(self.y + self.size[1])), color, border_thickness)

        # calculate the size of the text
        text_size, _ = cv2.getTextSize(str(self.id), cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)

        # calculate the center of the bounding box of the text
        text_x = int(self.x + self.size[0] // 2 - text_size[0] // 2)
        text_y = int(self.y + self.size[1] // 2 + text_size[1] // 2)

        # draw the text with the updated position
        cv2.putText(image, str(self.id), (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)

        # cv2.putText(image, str(self.id), (int(self.x + self.size[0]//2), int(self.y + self.size[1]//2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2, cv2.LINE_AA)
        
        return image
    
    def get_marker(self):
        return self.marker
    
    def get_id(self):
        return self.id

class Board(metaclass=singleton.SingletonMeta):
    '''
    cells: list of cells that make up the board
    '''
    def __init__(self):
        self.cells = []
        
    def draw_board(self, image, color, window_size):
        cv2.rectangle(image, (0, 0), (window_size[0], window_size[1]), (10, 10, 10), -1)
        # Draw the cells
        for cell in self.cells:
            cell.draw_cell(image, color)
        return image
    
    # def attach_cell_observers(self, observer):
    #     for cell in self.cells:
    #         cell.attach_observer(observer)
    
    def get_cell(self, id):
        for cell in self.cells:
            if cell.get_id() == id:
                return cell
        return None

    def get_cells(self):
        return self.cells
    
class BoardFactory():
    @staticmethod
    def make_board(window_dims, grid_dims):
        # version where grid_size is the number of squares in the grid on the shortest window dimension
        width = window_dims[0]
        height = window_dims[1]
        board = Board()

        square_unit_size = min(width, height) // grid_dims
        num_squares_height = int(height // square_unit_size)
        num_squares_width = int(width // square_unit_size)

        margin_x = (width - (num_squares_width * square_unit_size)) // 2
        margin_y = (height - (num_squares_height * square_unit_size)) // 2

        for i in range(num_squares_width):
            for j in range(num_squares_height):
                cell_x = i * square_unit_size + margin_x
                cell_y = j * square_unit_size + margin_y
                if cell_x > width:
                    pass
                elif cell_y > height:
                    pass
                else:
                    id = f'{i},{j}'
                    board.cells.append(Cell(cell_x, cell_y, id, (square_unit_size, square_unit_size)))
        return board