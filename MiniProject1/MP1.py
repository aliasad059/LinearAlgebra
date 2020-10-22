# system of equations solver using row reduced echelon algorithm and numpy

import numpy as  np

# setting precision of matrix cells
float_formatter = "{:.2f}".format
np.set_printoptions(formatter={'float_kind': float_formatter})

# defining global variables
height = 0
width = 0
matrix = np.empty([1, 1])
basicVariables = []


# gets user input and initializes the matrix
def initMatrix():
    print("Coefficient matrix:")
    size_input_string = input("Enter number of rows and columns respectively\n")
    coefficient_matrix_height = int(size_input_string.split()[0])
    coefficient_matrix_width = int(size_input_string.split()[1])

    global matrix, height, width
    width = coefficient_matrix_width + 1
    height = coefficient_matrix_height

    matrix = np.empty([height, width]).astype(float)
    for i in range(height):
        while True:
            row_input_sting = input("Enter row {}:\n".format(i + 1))
            new_row = row_input_sting.split()
            if len(new_row) != coefficient_matrix_width:
                print("Wrong input! Enter {} numbers in the row again".format(coefficient_matrix_width))
                continue
            else:
                for j in range(coefficient_matrix_width):
                    while True:
                        try:
                            matrix[i][j] = float(new_row[j])
                            break
                        except ValueError:
                            print("Undefined input \'{}\' !".format(new_row[j]))
                            new_row[j] = input("Enter a number instead:\n")
                break

    while True:
        constant_values_string = input("Enter constant values:\n")
        constant_values_array = constant_values_string.split()
        if len(constant_values_array) != height:
            print("Wrong input! Enter {} numbers in the row again".format(coefficient_matrix_height))
            continue
        else:
            for i in range(height):
                while True:
                    try:
                        matrix[i][width - 1] = float(constant_values_array[i])
                        break
                    except ValueError:
                        print("Undefined input \'{}\' !".format(constant_values_array[i]))
                        constant_values_array[i] = input("Enter a number instead:\n")
            break

    print("Given matrix:")
    print(matrix)
    print()
    pass


# checks if there is at least one noneZero value in the column_number'th column
def isPivotColumn(column_number):
    for row_index in range(height):
        if matrix[row_index][column_number] != 0:
            return True
    return False


# checks if there is at least one pivot position in the column
def hasPivotPosition(column_number, row_number):
    for row_index in range(row_number, height):
        if abs(matrix[row_index][column_number]) >= 0.0001:
            return True
    return False


# interchanges two rows of the matrix
def interchange(first_row_number, second_row_number):
    matrix[[first_row_number, second_row_number], :] = matrix[[second_row_number, first_row_number], :]


# scales a row of the matrix scaling times
def scale(row_to_scale, scaling):
    matrix[row_to_scale] *= scaling
    pass


# adds scaling times of first_row to second_row
def replace(first_row, scaling, second_row):
    matrix[second_row] = matrix[second_row] + matrix[first_row] * scaling
    pass


# changes the equations to string
def getEquationString(row_index, pivot_position):
    equation_string = "x{}: ".format(pivot_position + 1)
    has_variable = False
    for i in range(pivot_position + 1, width - 1):
        if abs(matrix[row_index][i]) < 0.00001:
            continue
        elif matrix[row_index][i] > 0:
            has_variable = True

            equation_string += "{}x{} ".format(round(-matrix[row_index][i], 4), i + 1)
        else:
            has_variable = True
            if i == pivot_position + 1:
                equation_string += "{}x{} ".format(round(-matrix[row_index][i], 4), i + 1)
            else:
                if -matrix[row_index][i] == 1:
                    equation_string += "+x{} ".format(round(-matrix[row_index][i], 4), i + 1)
                else:
                    equation_string += "+{}x{} ".format(round(-matrix[row_index][i], 4), i + 1)

    if not has_variable:
        equation_string += str(round(matrix[row_index][width - 1], 4))
    else:
        if abs(matrix[row_index][width - 1]) < 0.00001:
            pass
        else:
            if matrix[row_index][width - 1] > 0:
                equation_string += '+'
            equation_string += str(round(matrix[row_index][width - 1], 4))

    return equation_string


# prints answer of the system
def printAnswers():
    basic_variable_index = 0
    for i in range(width - 1):
        if basic_variable_index < len(basicVariables) and basicVariables[basic_variable_index] == i:
            print(getEquationString(basic_variable_index, basicVariables[basic_variable_index]))
            basic_variable_index += 1
        else:
            print("x{} is free".format(i + 1))
    pass


# checks if there is at least one contradiction
def checkInconsistency():
    for i in range(height):
        zero_counter = 0
        for j in range(width - 1):
            if abs(matrix[i][j]) < 0.00001:
                zero_counter += 1
            else:
                break
        if zero_counter == width - 1 and abs(matrix[i][width - 1]) > 0.00001:
            return True

    return False


# interchanges the rows of matrix ,so the zero value is moved down, and the most absolute value is at the top
def sortMatrixColumn(column_to_sort, starting_row=0):
    for i in range(height):
        for j in range(starting_row, height - 1 - i):
            if abs(matrix[j][column_to_sort]) < abs(matrix[j + 1][column_to_sort]):
                interchange(j, j + 1)


# change the user given matrix to the row reduced echelon form
def changeToEchelonForm():
    row_to_check = 0
    for column_to_check in range(width - 1):
        if isPivotColumn(column_to_check) and hasPivotPosition(column_to_check, row_to_check):
            sortMatrixColumn(column_to_check, row_to_check)
            scale(row_to_check, 1.0 / (matrix[row_to_check][column_to_check]))
            basicVariables.append(column_to_check)
            for i in range(height):
                if i != row_to_check:
                    replace(row_to_check, -matrix[i][column_to_check], i)
            row_to_check += 1
    pass


if __name__ == '__main__':
    initMatrix()
    changeToEchelonForm()
    if checkInconsistency():
        print("The system has no solution.")
    else:
        printAnswers()
