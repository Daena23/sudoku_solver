from typing import List, Tuple

from field import Field


def indentify_if_trans(field, line_num_to_study):
    if line_num_to_study < len(field.matrix):
        return field.matrix, False
    else:
        return field.trans_matrix, True


def find_line_to_fill_stats(field: Field, line_num_to_study: int) -> Tuple[Field, bool, List[int], List[int]]:
    sample, is_transponated = indentify_if_trans(field, line_num_to_study)
    row = sample[line_num_to_study] if not is_transponated else sample[line_num_to_study - len(field.matrix)]
    gap_nums: List[int] = [cell_num for cell_num in range(len(row)) if row[cell_num] == 0]
    missing_digits = field.find_missing_digits(row)
    return sample, is_transponated, gap_nums, missing_digits


def search_gap_in_lines(field):
    for line_num_to_study in range(len(field.all_gaps_in_lines)):
        sample, is_trans, gap_nums, missing_digits = find_line_to_fill_stats(field, line_num_to_study)
        row_num = line_num_to_study if not is_trans else line_num_to_study - len(field.matrix)
        for digit in missing_digits:
            undefined_cells = [cell_num for cell_num in gap_nums if digit not in field.extract_perpen_line(sample, cell_num)]
            if len(undefined_cells) == 1:
                cell_num_to_fill = undefined_cells[0]
                if is_trans:
                    row_num_to_study, cell_num_to_fill = cell_num_to_fill, row_num
                else:  # todo i7 неправильно
                    row_num_to_study = row_num
                print('(undefined_cells)', undefined_cells, 'Line: enDD: row_num', row_num_to_study, 'cell_num', cell_num_to_fill, 'digit', digit, 'is_trans', is_trans)
                return row_num_to_study, cell_num_to_fill, digit
            else:
                continue
    return None, None, None


def search_gap_in_squares(field):
    for square in field.all_squares:
        gap_coord_in_matrix: List[List[int]] = field.find_gap_coord_in_matrix(square)
        missing_digits: List[int] = field.find_missing_digits(square[2])
        for digit in missing_digits:
            undefined_cells = [coord for coord in gap_coord_in_matrix if digit not in field.find_cross_row_column(coord)]
            if len(undefined_cells) == 1:  # todo правильно или нет
                row_num_to_study, cell_num_to_fill = undefined_cells[0]
                print('square enD: row_num', row_num_to_study, 'cell_num', cell_num_to_fill, 'digit', digit)
                return row_num_to_study, cell_num_to_fill, digit
            else:
                continue
    return None, None, None


def fill_multiple_gaps(field: Field):
    # todo поичк по единичным

    row_num_to_study, cell_num_to_fill, digit = search_gap_in_lines(field)
    if None in (row_num_to_study, cell_num_to_fill, digit):
        row_num_to_study, cell_num_to_fill, digit = search_gap_in_squares(field)
    return row_num_to_study, cell_num_to_fill, digit


def update_matrix(field: Field, row_num: int, cell_num: int, missing_digit):
    field.matrix[row_num][cell_num] = missing_digit
