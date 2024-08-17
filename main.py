from field import Field
from main_func import fill_multiple_gaps, update_matrix
from samples import large_sample_edited, ample


def main():
    field = Field(ample)
    i = 0
    while not field.check_win_condition():
        print('i', i)
        field.visualize_matrix()
        row_num, cell_num, missing_digit = fill_multiple_gaps(field)
        if None not in (row_num, cell_num, missing_digit):
            update_matrix(field, row_num, cell_num, missing_digit)
        else:
            print('unable to identify new number')
            break
        print()
        i += 1

    field.visualize_matrix()
    if field.check_win_condition():
        print('You won!')


if __name__ == '__main__':
    main()
