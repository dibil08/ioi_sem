import cv2
from numpy.lib.function_base import average, disp
from camera import Camera, image_tresholder
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import truncnorm
from parallelDetector import DetectorSupervisor
import time
from gameOfLife.state import SparseSetState, State
from gameOfLife.game import Game
from gameOfLife.rules import Rule, SparseSetRules
from smileDet import isSmile, faceLandmarks
import PIL.Image
import random
from imageToPixel import png_to_points
from patterns import patterns
MAX_ITER = 2000000

CAMERA_WIDTH=1280
CAMERA_HEIGHT=720

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080
GAME_WIDTH = int(SCREEN_HEIGHT/4)
GAME_HEIGHT= int(SCREEN_HEIGHT/4)
frame_rate = 10
prev = 0

init = np.zeros((GAME_WIDTH, GAME_WIDTH), dtype=bool)

board = png_to_points("smile_to_give_life.png",np.array([0,0,0]),30,30)

rules = SparseSetRules()

state = SparseSetState(board)
previous_state = None
progression = []
i = 0
random.seed(0)

camera=Camera(0)
def state_to_matrix(dimensions,state):
    res = np.zeros(dimensions, dtype=bool)
    for key in state.grid:
        res[key[0],key[1]]=True
    return res

def display_image(array,game_dimensions,screen_dimensions):
    array = np.uint8(np.clip(array,0,1)*255.0)
    array = np.reshape(array,game_dimensions)
#    PIL.Image.fromarray(array)
    array=cv2.resize(array,screen_dimensions)
    #array=cv2.GaussianBlur(array,(13,13),cv2.BORDER_DEFAULT)
    #array=cv2.bilateralFilter(array,9,75,75)
    cv2.imshow("test", array)

def add_pattern_to_point(state,point_x,point_y,dimensions):
    choice = random.choice(patterns)
    rotation=random.choice([True, False])
    flipX = random.choice([True, False])
    flipY = random.choice([True, False])
    for point in choice:
        x=point[0]
        y=point[1]
        if(rotation):
            z=x
            x=y
            y=z
        if(flipX):
            x=x*(-1)
        if(flipY):
            y=y*(-1)
        state.add_point((
            (point_x+x+dimensions[0])%dimensions[0],
            (point_y+y+dimensions[1])%dimensions[1]))
        
    

    

gameRunning=True
main=DetectorSupervisor(camera,1)
main.do_work()
while gameRunning:
    
    if not main.work_done:
        time_elapsed = time.time() - prev

        if time_elapsed > 1./frame_rate:
            prev=time.time()
            i += 1

            previous_state = state.copy()
            progression.append(previous_state.grid)
            state = state.apply_rules(rules,GAME_WIDTH)

            stateMatrix= state_to_matrix((GAME_WIDTH,GAME_HEIGHT),state)
            display_image(stateMatrix,(GAME_WIDTH,GAME_HEIGHT),(SCREEN_HEIGHT,SCREEN_WIDTH))

        if cv2.waitKey(1) == 27 : 
            gameRunning=False  # esc to quit
            cv2.destroyAllWindows()
        
    else:
        results=main.get_result()
        print(results[0])
        if(results[0]=="Smile"):
            print("Adding points")
            for point in results[2]:
                if(point[0]>280 and point[0]<1000):
                    x=int(((point[0]-280)/CAMERA_WIDTH)*GAME_HEIGHT)
                    y=int((point[1]/CAMERA_WIDTH)*GAME_WIDTH)
                    add_pattern_to_point(state,y,x,(GAME_WIDTH,GAME_HEIGHT))
        main.reset()
main.close()

