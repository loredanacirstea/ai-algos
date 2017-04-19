digits = '123456789'
rows = 'ABCDEFGHI'

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:

        # Find all instances of naked twins in this unit
        unit_values = [values[box] for box in unit]
        chains = dict([(box, values[box]) for box in unit if len(values[box]) > 1 and len(values[box]) == unit_values.count(values[box])])

        # create a dict with twins' values as keys and a list of boxes as values
        ch = dict()
        for chain in chains:
            if not ch.get(chains[chain]):
                ch[chains[chain]] = []
            ch[chains[chain]].append(chain)

        # Eliminate the naked twins as possibilities for their unit peers
        for val in ch:
            for box in ch[val]:
                for peer in unit:
                    if peer not in ch[val] and len(values[peer]) > 1:
                        new_val = values[peer]
                        for l in val:
                            new_val = new_val.replace(l, '')
                        values = assign_value(values, peer, new_val)
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    assert len(grid) == 81, "Input grid must be a string of length 81 (9x9)"
    return dict(map(lambda x,y:[x,y.replace('.', digits)], boxes, grid))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in digits))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    assert len(values) == 81, "Input grid must be a string of length 81 (9x9)"
    for val in values:
        if(len(values[val]) == 1):
            for peer in peers[val]:
                values = assign_value(values, peer, values[peer].replace(values[val], ''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    assert len(values) == 81, "Input grid must be a string of length 81 (9x9)"
    for unit in unitlist:
        # Concatenate all values in a unit
        all_vals = ''
        for box in unit:
            all_vals += values[box]

        # Get unique values if they exist (onces)
        all_vals = sorted(all_vals)
        length = len(all_vals)
        onces = ''

        if all_vals[0] != all_vals[1]:
            onces += all_vals[0]
        for i in range(1, length - 1):
            if all_vals[i] != all_vals[i+1] and all_vals[i] != all_vals[i-1]:
                onces += all_vals[i]
        if all_vals[length-2] != all_vals[length-1]:
            onces += all_vals[length-1]

        # Assign unique values to boxes that contain them
        for box in unit:
            for once in onces:
                if once in values[box]:
                    values = assign_value(values, box, once)
                    break


    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False:
        return False

    # Get 1 box with min length value
    lengths = dict((box, len(values[box])) for box in values )
    min_len = min(list(filter(lambda x: x > 1, lengths.values())) or [0]);

    if not min_len:
        return values;

    for b in lengths:
        if lengths[b] == min_len:
            box = b
            break;

    # Recursively call search on each resulted grid
    for val in values[box]:
        new_values = values.copy()
        new_values = assign_value(new_values, box, val)
        result = search(new_values)
        if result:
            return result

    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    values = search(values)
    return values


boxes = cross(rows, digits)
row_units = [cross(r, digits) for r in rows]
column_units = [cross(rows, c) for c in digits]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diag_units = [[], []]

diag1 = [cross(rows[ri], digits[di]) for ri in range(len(rows)) for di in range(ri, ri+1)]
diag2 = [cross(rows[ri], digits[di]) for ri in range(len(rows)) for di in range(len(rows)-ri-1, len(rows)-ri-2, -1)]
for i in range(len(diag1)):
    diag_units[0] += diag1[i]
    diag_units[1] += diag2[i]

unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
