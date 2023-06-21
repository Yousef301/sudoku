import itertools
import random


def attempt_board():  # Generate a random board
    n = 9
    numbers = list(range(1, n + 1))
    boards = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    for i, j in itertools.product(range(n), repeat=2):
        i0, j0 = i - i % 3, j - j % 3  # origin of 3x3 block
        random.shuffle(numbers)
        for x in numbers:
            if (x not in boards[i]  # row
                    and all(row[j] != x for row in boards)  # column
                    and all(x not in row[j0:j0 + 3]  # block
                            for row in boards[i0:i])):
                boards[i][j] = x
                break
        else:
            return None
    return boards


def makeBoard():  # This method is used to keep generate a sudoku board until getting a valid one
    boards = None
    while boards is None:
        boards = attempt_board()
    return boards


def remove_num(boards, cells):  # Empty cells from generated board to get a ready to play board
    cnt = 0
    while cnt < cells:
        column = random.randint(0, 8)
        row = random.randint(0, 8)
        if boards[row][column] != 0:
            boards[row][column] = 0
            cnt += 1
    return boards


def auto_board(difficulty):  # Generate a board that is ready to play
    board = makeBoard()
    board = remove_num(board, difficulty)
    return board


def board_from_file(file):  # Read board from a file
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]
    column_cnt = 0
    row_cnt = 0

    for line in file:
        if line[0] == ",":
            line = "0" + line[::]
        line = line.replace(",,", ",0,")
        line = line.replace(",,", ",0,")
        for char in line:
            if char.isdigit():
                board[row_cnt][column_cnt] = int(char)
                column_cnt += 1
        row_cnt += 1
        column_cnt = 0
    return board


def find_empty(boards):  # Find an empty cell and return its position
    for i in range(len(boards)):
        for j in range(len(boards[0])):
            if boards[i][j] == 0:
                return i, j  # row, col
    return None


def valid(boards, num, pos):  # Checking if the entered value in the chosen pos are valid
    # Check row
    for i in range(len(boards[0])):
        if boards[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(boards)):
        if boards[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if boards[i][j] == num and (i, j) != pos:
                return False
    return True


def hint(boards):  # Fill an empty cell with valid value
    row, column = find_empty(boards)
    value = random.randint(1, 9)
    while not valid(boards, value, (row, column)):
        value = random.randint(1, 9)
    boards[row][column] = value
    return boards, value, row, column


def solve(boards):  # Solve the whole board
    find = find_empty(boards)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(boards, i, (row, col)):
            boards[row][col] = i

            if solve(boards):
                return True

            boards[row][col] = 0
    return False


def print_board(boards):  # Printing the board
    for i in range(len(boards)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(boards[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                if boards[i][j] == 0:
                    print('\033[91m' + str(boards[i][j]) + '\033[0m')
                else:
                    print(boards[i][j])
            else:
                if boards[i][j] == 0:
                    print('\033[91m' + str(+boards[i][j]) + " ", end="" + '\033[0m')
                else:
                    print(str(+boards[i][j]) + " ", end="")
