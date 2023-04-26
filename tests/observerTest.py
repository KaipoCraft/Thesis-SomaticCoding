# Test Code
# should return:
# []
# ['←']
# ['←', '↑']
# ['←', '↑', '→']
# ['←', '↑', '→', '↓']
# Clockwise Circle found
# [[<markers.DataMarker object at 0x000001E65300E4A0>, <markers.DataMarker object at 0x000001E65300E440>]]

import sys
sys.path.append('..\src')

import markers
import gestures
import observer



test_cursor = markers.CursorMarker(0, None, 10)

test_marker1 = markers.DataMarker(8, "Black")
test_marker2 = markers.DataMarker(9, "Board")
test_marker1.is_visible = True
test_marker2.is_visible = True

test_observer = observer.Executioner([test_marker1, test_marker2])

test_cursor.attach_observer(test_observer)
test_marker1.attach_observer(test_observer)
test_marker2.attach_observer(test_observer)

test_marker1.memory['concatenate'] = "BlackBoard" 
test_marker1.memory['add'] = "Black and White"
test_marker2.memory['concatenate'] = "BlackBoard" 
test_marker2.memory['add'] = "Black and White"
# test_marker2.memory = {'start': 'self.data',
#                        'concatenate': 'self.data + " and Black"',
#                         'add': 'self.data + " and White"',}

#TODO for some reason this is reversed now (i.e. cell history is now direction history and vice versa)
# test_cursor.set_movement_history([(0, 0), (0, 1), (1, 1), (1, 0)], ["←", "↑", "→", "↓", "←"])
# test_cursor.set_movement_history([(0, 0), (0, 1), (1, 1), (1, 0)], ["←", "←", "←", "→", "→", "→", "←"])
test_cursor.set_movement_history([(0, 0), (0, 1), (1, 1), (1, 0)], ["↑", "↑", "↑", "↓", "↓", "↓", "↑"])
test_cursor.set_movement_history([(0, 0), (0, 1), (1, 1), (1, 0)], ["←", "↓", "→", "↑", "→"])

test_observer.set_active_data_markers()
test_observer.update(test_cursor.cell_history, test_cursor.direction_history)