from field import Field
from main_func import find_missing_digit
from samples import (hard_sudoku_1, hard_sudoku_1_solved,
                     easy_sudoku_1_solved, easy_sudoku_1)


def main():
    field = Field(hard_sudoku_1)
    solved_sudoku = hard_sudoku_1_solved
    cycle_num = 0
    while not field.check_win_condition():
        field.visualize_matrix()
        row_num, cell_num, missing_digit = find_missing_digit(field)
        if None in (row_num, cell_num, missing_digit):
            print('Can\'t solve this sudoku :(')
            break
        else:
            print(f'row: {row_num}, column: {cell_num}, missing digit: {missing_digit}')
            field.matrix[row_num][cell_num] = missing_digit
        cycle_num += 1
    if field.check_win_condition():
        field.visualize_matrix()
        print(f'{cycle_num} gaps have been filled')
        print('SOLVED')

    # Test
    if field.matrix == solved_sudoku:
        print('Correct answer')
    else:
        print('Wrong answer')

if __name__ == '__main__':
    main()
