# Abstract class contain most of used methods in one_player_mode class as an abstract methods
from abc import abstractmethod, ABC


class Abstract(ABC):
    @abstractmethod
    def create_puzzle(self):
        pass

    @abstractmethod
    def calculate_score(self, t, points):
        pass

    @abstractmethod
    def print_board(self):
        pass

    @abstractmethod
    def fill_value(self, points):
        pass

    @abstractmethod
    def hint(self, points):
        pass

    @abstractmethod
    def solve_sudoku(self):
        pass

    @abstractmethod
    def run_game(self):
        pass

    @abstractmethod
    def points_score_board(self):
        pass
