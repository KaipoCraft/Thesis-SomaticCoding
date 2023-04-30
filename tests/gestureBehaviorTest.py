import sys
sys.path.append('..\src')

import markers
import gestures
import display
import openai

# Test Code
# should return:
# ['Hello']
# {'print': ['Hello']}
# ['Hello', 'World']
# {'print': ['Hello', 'World']}
#

test_dict = {8: ['go', 'verb'], 9: ['world', 'noun']}

test_display = None

TestMarker1 = markers.DataMarker(8, test_dict[8][0], test_dict[8][1])
TestMarker2 = markers.DataMarker(9, test_dict[9][0], test_dict[9][1])
found_markers = [TestMarker1, TestMarker2]

TestGesture = gestures.ClockwiseCircleGesture()
TestGesture.set_found(True)
TestGesture.execute(found_markers, test_display)

# data_ = "world"
# word_type_ = "noun"
# new_word_type = "negated noun"
# prompt_opening = f"You can only say one word at a time and cannot use any symbols or uppercase letters."
# prompt = f"Transform the word '{data_}' from a {word_type_} to a {new_word_type}. The one-word answer with no symbols or punctuation in lowercase is:"
# print(prompt)
# model = "text-davinci-002"
# response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=5, temperature=0.8, n=1, stop=None)
# transformed_data = response.choices[0].text.strip()
# print(transformed_data)