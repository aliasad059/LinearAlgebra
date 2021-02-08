from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import math

# t is our threshold
t = 3

height = 30
width = 30


def get_main_function():
    x = np.linspace(0, math.pi * 3 / 2, 30)
    y = np.linspace(0, math.pi * 3 / 2, 30)
    X, Y = np.meshgrid(x, y)
    return np.sin(X * Y)


def make_function_noisy(z):
    max_noise = 0.1
    t = 2 * np.random.rand(30 * 30) * max_noise - max_noise
    t = t.reshape(30, 30)
    return np.add(z, t)


def get_function():
    return make_function_noisy(get_main_function())


def show_my_matrix(Z):
    x = np.linspace(0, math.pi * 3 / 2, 30)
    y = np.linspace(0, math.pi * 3 / 2, 30)
    X, Y = np.meshgrid(x, y)
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='viridis', edgecolor='black')
    ax.set_title('surface');
    ax.view_init(60, 35)
    plt.show()


def show_main():
    Z = get_main_function()
    show_my_matrix(Z)


def show_noisy():
    Z = get_function()
    show_my_matrix(Z)


def show_cleand():
    noisy_matrix = get_function()
    U, S, V = getSVD(noisy_matrix)
    R = filter(S)
    cleaned_matrix = np.dot(np.dot(U, R), V)
    show_my_matrix(cleaned_matrix)


# Calculates SVD using np.linalg.svd() and change S to m*n array
def getSVD(arr):
    U, S, V = np.linalg.svd(arr)
    mnS = [[0 for col in range(width)] for col in range(height)]

    for i in range(height):
        for j in range(width):
            if i == j:
                mnS[i][j] = S[j]

    return U, mnS, V


# Filters S based on the threshold and returns cleaned R
def filter(S):
    R = [[0 for col in range(width)] for col in range(height)]

    for i in range(height):
        for j in range(width):
            if i == j:
                if S[i][j] > t:
                    R[i][j] = S[i][j]
    return R


if __name__ == '__main__':
    # show_main()
    # show_noisy()
    show_cleand()
