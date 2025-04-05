from typing import List, Union, Dict, Optional

from auxiliary_func import find_row_cell_suppl


class Sudoku:
    def __init__(self, sample: List[List[int]]):
        self.matrix = sample
        self.size = len(self.matrix)
        self.transposed_matrix: List[List[int]] = self.find_transposed
        self.new_row_num: Optional[None] = None
        self.new_column_num: Optional[None] = None
        self.new_digit: Optional[None] = None

    @property
    def find_transposed(self) -> List[List[int]]:
        return [[self.matrix[column_num][row_num] for column_num in range(self.size)] for row_num in range(self.size)]

    def gap_number_in_line(self, matrix) -> List[int]:
        return [line.count(0) for line in matrix]

    # @property
    # def gap_coord_per_line(self) -> Dict[str, List]:
    #     gap_coord_in_all_rows = []
    #     for row_num in range(len(self.matrix)):
    #         gaps_coord_per_row = [[row_num, cell_num] for cell_num in range(len(self.matrix[row_num])) if self.matrix[row_num][cell_num] == 0]
    #         gap_coord_in_all_rows.append(gaps_coord_per_row)
    #     gap_coord_in_all_columns = []
    #     for row_num in range(len(self.matrix)):
    #         gaps_coord_in_columns = [[row_num, cell_num] for cell_num in range(len(self.matrix[row_num])) if self.matrix[row_num][cell_num] == 0]
    #         gap_coord_in_all_columns.append(gaps_coord_in_columns)
    #     return {'gap_coord_in_all_rows': gap_coord_in_all_rows, 'gap_coord_in_all_columns': gap_coord_in_all_columns}

    @property
    def all_squares(self) -> List[List[int]]:
        square_slices = [n for n in range(len(self.matrix)) if n % 3 == 0]
        all_squares = []
        for row_num in square_slices:
            for column_num in square_slices:
                rows = self.matrix[row_num: row_num + 3]
                square = []
                for row in rows:
                    square.extend(row[column_num: column_num + 3])
                all_squares.append([row_num, column_num, square])
        return all_squares

    def find_gap_coord_in_matrix(self, square) -> List[List[int]]:
        init_row, init_column, line = square
        gap_nums_in_line = [cell_num for cell_num in range(len(line)) if line[cell_num] == 0]
        gap_coord_in_matrix = self.convert_coord_line_to_matrix(square, gap_nums_in_line)
        return gap_coord_in_matrix

    def find_single_gap_in_line(self, matrix: List[List[int]]) -> None:
        print('self.new_row_num', self.new_row_num, self.new_column_num)
        self.new_row_num = self.gap_number_in_line(matrix).index(1)
        self.new_digit, = self.find_missing_digits(matrix[self.new_row_num])
        self.new_column_num = matrix[self.new_row_num].index(0)

    def find_missing_digits(self, row):
        all_digits = {*range(1, 10)}
        present_digits = set(row)
        all_digits -= present_digits
        return all_digits

    def find_cross_row_column(self, coord: List[int]):
        row_num, cell_num = coord[0], coord[1]
        row_cells = self.matrix[row_num]
        column_cells = [row[cell_num] for row in self.matrix]
        cross_row_column = row_cells + column_cells
        return cross_row_column

    def visualize(self, matrix) -> None:
        print('     ', end=' ')
        # Horizontal indexes
        for num in range(len(matrix)):
            print(num, end=' ')
            if (num + 1) % 3 == 0:
                print(end='   ')
        # Vertical indexes
        for row_num in range(len(matrix)):
            if row_num % 3 == 0:
                print()
            print(row_num, end='   | ')
            # Sample in triplets
            for column_num in range(len(matrix[row_num])):
                print(matrix[row_num][column_num], end='')
                if (column_num + 1) % 3 == 0:
                    print(' | ', end=' ')
                else:
                    print(end=' ')
            print()
        print()

    def is_solved(self) -> bool:
        return not any([self.matrix[row_num][cell_num] == 0 for cell_num in range(self.size) for row_num in range(self.size)])

    @property
    def trans_matrix(self) -> List[List[int]]:
        return [[self.matrix[row][column] for row in range(len(self.matrix))] for column in range(len(self.matrix))]

    @property
    def gaps_per_square(self) -> List[List[int]]:
        return [square[2].count(0) for square in self.all_squares]

    @staticmethod
    def convert_coord_line_to_matrix(square: List, gap_nums_in_line) -> List[List[int]]:
        gaps_coord = []
        for cell_num_in_line in gap_nums_in_line:
            row_suppl, cell_suppl = find_row_cell_suppl(cell_num_in_line)
            row_num, cell_num = square[0] + row_suppl, square[1] + cell_suppl
            gaps_coord.append([row_num, cell_num])
        return gaps_coord

    @staticmethod
    def extract_perpen_line(matrix: List[List[int]], column_num: int) -> List[int]:
        return [row[column_num] for row in matrix]
