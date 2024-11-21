from typing import List, Tuple

from field import Field


def indentify_if_trans(field: Field, line_num_to_study: int) -> Tuple[List[List[int]], bool]:
    if line_num_to_study < len(field.matrix):
        return field.matrix, False
    else:
        return field.trans_matrix, True


def find_line_param(field: Field, line_num_to_study: int) -> (
        Tuple[List[List[int]],
        bool,
        int,
        List[int],
        List[int]],
):
    sample, is_trans = indentify_if_trans(field, line_num_to_study)
    row_num = line_num_to_study if not is_trans else line_num_to_study - len(field.matrix)
    row = sample[row_num]
    gap_nums: List[int] = [cell_num for cell_num in range(len(row)) if row[cell_num] == 0]
    missing_digits = field.find_missing_digits(row)
    return sample, is_trans, row_num, gap_nums, missing_digits


def search_single_gap_in_line(field: Field) -> Tuple[int, int, int]:
    line_num_to_study = field.gap_in_lines.index(1)
    sample, is_trans, row_num, gap_nums, digit = find_line_param(field, line_num_to_study)
    cell_num = sample[row_num].index(0)
    if is_trans:
        row_num, cell_num = cell_num, row_num
    return row_num, cell_num, *digit


def search_single_gap_in_square(field: Field) -> Tuple[int, int, int]:
    square_to_study = field.gaps_per_square.index(1)
    square = field.all_squares[square_to_study]
    gap_coord_in_matrix: List[List[int]] = field.find_gap_coord_in_matrix(square)
    row_num, cell_num = gap_coord_in_matrix[0]
    missing_digit: List[int] = field.find_missing_digits(square[2])
    return row_num, cell_num, *missing_digit


def search_multi_gap_in_lines(field: Field):
    for line_num_to_study in range(len(field.gap_in_lines)):
        sample, is_trans, row_num, gap_nums, missing_digits = find_line_param(field, line_num_to_study)
        for digit in missing_digits:
            undefined_cells = [cell_num for cell_num in gap_nums
                               if digit not in field.extract_perpen_line(sample, cell_num)]
            if len(undefined_cells) == 1:
                cell_num = undefined_cells[0]
                if is_trans:
                    row_num, cell_num = cell_num, row_num
                else:
                    row_num = row_num
                return row_num, cell_num, digit
            else:
                continue
    return None, None, None


def search_multi_gap_in_squares(field: Field):
    for square in field.all_squares:
        gap_coord_in_matrix: List[List[int]] = field.find_gap_coord_in_matrix(square)
        missing_digits: List[int] = field.find_missing_digits(square[2])
        for digit in missing_digits:
            undefined_cells = [coord for coord in gap_coord_in_matrix
                               if digit not in field.find_cross_row_column(coord)]
            if len(undefined_cells) == 1:
                row_num, cell_num = undefined_cells[0]
                return row_num, cell_num, digit
            else:
                continue
    return None, None, None


def find_missing_digit(field: Field) -> Tuple[int, int, int]:
    if 1 in field.gap_in_lines:
        return search_single_gap_in_line(field)
    elif 1 in field.gaps_per_square:
        return search_single_gap_in_square(field)
    else:
        row_num_to_fill, cell_num_to_fill, digit = search_multi_gap_in_lines(field)
        if None in (row_num_to_fill, cell_num_to_fill, digit):
            row_num_to_fill, cell_num_to_fill, digit = search_multi_gap_in_squares(field)
    return row_num_to_fill, cell_num_to_fill, digit
