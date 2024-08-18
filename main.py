from field import Field
from main_func import fill_gap, update_matrix
from samples import large_sample, large_sample_edited, ample, trial


def main():
    field = Field(trial)
    i = 0
    while not field.check_win_condition():
        print('i', i)
        field.visualize_matrix()
        # a = input()
        row_num, cell_num, missing_digit = fill_gap(field)
        if None in (row_num, cell_num, missing_digit):
            print('Unable to identify new number')
            break
        else:
            update_matrix(field, row_num, cell_num, missing_digit)
        i += 1

    field.visualize_matrix()
    if field.check_win_condition():
        print('You won!')


if __name__ == '__main__':
    main()
