# Test Code
# should return:
# ['Hello']
# {'print': ['Hello']}
# ['Hello', 'World']
# {'print': ['Hello', 'World']}

import sys
sys.path.append('..\src')

import markers
import gestures

TestMarker1 = markers.DataMarker(8, "Hello")
TestMarker2 = markers.DataMarker(9, "World")
found_markers = [TestMarker1, TestMarker2]

TestGesture = gestures.UnderlineGesture()
TestGesture.set_found(True)
TestGesture.execute(found_markers)