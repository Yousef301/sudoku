import time

import sudoku
from one_player_mode import OPM


class TPM(OPM):  # Inherit OPM class to use its methods
    _point1 = 0
    _point2 = 0
    _score1 = 0
    _score2 = 0

    def calculate_score(self, t, points):  # Override calculate_score function and do some edits on it
        if points[0] > 0:
            self._score1 = int((points[0] / 81) * ((t[0] + t[1]) / t[0]))
        else:
            self._score1 = 0
        if points[1] > 0:
            self._score2 = int((points[1] / 81) * ((t[0] + t[1]) / t[1]))
        else:
            self._score2 = 0

    def points_score_board(self):
        return (self._point1, self._point2), (self._score1, self._score2), self._board

    def run_game(self):  # Override this function and doing some edits to corresponds with it
        pass_cnt = 0
        p1_time = 0
        p2_time = 0
        player = 1
        self.create_puzzle()
        print("\nYou guys have the following options:\n(Fill) to fill a specific cell.\n(Hint) to fill an empty "
              "cell automatically with valid value (COST 2 POINTS).\n(Pass) to pass turn to the other player"
              " (COST 1 POINT).\n(Solve) to solve the whole puzzle.\n(Exit) to end the game.")
        while sudoku.find_empty(self._board):  # while loop until fill all empty cells
            if player == 1:
                start_time = time.time()
                print('\033[1m' + "\n ==>PLAYER ONE TURN<==" + '\033[0m')
                self.print_board()
                print(f"Player one points: {self._point1}\nPlayer two points: {self._point2}\n")
                choice = input("Your choice: ").upper()
                while choice not in ["FILL", "HINT", "SOLVE", "PASS", "EXIT"]:
                    choice = input("Your choice: ")
                if choice == "FILL":
                    self._point1 = self.fill_value(self._point1)
                    player = 2
                    pass_cnt = 0
                elif choice == "HINT":
                    if self._point1 > 1:
                        self._point1 = self.hint(self._point1)
                        player = 2
                        pass_cnt = 0
                    else:
                        print(f"You don't have enough point to get a hint. (Points: {self._point1})\n")
                elif choice == "PASS":
                    if self._point1 > 0:
                        self._point1 -= 1
                        player = 2
                        pass_cnt += 1
                    else:
                        print("You don't have points to pass the round")
                elif choice == "SOLVE":
                    self.solve_sudoku()
                    pass_cnt = 0
                else:
                    break
                turn_time = time.time() - start_time
                p1_time += turn_time
                if pass_cnt == 4:
                    self.hint(1)
            else:
                start_time = time.time()
                print('\033[1m' + "\n ==>PLAYER TWO TURN<==" + '\033[0m')
                self.print_board()
                print(f"Player one points: {self._point1}\nPlayer two points: {self._point2}\n")
                choice = input("Your choice: ").upper()
                while choice not in ["FILL", "HINT", "SOLVE", "PASS", "PRINT", "EXIT"]:
                    choice = input("Your choice: ")
                if choice == "FILL":
                    self._point2 = self.fill_value(self._point2)
                    player = 1
                    pass_cnt = 0
                elif choice == "HINT":
                    if self._point2 > 1:
                        self._point2 = self.hint(self._point2)
                        player = 1
                        pass_cnt = 0
                    else:
                        print(f"You don't have enough point to get a hint. (Points: {self._point2})\n")
                elif choice == "PASS":
                    if self._point2 > 0:
                        self._point2 -= 1
                        player = 1
                        pass_cnt += 1
                    else:
                        print("You don't have points to pass the round")
                elif choice == "SOLVE":
                    self.solve_sudoku()
                    pass_cnt = 0
                elif choice == "PRINT":
                    self.print_board()
                    pass_cnt = 0
                else:
                    break
                turn_time = time.time() - start_time
                p2_time += turn_time
                if pass_cnt == 4:
                    self.hint(1)
        p1_time = int(p1_time)
        p2_time = int(p2_time)
        self.calculate_score((p1_time, p2_time), (self._point1, self._point2))  # Calculate the score
        print(  # Print the results for both players
            '\033[1m' + f"\nResults:\n==>Player One<==\nPoints: {self._point1}\t\tScore: {self._score1}\nTime: {p1_time} second\n"
                        f"==>Player Two<==\nPoints: {self._point2}\t\tScore: {self._score2}\nTime: {p2_time} second")
