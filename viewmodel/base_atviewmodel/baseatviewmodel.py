#-----------------------------------------------------------------------------+
from abc import ABC, abstractmethod


class BaseATViewModel(ABC):

    @abstractmethod
    def get_filepath(self):
        raise NotImplementedError
    

