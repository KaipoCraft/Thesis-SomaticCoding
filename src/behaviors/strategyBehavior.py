from abc import ABC, abstractmethod

@abstractmethod
class GestureBehavior(ABC):
    def __init__(self, gestureCommand) -> None:
        self.gestureCommand = gestureCommand

    def execute(self):
        self.gestureCommand.process()

#------------------------------------------------------------#

# Users use the print function to see what the different data points are
class PrintBehavior(GestureBehavior):
    def __init__(self, gestureCommand) -> None:
        super().__init__(gestureCommand)
    
    def execute(self):
        super().execute()

# Users use the concat function to concatenate the data on the visible markers
class ConcatBehavior(GestureBehavior):
    def __init__(self, gestureCommand) -> None:
        super().__init__(gestureCommand)
    
    def execute(self):
        super().execute()

# Call ChatGPT to process the data into an interesting response
class CallChatGPTBehavior(GestureBehavior):
    def __init__(self, gestureCommand) -> None:
        super().__init__(gestureCommand)
    
    def execute(self):
        super().execute()

# Users use the remove function to undo the last action
class UndoBehavior(GestureBehavior):
    def __init__(self, gestureCommand) -> None:
        super().__init__(gestureCommand)
    
    def execute(self):
        super().execute()

# Users use the split function to remove components of the data
class SplitBehavior(GestureBehavior):
    def __init__(self, gestureCommand) -> None:
        super().__init__(gestureCommand)
    
    def execute(self):
        super().execute()

# Users use the getComponent function to get the type of string the data is
class GetTypeBehavior(GestureBehavior):
    def __init__(self, gestureCommand) -> None:
        super().__init__(gestureCommand)
    
    def execute(self):
        super().execute()