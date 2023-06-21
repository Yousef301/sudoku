import re
import time
from abc import ABC

import sudoku
from abstract import Abstract


class OPM(Abstract, ABC):
    _board = None
    _solvedBoard = None
    _points = 0
    _score = 0

    def create_puzzle(self):  # Build the puzzle
        choice = input("Generate random sudoku board [G], Load a board from a file [F] and [E] for exit: ").upper()
        while choice not in ["G", "F", "E"]:
            choice = input("Generate random sudoku board [G], Load a board from a file [F] and [E] for exit: ").upper()

        if choice == "F":  # This option is to read the board from a file
            try:  # Checking if the file is exist
                file = input("Enter file name: ")
                data = open(file, "r")
                num_lines = sum(1 for line in open(file))
                if num_lines != 9:
                    print('\033[91m', end="")
                    print("Check the format of the puzzle inside the file...")
                    exit()
                for line in data:
                    for char in line:
                        if char not in ["1", "2", "3", "4", "5", "6", "7", "8",
                                        "9"] and char != "," and char != "\n":
                            print('\033[91m', end="")
                            print("Check the format of the puzzle inside the file...")
                            exit()
                data.seek(0)
                self._board = sudoku.board_from_file(data)
            except FileNotFoundError:
                print("File not found")
                file = input("Renter file name: ")
                data = open(file, "r")
                self._board = sudoku.board_from_file(data)

        elif choice == "G":  # this option to generate a board ready to be solve
            emp_cells = None
            difficulty = input("Enter the difficulty [E/M/H]:").upper()
            while difficulty not in ["E", "M", "H"]:
                difficulty = input("Enter the difficulty [E/M/H]:").upper()
            if difficulty == "E":
                emp_cells = int(81 - 0.4 * 81)
            elif difficulty == "M":
                emp_cells = int(81 - 0.25 * 81)
            elif difficulty == "H":
                emp_cells = int(81 - 0.1 * 81)

            self._board = sudoku.auto_board(emp_cells)
        else:
            exit(1)

    def fill_value(self,
                   points):  # Take an empty cell pos and a value from the user and fill it after check if it is valid
        values = input("Please enter the value,row and column as following (v,r,c): ")
        while not re.match("[1-9],[0-9],[0-9]", values[1:len(values) - 1]):
            values = input("Please enter the value,row and column as following (v,r,c): ")
        values = tuple(int(num) for num in values[1:len(values) - 1].split(","))
        if sudoku.valid(self._board, values[0], values[1::]):
            self._board[values[1]][values[2]] = values[0]
            points += 1
        else:
            if points > 0:
                points -= 1
            print("Invalid value...")
        return points

    def hint(self, points):  # Fill an empty cell with a valid value
        self._board, value, row, column = sudoku.hint(self._board)
        sudoku.print_board(self._board)
        points -= 2
        print(f"cell ({row},{column}) has been filled with value {value}")
        return points

    def solve_sudoku(self):  # Solve the whole puzzle
        sudoku.solve(self._board)
        if sudoku.find_empty(self._board):
            print("\nThere is no solution for this board ^_^")
        else:
            print("\n========SOLUTION========")
            self.print_board()

    def calculate_score(self, t, points):  # Calculate player final score
        if points > 0:
            self._score = int((points / 81) * (3600 / t))
        else:
            self._score = 0

    def print_board(self):
        sudoku.print_board(self._board)

    def points_score_board(self):
        return self._points, self._score, self._board

    def run_game(self):  # This method used to run the game and do a lot of other things......
        self.create_puzzle()
        print("\nYou have the following options:\n(Fill) to fill a specific cell.\n(Hint) to fill an empty "
              "cell automatically with valid value (COST 2 POINTS).\n(Solve) to solve the whole puzzle.\n(Exit) to "
              "end the game" + '\033[0m')
        start_time = time.time()
        while sudoku.find_empty(self._board):
            print()
            self.print_board()
            print(f"Points: {self._points}\n")
            choice = input("Your choice: ").upper()
            while choice not in ["FILL", "HINT", "SOLVE", "EXIT"]:
                choice = input("Your choice: ").upper()
            if choice == "FILL":
                self._points = self.fill_value(self._points)
            elif choice == "HINT":
                if self._points > 1:
                    self._points = self.hint(self._points)
                    print(f"Points: {self._points}\n")
                else:
                    print(f"You don't have enough point to get a hint. (Points: {self._points})\n")
            elif choice == "SOLVE":
                self.solve_sudoku()
                break
            else:
                break
        time_taken = time.time() - start_time
        self.calculate_score(time_taken, self._points)

        print(
            '\033[1m' + f"\n\nSudoku puzzle has been solved\nYour points: {self._points}\t\tYour score: {self._score}\n"
                        f"Time taken to solve the puzzle: {int(time_taken)} second")
