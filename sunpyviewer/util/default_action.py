from abc import ABC, abstractmethod


class ActionController(ABC):

    @staticmethod
    @abstractmethod
    def getItemConfig():
        pass

    @abstractmethod
    def doAction(self, viewer_ctrl):
        pass
