from abc import ABC, abstractmethod

@abstractmethod
class GestureBehavior(ABC):
    def __init__(self):
        self.function_name = None

    def execute(self, active_data_markers):
        # Take all the active data markers, get their data, and execute the function
        data = []
        for marker in active_data_markers:
            data.append(marker.get_data())
            self.function(data)
            marker.write_data(self.function_name, data)
        return data
    
    def function(self, data):
        # Do something to the data
        pass

#------------------------------------------------------------#
# Users use the print function to see what the different data points are
class PrintBehavior(GestureBehavior):
    def __init__(self):
        self.function_name = "print"

    def execute(self):
        super().execute()
    
    def function(self, data):
        print(data)

# Users use the concat function to concatenate the data on the visible markers
class ConcatBehavior(GestureBehavior):
    
    def execute(self):
        super().execute()

class SplitBehavior(GestureBehavior):
    
    def execute(self):
        super().execute()

# Call ChatGPT to process the data into an interesting response
class CallChatGPTBehavior(GestureBehavior):

    def execute(self):
        super().execute()

# Users use the remove function to undo the last action
class UndoBehavior(GestureBehavior):

    def execute(self):
        super().execute()

# Users use the split function to remove components of the data
class SplitBehavior(GestureBehavior):

    def execute(self):
        super().execute()

# Users use the getComponent function to get the type of string the data is
class GetTypeBehavior(GestureBehavior):

    def execute(self):
        super().execute()