import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# Number of data to estimate from the end of data array
# This data wouldn't be used to calculate the estimated polynomial
data_to_estimate = 10


# Reads CSV file from file_address and  makes a list from data_name column
def readCsv(file_address, data_name):
    df = pd.read_csv(file_address)
    return df[data_name].to_list()


# Find a solution (beta) for the following equation
# xT x beta = xT y
def solveSystem(x_matrix, y_matrix):
    xT = np.transpose(x_matrix)
    xTx = np.dot(xT, x_matrix)
    xTy = np.dot(xT, y_matrix)

    return np.round(np.linalg.solve(xTx, xTy), 5)


# Makes the X matrix
# If is_linear is true x has 2 columns else has 3 columns
def makeXMatrix(start, end, is_linear=True):
    columns_number = 0

    if is_linear:
        columns_number = 2
    else:
        columns_number = 3

    res_matrix = [[1 for i in range(columns_number)] for j in range(end - start)]

    for i in range(start, end):
        res_matrix[i][1] = i
        if not is_linear:
            res_matrix[i][2] = i * i

    return res_matrix


# Calculates and prints the estimated data based of system_solution from start to the end
# In addition, returns Sum of square of errors
def getLinearError(data_list, start, end, system_solution):
    print("Linear Polynomial Error :\n")
    errors = 0
    for x in range(start, end):
        actual_value = data_list[x]
        calculated_value = round(system_solution[0] + system_solution[1] * x, 5)
        error = round(actual_value - calculated_value, 5)
        print('Actual Value: ' + str(actual_value))
        print('Calculated Value: ' + str(calculated_value))
        print('Error: ' + str(error) + '\n')
        errors += error * error

    return round(errors, 5)


# Calculates and prints the estimated data based of system_solution from start to the end
# In addition, returns Sum of square of errors
def getQuadraticError(data_list, start, end, system_solution):
    print("Quadratic Polynomial Error :\n")
    errors = 0
    for x in range(start, end):
        actual_value = data_list[x]
        calculated_value = round(system_solution[0] + system_solution[1] * x + system_solution[2] * x * x, 5)
        error = round(actual_value - calculated_value, 5)
        print('Actual Value: ' + str(actual_value))
        print('Calculated Value: ' + str(calculated_value))
        print('Error: ' + str(error) + '\n')
        errors += error * error

    return round(errors, 5)


if __name__ == '__main__':
    data_list = readCsv("GOOGL.csv", "Low")

    # Find the coefficient of quadratic polynomial
    quadratic_solution = solveSystem(makeXMatrix(0, len(data_list) - data_to_estimate, False),
                                     data_list[:len(data_list) - data_to_estimate])
    # Find the coefficient of linear polynomial
    linear_solution = solveSystem(makeXMatrix(0, len(data_list) - data_to_estimate, True),
                                  data_list[:len(data_list) - data_to_estimate])

    linear_error = getLinearError(data_list, len(data_list) - data_to_estimate, len(data_list), linear_solution)
    quadratic_error = getQuadraticError(data_list, len(data_list) - data_to_estimate, len(data_list),
                                        quadratic_solution)

    print('Sum Of Linear Polynomial Errors: ' + str(linear_error))
    print('Sum of Quadratic Polynomial Errors: ' + str(quadratic_error))

    estimated_values = [0 for i in range(len(data_list))]
    if quadratic_error < linear_error:
        for x in range(len(data_list)):
            estimated_values[x] = x * x * quadratic_solution[2] + x * quadratic_solution[1] + quadratic_solution[0]

    else:
        for x in range(len(data_list)):
            estimated_values[x] = x * linear_solution[1] + linear_solution[0]

    plt.scatter(range(len(data_list)), data_list, color='red', label='Actual Values')
    plt.plot(estimated_values, color='blue', label='Estimated Polynomial')
    plt.show()
