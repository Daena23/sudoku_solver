from tkinter.constants import RAISED

from sudoku import Sudoku
from main_func import find_gaps
from samples import (
    hard_sudoku_1,
    hard_sudoku_1_solved,
    easy_sudoku_1_solved,
    easy_sudoku_1,
)


def main():
    sudoku = Sudoku(hard_sudoku_1)
    solved_sudoku = hard_sudoku_1_solved
    move_counter = 0
    # todo remove sq index sq [0, 0, [1, 2, 3, 9, 4, 5, 0, 7, 6]]
    while not sudoku.is_solved():
        sudoku.visualize(sudoku.matrix)
        find_gaps(sudoku)
        print(f'TRRRrow: {sudoku.new_row_num}, column: {sudoku.new_column_num}, missing digit: {sudoku.new_digit}')
        if None in (sudoku.new_row_num, sudoku.new_column_num, sudoku.new_digit):
            print('Can\'t solve this sudoku :(')
            break
        # print(f'TRRRrow: {sudoku.new_row_num}, column: {sudoku.new_column_num}, missing digit: {sudoku.new_digit}')
        assert sudoku.matrix[sudoku.new_row_num][sudoku.new_column_num] == 0
        sudoku.matrix[sudoku.new_row_num][sudoku.new_column_num] = sudoku.new_digit
        move_counter += 1
        if move_counter == 100:
            break
        print('accum', sum([sudoku.matrix[row_num][column_num] for column_num in range(sudoku.size) for row_num in range(sudoku.size)]))
        sudoku.new_row_num = None
        sudoku.new_column_num = None
        sudoku.new_digit = None

    if sudoku.is_solved():
        print(f'SOLVED in {move_counter} moves')
        sudoku.visualize(sudoku.matrix)
    # Test
    if sudoku.matrix == solved_sudoku:
        print('Correct answer')
    else:
        print('Wrong answer')


if __name__ == '__main__':
    main()
