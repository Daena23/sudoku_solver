from typing import Tuple


def find_row_cell_suppl(num_in_square: int) -> Tuple[int, int]:
    row_dict = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2}
    cell_dict = {0: 0, 1: 1, 2: 2, 3: 0, 4: 1, 5: 2, 6: 0, 7: 1, 8: 2}
    return row_dict[num_in_square], cell_dict[num_in_square]
