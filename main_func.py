from sudoku import Sudoku
from utils import swap_row_column


def define_gap(sudoku: Sudoku) -> None:
    if sudoku.is_single_gap_in_line(sudoku.matrix):
        sudoku.define_single_gap_in_line(sudoku.matrix)
        return
    elif sudoku.is_single_gap_in_line(sudoku.transposed):
        sudoku.define_single_gap_in_line(sudoku.transposed)
        swap_row_column(sudoku)
        return
    elif sudoku.is_single_gap_in_square:
        sudoku.define_single_gap_in_square()
        return
    elif sudoku.define_gap_among_several(sudoku.matrix):
        return
    elif sudoku.define_gap_among_several(sudoku.transposed):
        return
    sudoku.row_index = None
    sudoku.column_index = None
    sudoku.digit = None
