from typing import List, Union

from auxiliary_func import find_row_cell_suppl


class Field:
    def __init__(self, sample):
        self.matrix = sample

    @property
    def all_gaps_in_lines(self) -> List[int]:
        gaps_in_rows = self.gaps_per_line[0]
        gaps_in_columns = self.gaps_per_line[1]
        return gaps_in_rows + gaps_in_columns

    @property
    def gaps_per_line(self) -> List[List[int]]:
        gaps_in_rows = [row.count(0) for row in self.matrix]
        gaps_in_columns = [row.count(0) for row in self.trans_matrix]
        return [gaps_in_rows, gaps_in_columns]

    @property
    def all_squares(self) -> List[List[int]]:
        square_slices = [n for n in range(len(self.matrix)) if n % 3 == 0]
        all_squares = []
        for row_num in square_slices:
            for cell_num in square_slices:
                rows = self.matrix[row_num: row_num + 3]
                square = []
                for row in rows:
                    square.extend(row[cell_num: cell_num + 3])
                all_squares.append([row_num, cell_num, square])
        return all_squares

    def find_gap_coord_in_matrix(self, square) -> List[List[int]]:
        init_row, init_column, line = square
        gap_nums_in_line = [cell_num for cell_num in range(len(line)) if line[cell_num] == 0]
        gap_coord_in_matrix = self.convert_coord_line_to_matrix(square, gap_nums_in_line)
        return gap_coord_in_matrix

    def convert_coord_line_to_matrix(self, square: List, gap_nums_in_line) -> List[List[int]]:
        gaps_coord = []
        line = square[2]
        for cell_num_in_line in gap_nums_in_line:
            row_suppl, cell_suppl = find_row_cell_suppl(cell_num_in_line)
            row_num, cell_num = square[0] + row_suppl, square[1] + cell_suppl
            gaps_coord.append([row_num, cell_num])
        return gaps_coord

    def find_missing_digits(self, line) -> Union[int, List[int]]:
        return [digit for digit in range(1, len(self.matrix) + 1) if digit not in line]

    def extract_perpen_line(self, sample, cell_num: int) -> List[int]:
        return [row[cell_num] for row in sample]

    def find_cross_row_column(self, coord):
        print('coord', coord)
        row_num, cell_num = coord[0], coord[1]
        row_cells = self.matrix[row_num]
        column_cells = [row[cell_num] for row in self.matrix]
        cross_row_column = row_cells + column_cells
        print('row_cells.extend(column_cells)', cross_row_column)
        return cross_row_column

    def visualize_matrix(self) -> None:
        print('  ', end=' ')
        for num in range(len(self.matrix)):
            print(num, end='  ')
        print()
        for row_num in range(len(self.matrix)):
            print(row_num, end=' ')
            print(self.matrix[row_num])

    def check_win_condition(self) -> bool:
        return all([all([cell != 0 for cell in row]) for row in self.matrix])

    @property
    def trans_matrix(self) -> List[List[int]]:
        return [[self.matrix[row][column] for row in range(len(self.matrix))] for column in range(len(self.matrix))]

    def find_gaps_per_square(self) -> List[List[int]]:
        return [row.count(0) for row in self.matrix]

    def find_rows_to_explore(self, empty_cell_per_line: List[int]) -> List[int]:
        rows_to_explore = []
        for cell_num in range(len(empty_cell_per_line)):
            if empty_cell_per_line[cell_num] == 2:
                rows_to_explore.append(cell_num)
        return rows_to_explore
