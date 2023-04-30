from abc import ABC, abstractmethod
import openai
openai.api_key = "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"

@abstractmethod
class GestureBehavior(ABC):
    def __init__(self):
        self.function_name = None

    #TODO rework gesture behaviors to run gramatical trnaformations on the data
    def execute(self, active_data_markers):
        # # Take all the active data markers, get their data, and execute the function
        # data = []
        # memory = []
        # # print(active_data_markers)
        # for marker in active_data_markers:
        #     data.append(marker.get_data())
        #     memory.append(marker.get_memory())
        
        transformed_data = self.function(active_data_markers)

        for marker in active_data_markers:
            marker.write_data(self.function_name, transformed_data)

        # return data
    
    def function(self, data):
        # Do something to the data
        pass

#------------------------------------------------------------#
#TODO alter these all so that they return the altered data to the display!

# Users use the print function to see what the different data points are
class PrintBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "print"
    
    def function(self, active_data_markers_):
        super().function(active_data_markers_)
        # check last memory, if it's start then skip
        last_key = None
        for marker in active_data_markers_:
            last_key = list(marker.memory.keys())[-1]
            last_value = marker.memory[last_key]
            if last_key != "start":
                marker.memory.pop(last_key)
            else:
                print("Can't undo start")
        return last_key

# Users use the concat function to concatenate the data on the visible markers
class ConcatBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "concatenate"
    
    def function(self, active_data_markers_):
        super().function(active_data_markers_)
        output_string = ""
        for marker in active_data_markers_:
            # output_string.append(marker.get_data())
            output_string += marker.get_data()
        return output_string

class SplitBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "split"

    def function(self, active_data_markers_):
        super().function(active_data_markers_)
        for marker in active_data_markers_:
            for key, value in reversed(list(marker.memory.items())):
                if key == "concatenate":
                    # Get the string from the concatenate function
                    string = marker.memory[key]
                    # Compare the string to the "data" key and remove differences
                    marker.memory.pop(key)
            return marker.memory["data"]

# Call ChatGPT to process the data into an interesting response
class CallChatGPTBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "Chat GPT call"

    def function(self, active_data_markers_):
        super().function(active_data_markers_)
        import openai
        openai.api_key = "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"

        prompt_string = []

        prompt_string = ' '.join(data)

        prompt = f"Please make a haiku using these words as inspiration: {prompt_string}"
        model = "text-davinci-002"
        response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=50)

        print(response.choices[0].text.strip())

# Users use the remove function to undo the last action
class UndoBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "undo"

    def function(self, active_data_markers_):
        super().function(active_data_markers_)
        # check last memory, if it's start then skip
        last_key = None
        for marker in active_data_markers_:
            last_key = list(marker.memory.keys())[-1]
            # last_value = marker.memory[last_key]
            if last_key == "undo":
                last_key = list(marker.memory.keys())[-2]
            elif last_key != "start":
                marker.memory.pop(last_key)
            else:
                print("Can't undo start")
        return last_key

# Users use the getComponent function to get the type of string the data is
class GetTypeBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "get type"

    def function(self, active_data_markers_):
        super().function(active_data_markers_)





class GrammarTransformationBehavior(GestureBehavior):
    def __init__(self, transform_function):
        self.transform_function = transform_function

    def function(self, active_data_markers_):
        super().function(active_data_markers_)
        #TODO get the last value from the active marker's memory
        
        #TODO find out what it is grammatically (i.e. noun, verb, adjective, adverb)

        # perform the grammatical transformation using the specified transform function
        transformed_value = self.transform_function(last_value)
        # update the marker's memory with the transformed value
        active_data_markers_[-1].memory["transformed_value"] = transformed_value

    def find_type(self, string):
        #TODO find out what it is grammatically (i.e. noun, verb, adjective, adverb)
        pass