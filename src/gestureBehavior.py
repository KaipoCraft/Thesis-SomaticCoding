from abc import ABC, abstractmethod
import openai
import random
openai.api_key = "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"

@abstractmethod
class GestureBehavior(ABC):
    def __init__(self):
        self.function_name = None

    #TODO rework gesture behaviors to run gramatical trnaformations on the data
    def execute(self, active_data_markers_, display_):
        # # Take all the active data markers, get their data, and execute the function
        # data = []
        # memory = []
        # # print(active_data_markers)
        # for marker in active_data_markers:
        #     data.append(marker.get_data())
        #     memory.append(marker.get_memory())
        
        transformed_data = self.function(active_data_markers_, display_)

        # for marker in active_data_markers_:
        #     marker.write_data(self.function_name, transformed_data)

        # return data
    
    def function(self, data):
        # Do something to the data
        pass

#------------------------------------------------------------#
#TODO alter these all so that they return the altered data to the display!

# Users use the print function to see what the different data points are
# class PrintBehavior(GestureBehavior):
#     def __init__(self):
#         self.function_name = "print"
    
#     def function(self, active_data_markers_):
#         super().function(active_data_markers_)
#         # check last memory, if it's start then skip
#         last_key = None
#         for marker in active_data_markers_:
#             last_key = list(marker.memory.keys())[-1]
#             last_value = marker.memory[last_key]
#             if last_key != "start":
#                 marker.memory.pop(last_key)
#             else:
#                 print("Can't undo start")
#         return last_key

# Users use the concat function to concatenate the data on the visible markers
# class ConcatBehavior(GestureBehavior):
#     def __init__(self):
#         self.function_name = "concatenate"
    
#     def function(self, active_data_markers_):
#         super().function(active_data_markers_)
#         output_string = ""
#         for marker in active_data_markers_:
#             # output_string.append(marker.get_data())
#             output_string += marker.get_data()
#         return output_string

# class SplitBehavior(GestureBehavior):
#     def __init__(self):
#         self.function_name = "split"

#     def function(self, active_data_markers_):
#         super().function(active_data_markers_)
#         for marker in active_data_markers_:
#             for key, value in reversed(list(marker.memory.items())):
#                 if key == "concatenate":
#                     # Get the string from the concatenate function
#                     string = marker.memory[key]
#                     # Compare the string to the "data" key and remove differences
#                     marker.memory.pop(key)
#             return marker.memory["data"]

# Call ChatGPT to process the data into an interesting response
# class CallChatGPTBehavior(GestureBehavior):
#     def __init__(self):
#         self.function_name = "Chat GPT call"

#     def function(self, active_data_markers_):
#         super().function(active_data_markers_)
#         import openai
#         openai.api_key = "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"

#         prompt_string = []

#         prompt_string = ' '.join(data)

#         prompt = f"Please make a haiku using these words as inspiration: {prompt_string}"
#         model = "text-davinci-002"
#         response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

#         print(response.choices[0].text.strip())

# Users use the remove function to undo the last action
# class UndoBehavior(GestureBehavior):
#     def __init__(self):
#         self.function_name = "undo"

#     def function(self, active_data_markers_):
#         super().function(active_data_markers_)
#         # check last memory, if it's start then skip
#         last_key = None
#         for marker in active_data_markers_:
#             last_key = list(marker.memory.keys())[-1]
#             # last_value = marker.memory[last_key]
#             if last_key == "undo":
#                 last_key = list(marker.memory.keys())[-2]
#             elif last_key != "start":
#                 marker.memory.pop(last_key)
#             else:
#                 print("Can't undo start")
#         return last_key

# Users use the getComponent function to get the type of string the data is
# class GetTypeBehavior(GestureBehavior):
#     def __init__(self):
#         self.function_name = "get type"

#     def function(self, active_data_markers_):
#         super().function(active_data_markers_)



class ResetBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "reset"

    def function(self, active_data_markers_, display_):
        for marker in active_data_markers_:
            marker.data = marker.og_data
        display_.reset_output()

class GrammarTransformationBehavior(GestureBehavior):
    def __init__(self):
        self.prompt_ending = "The one-word answer with no symbols or punctuation in lowercase is:"
        # Some of these are additive, while others are transformative (maybe order them?)
        # self.word_types = ["Noun-Profession", "Verb-Transitive", "Adjective-Intensifier", "Adverb-Place", "Pronoun-Possessive", "Interjection-Exclamatory", "Article-Definite", "Adverb-Manner"]
        self.word_types = {
            "noun-profession": ["tranformative", "noun"], 
            "verb-transitive": ["additive", "noun"], 
            "adjective-intensifier": ["additive", "adjective"],
            "adverb-place": ["additive", "verb"], 
            "pronoun-possessive": ["additive", "noun"], 
            "interjection-exclamatory": ["additive", "noun"], 
            "article-definite": ["additive", "noun"], 
            "adverb-manner": ["additive", "verb"],
            "adjective-comparative": ["transformative", "adjective"],
            "adjective-superlative": ["transformative", "adjective"],
        }

    def function(self, active_data_markers_, display_):
        print("GrammarTransformationBehavior")
        super().function(active_data_markers_)
        if len(active_data_markers_) == 0:
            return
        transformed_data = []
        # run through each marker
        for marker in active_data_markers_:
            # get this marker's data
            data = marker.get_data()
            # find out what kind of word it is
            word_type = self.find_type(marker)
            # check which type of word it is,, then perform the appropriate transformation via ChatGPT and update the marker's memory
            transformed_data = self.transform_word(data, word_type)

            marker.set_data(transformed_data)

    def find_type(self, marker_):
        return marker_.get_data_type()

    def transform_word(self, data_, word_type_):
        #TODO transform the word based on its type
        new_word_type = self.find_new_word_type(word_type_)
        prompt = f"Transform the word '{data_}' from a {word_type_} to a {new_word_type}. {self.prompt_ending}"
        model = "text-davinci-003"
        # if self.word_types[new_word_type][0] == "additive":
        #     prompt = f"Please add {data_} to the {word_type_}."
        # elif self.word_types[new_word_type][0] == "transformative":
        #     prompt = f"Please transform {data_} from {word_type_} to {new_word_type}."
        response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=5, temperature=0.9, n=1, stop=None)
        transformed_data = response.choices[0].text.strip()
        return transformed_data

    def find_new_word_type(self, word_type_):
        options = []
        for key in self.word_types.keys():
            options.append(str(key))
        new_word_type = random.choice(options)
        return new_word_type
    
    def get_noun_keys(self):
        noun_keys = []
        for key in self.word_types.keys():
            if "noun" in key.lower():
                noun_keys.append(key)
        return noun_keys
    def get_verb_keys(self):
        verb_keys = []
        for key in self.word_types.keys():
            if "verb" in key.lower():
                verb_keys.append(key)
        return verb_keys
    def get_adjective_keys(self):
        adjective_keys = []
        for key in self.word_types.keys():
            if "adjective" in key.lower():
                adjective_keys.append(key)
        return adjective_keys

class AddToOutputBehavior(GestureBehavior):
    def __init__(self) -> None:
        self.function_name = "add to output"
    
    def function(self, active_data_markers_, display_):
        existing_string = display_.get_output()
        if existing_string == None or existing_string.isspace() or "":
            existing_string = "Please add markers to the board first."
        output = []
        for marker in active_data_markers_:
            output.append(marker.get_data())
        output_string = existing_string + " " + " ".join(output)
        print(output_string)
        display_.update_output(output_string)

class RunOutputBehavior(GestureBehavior):
    def __init__(self) -> None:
        self.function_name = "run output"
    
    def function(self, active_data_markers_, display_):
        output_string = display_.get_output()
        print(output_string)
        if output_string == None or output_string.isspace() or "":
            output_string = "Please add some words to the output first."
            display_.update_final_output(output_string)
        else:
            prompt = f"Please write a short poem inspired by this prompt under 40 characters: {output_string}."
            model = "text-davinci-003"
            response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=30, temperature=0.9, n=1, stop=None)
            transformed_data = response.choices[0].text.strip()
            display_.update_final_output(transformed_data)