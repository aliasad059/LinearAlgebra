import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

height = 0
width = 0
# t is our threshold
t = 1100


# Reads image from th path and returns img_data
def get_image(path):
    global height, width

    img_data = img.imread(path)
    width = img_data.shape[1]
    height = img_data.shape[0]

    return img_data


# Gets img_data (a height*width*3 dim array) and returns r,g,b
def changeImageDataToRGB(img_data):
    r = [[0 for col in range(width)] for col in range(height)]
    g = [[0 for col in range(width)] for col in range(height)]
    b = [[0 for col in range(width)] for col in range(height)]

    for i in range(height):
        for j in range(width):
            r[i][j] = img_data[i][j][0]
            g[i][j] = img_data[i][j][1]
            b[i][j] = img_data[i][j][2]
    return r, g, b


# Gets r,g,b (3 height*width dim array) and returns img_data
def changeRGBToImageData(r, g, b):
    new_arr = [[[255 for col in range(3)] for col in range(width)] for row in range(int(height))]

    for i in range(height):
        for j in range(width):
            new_arr[i][j][0] = r[i][j]
            new_arr[i][j][1] = g[i][j]
            new_arr[i][j][2] = b[i][j]

    return new_arr


# Calculates SVD using np.linalg.svd() and change S to m*n array
def getSVD(arr):
    U, S, V = np.linalg.svd(arr)
    mnS = [[0 for col in range(width)] for col in range(height)]

    for i in range(height):
        for j in range(width):
            if i == j:
                mnS[i][j] = S[j]

    return U, mnS, V


# Filters S of R, S of G, S of B based on threshold and returns cleaned ones
def filter(Sr, Sg, Sb):
    Rr = [[0 for col in range(width)] for col in range(height)]
    Rg = [[0 for col in range(width)] for col in range(height)]
    Rb = [[0 for col in range(width)] for col in range(height)]

    for i in range(height):
        for j in range(width):
            if i == j:
                if Sr[i][j] > t:
                    Rr[i][j] = Sr[i][j]
                if Sg[i][j] > t:
                    Rg[i][j] = Sg[i][j]
                if Sb[i][j] > t:
                    Rb[i][j] = Sb[i][j]

    return Rr, Rg, Rb


if __name__ == '__main__':
    img_path = input("Enter The Path Of Image:\n")
    img_data = get_image(img_path)

    r, g, b = changeImageDataToRGB(img_data)
    Ur, Sr, Vr = getSVD(r)
    Ug, Sg, Vg = getSVD(g)
    Ub, Sb, Vb = getSVD(b)

    Rr, Rg, Rb = filter(Sr, Sg, Sb)
    r = (np.round(np.dot(np.dot(Ur, Rr), Vr), 5)).astype(int)
    g = (np.round(np.dot(np.dot(Ug, Rg), Vg), 5)).astype(int)
    b = (np.round(np.dot(np.dot(Ub, Rb), Vb), 5)).astype(int)

    cleaned_matrix = changeRGBToImageData(r, g, b)
    plt.imshow(cleaned_matrix)
    plt.show()
    # plt.imsave("cleaned_" + img_path, cleaned_matrix)

