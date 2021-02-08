import matplotlib.pyplot as plt
import matplotlib.image as img

height = 0
width = 0


def get_image(path):
    global height, width
    img_data = img.imread(path)
    width = img_data.shape[1]
    height = img_data.shape[0]
    return img_data


# checks if the entered RGB is (nearly) white or not.
def isWhite(arr, i, j):
    return arr[i][j][0] >= 245 and arr[i][j][1] >= 245 and arr[i][j][2] >= 245


# Shades the transformed_arr as follows:
# Check the arr, for each pixel in arr checks if it is white or not.
# If so, that pixel in the final array gains from transformed_arr. if not, that pixel gains from the arr.
def shade(arr, transformed_arr):
    for i in range(height):
        for j in range(width):
            if not (isWhite(arr, i, j)):
                transformed_arr[i][j][0] = arr[i][j][0]
                transformed_arr[i][j][1] = arr[i][j][1]
                transformed_arr[i][j][2] = arr[i][j][2]
    return transformed_arr


# Transforms the matrix of the image with the shear transformation.
# T(x) = Ax and     A = [  1        0  ]
#                       [  lambda   1  ]     =>     T(x) = [ x1 ,x1*lambda + x2 ]
def shearTransform(arr, lambda_val=0.1):
    new_arr = [[[255 for col in range(3)] for col in range(int(height * lambda_val + width))] for row in
               range(int(height))]
    for i in range(height):
        for j in range(width):
            if not (isWhite(arr, i, j)):
                new_arr[i][int(lambda_val * i + j)][0] = 198
                new_arr[i][int(lambda_val * i + j)][1] = 202
                new_arr[i][int(lambda_val * i + j)][2] = 210
    return new_arr


if __name__ == '__main__':
    img_path = input("Enter The Path Of Image:(The Background Must Be White)\n")
    img_data = get_image(img_path)
    sheared_img_data = shearTransform(img_data)
    plt.imshow(shade(img_data, sheared_img_data))
    plt.show()
