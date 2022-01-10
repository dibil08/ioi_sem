import cv2
import numpy as np

def png_to_points(name,default_color,paddingTop,paddingLeft,lifePoints):
    # create red image
    img = cv2.imread(name)
    # convert to grayscale
    points=dict()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not np.array_equal(img[i][j],default_color):
                points[(i+paddingLeft,j+paddingTop)]=lifePoints
    return points

def png_to_points_no_color(name,default_color,paddingTop,paddingLeft,lifePoints):
    # create red image
    img = cv2.imread(name)
    # convert to grayscale
    points=set()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if not np.array_equal(img[i][j],default_color):
                points.add((i+paddingLeft,j+paddingTop,lifePoints))
    return points
if __name__ == "__main__":
    print(png_to_points_no_color("pixil-frame-0 (7).png",np.array([0,0,0]),-2,-2))