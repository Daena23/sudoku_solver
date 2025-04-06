from typing import Set, List


def find_index_of_square(row_num: int, column_num: int) -> Set:
    possible_row_indexes = set()
    possible_column_indexes = set()
    if row_num < 3:
        possible_row_indexes = {0, 1, 2}
    if 3 <= row_num < 6:
        possible_row_indexes = {3, 4, 5}
    if row_num >= 6:
        possible_row_indexes = {6, 7, 8}
    if column_num < 3:
        possible_column_indexes = {0, 3, 6}
    if 3 <= column_num <= 5:
        possible_column_indexes = {1, 4, 7}
    if column_num >= 6:
        possible_column_indexes = {2, 5, 8}
    return possible_row_indexes.intersection(possible_column_indexes)


def find_missing_digits(row: List[int]) -> Set:
    all_digits = {*range(1, 10)}
    present_digits = set(row)
    all_digits -= present_digits
    return all_digits


def convert_linear_coord_to_matrix_coord(square, zero_column_indexes: List[int]) -> List[List[int]]:
    gap_coord_in_matrix = []
    square_corner_row_index = square['row_index']
    square_corner_column_index = square['column_index']
    for zero_column_index in zero_column_indexes:
        row_suppl, column_suppl = zero_column_index // 3, zero_column_index % 3
        row_index, column_index = square_corner_row_index + row_suppl, square_corner_column_index + column_suppl
        gap_coord_in_matrix.append([row_index, column_index])
    return gap_coord_in_matrix


def extract_perpendicular_line(matrix: List[List[int]], column_index: int) -> List[int]:
    return [row[column_index] for row in matrix]


def swap_row_column(sudoku) -> None:
    carrier = sudoku.column_index
    sudoku.column_index = sudoku.row_index
    sudoku.row_index = carrier
