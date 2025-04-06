from typing import List, Optional, Set, Dict

from utils import (find_missing_digits,
                   convert_linear_coord_to_matrix_coord,
                   find_index_of_square,
                   swap_row_column,
                   extract_perpendicular_line,
                   )


class Sudoku:
    def __init__(self, sudoku: List[List[int]]):
        self.matrix: List[List[int]] = sudoku
        self.size: int = len(self.matrix)
        self.transposed_matrix: List[List[int]] = self.transposed
        self.row_index: Optional[None] = None
        self.column_index: Optional[None] = None
        self.digit: Optional[None] = None
        self.solved = []
        self.zeros_per_line = []

    @property
    def transposed(self) -> List[List[int]]:
        return [[self.matrix[column_index][row_index]
                 for column_index in range(self.size)] for row_index in range(self.size)]

    # SINGLE GAP
    def is_single_gap_in_line(self, matrix: List[List[int]]) -> bool:
        self.zeros_per_line = [line.count(0) for line in matrix]
        return 1 in self.zeros_per_line

    def define_single_gap_in_line(self, matrix: List[List[int]]) -> None:
        self.row_index = self.zeros_per_line.index(1)
        row = matrix[self.row_index]
        self.digit, = find_missing_digits(row)
        self.column_index = row.index(0)

    # IN SQUARE
    @property
    def is_single_gap_in_square(self) -> bool:
        self.zeros_per_line = [square['square_as_line'].count(0) for square in self.all_squares]
        return 1 in self.zeros_per_line

    def define_single_gap_in_square(self) -> None:
        square_to_study: int = self.zeros_per_line.index(1)
        square: Dict = self.all_squares[square_to_study]
        (row_index, column_index) = self.find_gap_coord_in_matrix(square)
        self.digit, = find_missing_digits(square['square_as_line'])
        self.row_index = row_index
        self.column_index = column_index

    def find_gap_coord_in_matrix(self, square: Dict) -> List[int]:
        line = square['square_as_line']
        zero_column_indexes: List[int] = [column_index for column_index in range(self.size) if line[column_index] == 0]
        gap_coord_in_matrix: List[List[int]] = convert_linear_coord_to_matrix_coord(square, zero_column_indexes)
        return gap_coord_in_matrix[0]

    @property
    def all_squares(self) -> List[Dict]:
        square_slices = [n for n in range(len(self.matrix)) if n % 3 == 0]
        all_squares = []
        for row_index in square_slices:
            for column_index in square_slices:
                rows = self.matrix[row_index: row_index + 3]
                square = []
                for row in rows:
                    square.extend(row[column_index: column_index + 3])
                all_squares.append({'row_index': row_index, 'column_index': column_index, 'square_as_line': square})
        return all_squares

    def is_digit_already_in_square(self, row_num: int, column_num: int, digit: int, matrix: List[List[int]]) -> bool:
        if id(matrix) == id(self.matrix):
            square_index, = find_index_of_square(row_num, column_num)
        else:
            square_index, = find_index_of_square(column_num, row_num)
        square = self.all_squares[square_index]
        if digit in square['square_as_line']:
            return True
        return False

    # MULTI GAPS
    def define_gap_among_several(self, matrix: List[List[int]]) -> bool:
        for row_index in range(self.size):
            row = matrix[row_index]
            missing_digits = find_missing_digits(row)
            if len(missing_digits) >= 2:
                empty_columns_indexes = [column_index for column_index in range(self.size) if row[column_index] == 0]
                if self.find_digit_position(empty_columns_indexes, missing_digits, matrix, row_index):
                    return True
        return False

    def find_digit_position(
            self,
            empty_columns_indexes: List[int],
            missing_digits: Set,
            matrix: List[List[int]],
            row_index: int,
    ) -> bool:
        for digit in missing_digits:
            possible_digit_positions = []
            for column_index in empty_columns_indexes:
                if (digit not in extract_perpendicular_line(matrix, column_index) and
                        not self.is_digit_already_in_square(row_index, column_index, digit, matrix)):
                    possible_digit_positions.append(column_index)
            if len(possible_digit_positions) == 1:
                column_index, = possible_digit_positions
                self.digit = digit
                self.row_index = row_index
                self.column_index = column_index
                if id(matrix) != id(self.matrix):
                    swap_row_column(self)
                return True
        return False

    # END
    def is_solved(self) -> bool:
        return not any([self.matrix[row_index][column_index] == 0
                        for column_index in range(self.size) for row_index in range(self.size)])

    @staticmethod
    def visualize(matrix) -> None:
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
            # Sudoku in triplets
            for column_num in range(len(matrix[row_num])):
                print(matrix[row_num][column_num], end='')
                if (column_num + 1) % 3 == 0:
                    print(' | ', end=' ')
                else:
                    print(end=' ')
            print()
        print()

    def final_message(self, move_counter: int) -> None:
        if self.is_solved():
            print(f'Solved in {move_counter} moves\n')
            self.visualize(self.matrix)
            self.check_if_answer_correct()
        else:
            print('Can\'t solve this sudoku :(')

    def check_if_answer_correct(self):
        message = 'Check: the answer is'
        if self.matrix == self.solved:
            print(f'{message} correct')
        else:
            print(f'{message} wrong')
