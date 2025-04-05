from typing import List, Tuple, Set, Optional

from sudoku import Sudoku


def indentify_if_trans(field: Sudoku, line_num_to_study: int) -> Tuple[List[List[int]], bool]:
    if line_num_to_study < len(field.matrix):
        return field.matrix, False
    else:
        return field.trans_matrix, True


# def find_line_param(sudoku: Sudoku, matrix, line_num_to_study: int) -> (
#         Tuple[List[List[int]],
#         bool,
#         int,
#         List[int],
#         List[int]],
# ):
#     sample, is_trans = indentify_if_trans(sudoku, line_num_to_study)
#     row_num = line_num_to_study if not is_trans else line_num_to_study - len(sudoku.matrix)
#     row = sample[row_num]
#     gap_nums: List[int] = [cell_num for cell_num in range(len(row)) if row[cell_num] == 0]
#     missing_digits = sudoku.find_missing_digits(matrix, row_num)
#     return sample, is_trans, row_num, gap_nums, missing_digits


def search_single_gap_in_square(sudoku: Sudoku) -> None:
    square_to_study: int = sudoku.gaps_per_square.index(1)
    square = sudoku.all_squares[square_to_study]
    print('sq', square)
    gap_coord_in_matrix: List[List[int]] = sudoku.find_gap_coord_in_matrix(square)
    row_num, column_num = gap_coord_in_matrix[0]
    missing_digit: List[int] = sudoku.find_missing_digits(square[2])
    sudoku.new_row_num = row_num
    sudoku.new_column_num = column_num
    sudoku.new_digit, = missing_digit
    print('fill single gap in sq', sudoku.new_row_num, sudoku.new_column_num, sudoku.new_digit)


def find_corresponding_square_index(row_num, column_num) -> Set:
    if row_num < 3:
        possible_indexes_row = {0, 1, 2}
    if 3 <= row_num < 6:
        possible_indexes_row = {3, 4, 5}
    if row_num >= 6:
        possible_indexes_row = {6, 7, 8}
    if column_num < 3:
        possible_indexes_column = {0, 3, 6}
    if 3 <= column_num <= 5:
        possible_indexes_column = {1, 4, 7}
    if column_num >= 6:
        possible_indexes_column = {2, 5, 8}
    return possible_indexes_row.intersection(possible_indexes_column)


        # for column in possible_digit_positions:
        #     if column in range(square[1], square[1] + 3):
        #         positions_to_exclude.add(column)
    # possible_digit_positions = set(possible_digit_positions)
    # possible_digit_positions -= positions_to_exclude
    # print('pos', list(possible_digit_positions))
    # positions_to_exclude = set()

    # for column_num in possible_digit_positions:
    #     square_index, = find_corresponding_square_index(row_num, column_num)  # 0 ... 8
    #     square = sudoku.all_squares[square_index]
    #     if digit in square[2]:
    #         for column in possible_digit_positions:
    #             if column in range(square[1], square[1] + 3):
    #                 positions_to_exclude.add(column)
    #     possible_digit_positions = set(possible_digit_positions)
    #     possible_digit_positions -= positions_to_exclude
    #     print('pos', list(possible_digit_positions))

def digit_is_already_in_square(sudoku, row_num, column_num, digit, matrix):
    if id(matrix) != id(sudoku.matrix):
        square_index, = find_corresponding_square_index(column_num, row_num)  # 0 ... 8
    else:
        square_index, = find_corresponding_square_index(row_num, column_num)  # 0 ... 8
    print('sq ind', square_index)
    print()
    square = sudoku.all_squares[square_index]
    if digit in square[2]:
        return True
    return False


def find_digit_position(sudoku, column_nums_of_gaps_in_row, missing_digits, matrix, row_num) -> Optional[int]:
    for digit in missing_digits:
        possible_digit_positions = []
        for column_num in column_nums_of_gaps_in_row:
            # print('digit', digit)
            print('rownum', row_num, 'colnum', column_num)
            print('bool - absence in perpen', digit not in sudoku.extract_perpen_line(matrix, column_num))
            print('bool - absence in sq', not digit_is_already_in_square(sudoku, row_num, column_num, digit, matrix))

            # print()
            if digit not in sudoku.extract_perpen_line(matrix, column_num) and not digit_is_already_in_square(sudoku, row_num, column_num, digit, matrix):
                possible_digit_positions.append(column_num)
        # print('possible_digit_positions', possible_digit_positions)
        if len(possible_digit_positions) == 1:
            column_num, = possible_digit_positions
            sudoku.new_row_num = row_num
            sudoku.new_column_num = column_num
            sudoku.new_digit = digit
            print('row col dig:', row_num, column_num, '|', digit)
            return True
    print('appropriate value not found')
    return False


def search_multi_gap_in_lines(sudoku: Sudoku, matrix):
    print('&', sudoku.gap_number_in_line(matrix))
    # TODO ПРИКРУТИТЬ поиск от минимального числа гэпов
    for row_num in range(sudoku.size):
        row = matrix[row_num]
        missing_digits = sudoku.find_missing_digits(row)
        if len(missing_digits) >= 2:
            empty_columns_nums: List[int] = [column_num for column_num in range(sudoku.size) if row[column_num] == 0]
            if find_digit_position(sudoku, empty_columns_nums, missing_digits, matrix, row_num):
                print('value found')
                print('id(matrix)', id(matrix), 'id(sudoku.matrix)', id(sudoku.matrix), 'id(sudoku.transposed_matrix)', id(sudoku.transposed_matrix))
                if id(matrix) != id(sudoku.matrix):
                    shuttle = sudoku.new_column_num
                    sudoku.new_column_num = sudoku.new_row_num
                    sudoku.new_row_num = shuttle  # todo для транс нужно еще убедиться что правильно ищутся квадраты
                #     print('trans, RC D', sudoku.new_row_num, sudoku.new_column_num, '|', sudoku.new_digit)
                #     return
                return True
                # if id(matrix) == id(sudoku.matrix):
                #     print('non trans, RC D', sudoku.new_row_num, sudoku.new_column_num, '|', sudoku.new_digit)
                #     return
                #
    return False


# def search_multi_gap_in_squares(sudoku: Sudoku):
#     for square in sudoku.all_squares:
#         gap_coord_in_matrix: List[List[int]] = sudoku.find_gap_coord_in_matrix(square)
#         missing_digits: List[int] = sudoku.find_missing_digits(square[2])
#         for digit in missing_digits:
#             undefined_cells = [coord for coord in gap_coord_in_matrix
#                                if digit not in sudoku.find_cross_row_column(coord)]
#             if len(undefined_cells) == 1:
#                 row_num, column_num = undefined_cells[0]
#                 sudoku.new_column_num = row_num
#                 sudoku.new_column_num = column_num
#                 sudoku.new_digit = digit
#                 return True
#             else:
#                 continue
#     return False


def find_gaps(sudoku: Sudoku):
    # sudoku.transposed_matrix = sudoku.find_transposed
    if 1 in sudoku.gap_number_in_line(sudoku.matrix):
        sudoku.find_single_gap_in_line(sudoku.matrix)
        print('single gap')
        return
    elif 1 in sudoku.gap_number_in_line(sudoku.find_transposed):
        sudoku.find_single_gap_in_line(sudoku.find_transposed)
        shuttle = sudoku.new_row_num
        sudoku.new_row_num = sudoku.new_column_num
        sudoku.new_column_num = shuttle
        print('single gap - trans')
        return
    elif 1 in sudoku.gaps_per_square:
        search_single_gap_in_square(sudoku)
        print('single gap in sq')
        return
    else:
        if search_multi_gap_in_lines(sudoku, sudoku.matrix):
            print('Multi lines')
            # print('vars', [var is not None for var in (sudoku.new_row_num, sudoku.new_column_num, sudoku.new_digit)])
            return
        if search_multi_gap_in_lines(sudoku, sudoku.find_transposed):
            print('Multi lines - Trans')
            return
    sudoku.new_row_num = None
    sudoku.new_column_num = None
    sudoku.new_digit = None
