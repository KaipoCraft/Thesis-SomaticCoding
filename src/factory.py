import gestures

class GestureFactory:
    def make_gestures(self, list_of_gestures_):

        list_of_gesture_objects = None

        for gesture in list_of_gestures_:
            if gesture == "Test":
                gesture = list_of_gesture_objects.append(gestures.TestGesture())
            elif gesture == "Clockwise Circle":
                gesture = list_of_gesture_objects.append(gestures.ClockwiseCircleGesture())
            elif gesture == "Counter-Clockwise Circle":
                gesture = list_of_gesture_objects.append(gestures.CounterClockwiseCircleGesture())
            elif gesture == "Underline":
                gesture = list_of_gesture_objects.append(gestures.UnderlineGesture())
            else:
                pass
        
        return list_of_gesture_objects
    
#------------------------------------------------------------#
import markers

class MarkerFactory:    
    @staticmethod
    def make_markers(marker_dict_, history_length_):
        marker_list = []
        for marker_id, data in marker_dict_.items():
            if data == 'cursor':
                marker_list.append(markers.CursorMarker(marker_id, data, history_length_))
            else:
                marker_list.append(markers.DataMarker(marker_id, data))
        return marker_list

#------------------------------------------------------------#
import board

class BoardFactory():
    @staticmethod
    def make_board(board_, window_dims_, grid_dims_):
        # version where grid_size is the number of squares in the grid on the shortest window dimension
        width = window_dims_[0]
        height = window_dims_[1]

        square_unit_size = min(width, height) // grid_dims_
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
                    board_.cells.append(board.Cell(cell_x, cell_y, id, (square_unit_size, square_unit_size)))
        return board