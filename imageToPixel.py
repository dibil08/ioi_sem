import cv2
import numpy as np

def png_to_points(name,default_color,paddingTop,paddingLeft):
    # create red image
    img = cv2.imread(name)
    # convert to grayscale
    points=set()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not np.array_equal(img[i][j],default_color):
                points.add((i+paddingLeft,j+paddingTop,(img[i][j][0],img[i][j][1],img[i][j][2])))
    return points

def png_to_points_no_color(name,default_color,paddingTop,paddingLeft):
    # create red image
    img = cv2.imread(name)
    # convert to grayscale
    points=set()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not np.array_equal(img[i][j],default_color):
                points.add((i+paddingLeft,j+paddingTop))
    return points
if __name__ == "__main__":
    print(png_to_points_no_color("pixil-frame-0 (7).png",np.array([0,0,0]),-2,-2))