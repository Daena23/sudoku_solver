from typing import List, Union

from auxiliary_func import find_row_cell_suppl


class Field:
    def __init__(self, sample):
        self.matrix = sample

    @property
    def gap_in_lines(self) -> List[int]:
        gap_coord_in_rows = [len(gap) for gap in self.gap_coord_per_line[0]]
        gap_coord_in_columns = [len(gap) for gap in self.gap_coord_per_line[1]]
        return gap_coord_in_rows + gap_coord_in_columns

    @property
    def gap_coord_per_line(self):
        gap_coord_in_all_rows = []
        for row_num in range(len(self.matrix)):
            gaps_coord_per_row = [[row_num, cell_num] for cell_num in range(len(self.matrix[row_num])) if self.matrix[row_num][cell_num] == 0]
            gap_coord_in_all_rows.append(gaps_coord_per_row)
        gap_coord_in_all_columns = []
        for row_num in range(len(self.matrix)):
            gaps_coord_in_columns = [[row_num, cell_num] for cell_num in range(len(self.matrix[row_num])) if self.matrix[row_num][cell_num] == 0]
            gap_coord_in_all_columns.append(gaps_coord_in_columns)
        return [gap_coord_in_all_rows, gap_coord_in_all_columns]

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

    def find_missing_digits(self, line) -> Union[int, List[int]]:
        return [digit for digit in range(1, len(self.matrix) + 1) if digit not in line]

    def find_cross_row_column(self, coord):
        row_num, cell_num = coord[0], coord[1]
        row_cells = self.matrix[row_num]
        column_cells = [row[cell_num] for row in self.matrix]
        cross_row_column = row_cells + column_cells
        return cross_row_column

    def visualize_matrix(self) -> None:
        print()
        print('  ', end=' ')
        for num in range(len(self.matrix)):
            print(num, end='  ')
        print()
        for row_num in range(len(self.matrix)):
            print(row_num, end=' ')
            print(self.matrix[row_num])
        print()

    def check_win_condition(self) -> bool:
        return all([all([cell != 0 for cell in row]) for row in self.matrix])

    @property
    def trans_matrix(self) -> List[List[int]]:
        return [[self.matrix[row][column] for row in range(len(self.matrix))] for column in range(len(self.matrix))]

    @property
    def gaps_per_square(self) -> List[List[int]]:
        return [square[2].count(0) for square in self.all_squares]

    @staticmethod
    def convert_coord_line_to_matrix(square: List, gap_nums_in_line) -> List[List[int]]:
        gaps_coord = []
        line = square[2]
        for cell_num_in_line in gap_nums_in_line:
            row_suppl, cell_suppl = find_row_cell_suppl(cell_num_in_line)
            row_num, cell_num = square[0] + row_suppl, square[1] + cell_suppl
            gaps_coord.append([row_num, cell_num])
        return gaps_coord

    @staticmethod
    def extract_perpen_line(sample, cell_num: int) -> List[int]:
        return [row[cell_num] for row in sample]
