# CS 131 A4 Constraint Satisfaction Problem
# Written by: Perucy Mussiba
# Date: 20th March 2024
# Purpose: The algorithm below implements backtracking algorithm to solve a Sudoku puzzle


# Purpose: This function checks if a number in a cell of the sudoku puzzle is valid
#           by checking the corresponding row, column and 3 X 3 region if the number occurs only once
def is_num_valid(board, row, column, value):
    # loops through each cell in a row and checks if the value already pre-exists in the row
    # returns false meaning the number in a cell is invalid, otherwise it proceeds to the next code block
    for x in range(9):
        if board[row][x] == value:
            return False

    # loops through each cell in a column and checks if the value already pre-exists in the column
    # returns false meaning the number in a cell is invalid, otherwise it proceeds to the next code block
    for y in range(9):
        if board[y][column] == value:
            return False

    # determines the starting position of a 3 X 3 region to check if the numbers in cells are valid
    init_row = row - row % 3
    init_col = column - column % 3

    # loops through the rows and columns of a 3 X 3 region and returns false if a number already
    # pre-exists in the region
    for i in range(3):
        for p in range(3):
            if board[i + init_row][p + init_col] == value:
                return False

    # returns true when all cells have valid numbers
    return True


# Purpose: main loop that fills a number in cells marked as '0' in a 2D array (board) and calls a function that
#           checks if the number in a cell is valid
def solve_sudoku(board):
    # loops through the board (2D-array) and checks if the number in a cell is 0
    for i in range(9):
        for q in range(9):
            if board[i][q] == 0:
                # loops through numbers from 1 to 9 and calls a function to check if each possible number to be
                # filled in a cell is valid then it recursively call solve_sudoku with the new board
                for val in range(1, 10):
                    if is_num_valid(board, i, q, val):
                        board[i][q] = val
                        if solve_sudoku(board):
                            return True
                        board[i][q] = 0
                # returns false if the sudoku puzzle cannot be solved
                return False

    # returns true when the sudoku puzzle is solved
    return True


# main function
if __name__ == "__main__":
    # initializing a 2D list for the sudoku puzzle
    # 0 represents an empty cell

    # easy puzzle
    puzzle = [
        [6, 0, 8, 7, 0, 2, 1, 0, 0],
        [4, 0, 0, 0, 1, 0, 0, 0, 2],
        [0, 2, 5, 4, 0, 0, 0, 0, 0],
        [7, 0, 1, 0, 8, 0, 4, 0, 5],
        [0, 8, 0, 0, 0, 0, 0, 7, 0],
        [5, 0, 9, 0, 6, 0, 3, 0, 1],
        [0, 0, 0, 0, 0, 6, 7, 5, 0],
        [2, 0, 0, 0, 9, 0, 0, 0, 8],
        [0, 0, 6, 8, 0, 5, 2, 0, 3]
    ]

    """"
    # difficult puzzle
    puzzle = [
        [0, 7, 0, 0, 4, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 8, 6, 1, 0],
        [3, 9, 0, 0, 0, 0, 0, 0, 7],
        [0, 0, 0, 0, 0, 4, 0, 0, 9],
        [0, 0, 3, 0, 0, 0, 7, 0, 0],
        [5, 0, 0, 1, 0, 0, 0, 0, 0],
        [8, 0, 0, 0, 0, 0, 0, 7, 6],
        [0, 5, 4, 8, 0, 0, 0, 0, 0],
        [0, 0, 0, 6, 1, 0, 0, 5, 0]
    ]

    # arto inkala's puzzle
    puzzle = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]
    """""
    if solve_sudoku(puzzle):
        for cell in puzzle:
            print(cell)
    else:
        print("The Sudoku puzzle could not be solved")
