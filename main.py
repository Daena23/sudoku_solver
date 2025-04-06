from sudoku import Sudoku
from main_func import define_gap
from samples import (
    very_hard_sudoku,
    hard_sudoku,
    easy_sudoku,
)


def main():
    our_sudoku = hard_sudoku
    sudoku = Sudoku(our_sudoku['unsolved'])
    sudoku.solved = our_sudoku['solved']
    move_counter = 0
    while not sudoku.is_solved():
        sudoku.visualize(sudoku.matrix)
        define_gap(sudoku)
        if None in (sudoku.row_index, sudoku.column_index, sudoku.digit):
            break
        print(f'-> new move: {sudoku.row_index}, column: {sudoku.column_index}, missing digit: {sudoku.digit}')
        sudoku.matrix[sudoku.row_index][sudoku.column_index] = sudoku.digit
        move_counter += 1

    sudoku.final_message(move_counter)


if __name__ == '__main__':
    main()
