from field import Field
from main_func import fill_gap, update_matrix
from samples import trial


def main():
    field = Field(trial)
    cycle_num = 0
    while not field.check_win_condition():
        print('cycle_num', cycle_num)
        field.visualize_matrix()
        # a = input()
        row_num, cell_num, missing_digit = fill_gap(field)
        if None in (row_num, cell_num, missing_digit):
            print('Unable to identify new number')
            break
        else:
            print('row_num:', row_num, ', cell_num:', cell_num, ', missing_digit:', missing_digit)
            update_matrix(field, row_num, cell_num, missing_digit)
        cycle_num += 1

    field.visualize_matrix()
    if field.check_win_condition():
        print('You won!')


if __name__ == '__main__':
    main()
