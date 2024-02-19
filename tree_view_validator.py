import pandas as pd
from abc import ABC, abstractmethod
import config


class BaseStrategy(ABC):
    @abstractmethod
    def prepare(self, data):
        pass


class WithoutZeroData(BaseStrategy):
    def prepare(self, data) -> pd.DataFrame:
        vertices = []
        values = []

        for vertex in data:
            for neighbor, value in data[vertex].items():
                if value != 0:
                    vertices.append(f'{vertex}->{neighbor}')
                    values.append(value)

        return pd.DataFrame({config.TEXT_COLUMN_VERTICES: vertices, config.TEXT_COLUMN_VALUE: values})


class AnyData(BaseStrategy):
    def prepare(self, data) -> pd.DataFrame:
        vertices = []
        values = []

        for vertex in data:
            for neighbor, value in data[vertex].items():
                vertices.append(f'{vertex}->{neighbor}')
                values.append(value)

        return pd.DataFrame({config.TEXT_COLUMN_VERTICES: vertices, config.TEXT_COLUMN_VALUE: values})


class TreeViewDataPreparer:
    def __init__(self, strategy: BaseStrategy = WithoutZeroData()):
        self.__strategy = strategy

    def prepare_data(self, data):
        return self.__strategy.prepare(data)

    @property
    def strategy(self):
        raise RuntimeError('Can\'t get strategy')

    @strategy.setter
    def strategy(self, value: BaseStrategy):
        if issubclass(type(value), BaseStrategy):
            self.__strategy = value
        else:
            raise Exception(f'Value {value} should be subclass of {BaseStrategy}')
