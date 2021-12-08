
from asyncio.windows_events import NULL
from multiprocessing import Pool, Manager, Process
from time import sleep
import random
from smileDet import isSmile, faceLandmarks
import time


def runDetection(camera, delay, results):
    while True:
        time.sleep(delay)
        img = camera.getPicture()
        landmarks, _ = faceLandmarks(img)
        if(len(landmarks)>0):
            result = isSmile(landmarks[0])
            results[0]=result

class DetectorSupervisor:
    def __init__(self,camera,delay):
        self.work_done = False
        self.camera=camera
        self.result=NULL
        self.delay=delay
        self.manager = Manager()
        self.results = self.manager.dict()

    def do_work(self):
        myPool = Pool(1)
        Process(target=runDetection, args=(self.camera, self.delay, self.results))

    def on_work_done(self,result):
        self.work_done = True
        self.result=result
    
    def reset(self):
        self.work_done= False
        self.result=NULL

    def get_result(self):
        if self.result!=NULL:
            return self.result
        else:
            return NULL


# USAGE 

# main= DetectorSupervisor(camera)
# while True:
#     main.do_work()

#     while not main.work_done:
#         print("running game")
#         time.sleep(0.5)

#     print("got results")
#     print(main.get_result())
#     main=DetectorSupervisor(camera)
    