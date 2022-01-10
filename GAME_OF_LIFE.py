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
import dlib

lifePoints=1
MAX_ITER = 2000000

CAMERA_WIDTH=1280
CAMERA_HEIGHT=720

SCREEN_WIDTH = 1080
SCREEN_HEIGHT = 1080

startDelay=5
GAME_WIDTH = int(SCREEN_HEIGHT/4)
GAME_HEIGHT= int(SCREEN_HEIGHT/4)
frame_rate = 60
prev = 0
noise = np.random.poisson((256), (GAME_WIDTH,GAME_HEIGHT,3))

init = np.zeros((GAME_WIDTH, GAME_WIDTH), dtype=bool)

board = png_to_points("smile_to_give_life.png",np.array([0,0,0]),30,30,lifePoints)

rules = SparseSetRules(lifePoints)

state = SparseSetState(board,lifePoints)
previous_state = None
progression = []
i = 0
random.seed(0)
firstSmile=False
camera=Camera(0)
def state_to_matrix(dimensions,state):
    res = np.zeros(dimensions, dtype=bool)
    for key in state.grid:
        res[key[0],key[1]]=True
    return res

def display_image(array,game_dimensions,screen_dimensions,noise):
    if firstSmile:
        startValue=1.0
    else:
        startValue=255.0
    array = np.uint8(np.clip(array,0,1)*startValue)
    array= np.repeat(array[:, :, np.newaxis], 3, axis=2)
    if firstSmile:
        #if int(time.time())%100:
        #    noise = np.random.poisson((256), (array.shape[0],array.shape[1],3))
        noise =np.array(noise,dtype='uint8')
        array=np.multiply(array,noise)
    array = np.reshape(array,(game_dimensions[0],game_dimensions[1],3))
    array=cv2.resize(array,(screen_dimensions[0],screen_dimensions[1]))
    cv2.imshow("Smile everyday", array)

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
        state.add_point(
            ((point_x+x+dimensions[0])%dimensions[0],
            (point_y+y+dimensions[1])%dimensions[1],
            lifePoints))
        
    

    
PREDICTOR_PATH = "shape_predictor_68_face_landmarks.dat"
faceDetector = dlib.get_frontal_face_detector()  
landmarkDetector = dlib.shape_predictor(PREDICTOR_PATH)
gameRunning=True
main=DetectorSupervisor(camera,0,faceDetector,landmarkDetector)
main.do_work()
timeStarted=time.time()
while gameRunning:
    
    if not main.work_done:
        time_elapsed = time.time() - prev

        if time_elapsed > 1./frame_rate :
            prev=time.time()
            i += 1

            state = state.apply_rules(rules,GAME_WIDTH)

            stateMatrix= state_to_matrix((GAME_WIDTH,GAME_HEIGHT),state)
            display_image(stateMatrix,(GAME_WIDTH,GAME_HEIGHT),(SCREEN_HEIGHT,SCREEN_WIDTH),noise)

        pressedKey= cv2.waitKey(1)
        if pressedKey== 27 : 
            gameRunning=False  # esc to quit
            cv2.destroyAllWindows()
        if pressedKey == 114 : 
            print("Reset state")
            state.clear_all()    
            board = png_to_points("smile_to_give_life.png",np.array([0,0,0]),30,30,lifePoints)
            state = SparseSetState(board,lifePoints)
            timeStarted=time.time()
            firstSmile=False
            
        
    else:
        if time.time()-timeStarted>startDelay:
            results=main.get_result()
            print(results[0])
            if(results[0]=="Smile"):
                firstSmile=True
                print("Adding points")
                for point in results[2]:
                    if(point[0]>280 and point[0]<1000):
                        x=int(((point[0]-280)/CAMERA_WIDTH)*GAME_HEIGHT)
                        y=int((point[1]/CAMERA_WIDTH)*GAME_WIDTH)
                        add_pattern_to_point(state,y,x,(GAME_WIDTH,GAME_HEIGHT))
            main.reset()
main.close()

