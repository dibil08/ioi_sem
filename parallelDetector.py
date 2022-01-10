
from asyncio.windows_events import NULL
import threading
from smileDet import isSmile, faceLandmarks
import time

class FaceDetector(threading.Thread):
    def __init__(self, threadID, name,camera, delay, faceDet, landDet,callback=lambda: None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.callback = callback
        self.camera = camera
        self.delay=delay
        self.faceDet=faceDet
        self.landDet=landDet
        self.close=False


    def run(self):
        while not self.close:
            #time.sleep(self.delay)
            self.camera.getPicture()
            img = self.camera.getPicture()
            landmarks, _ = faceLandmarks(img,self.faceDet,self.landDet)
            if(len(landmarks)>0):
                result = isSmile(landmarks[0])
                self.callback(result)
    def finish(self):
        self.close=True


class DetectorSupervisor:
    def __init__(self,camera,delay,faceDetector,landmarkDetector):
        self.work_done = False
        self.camera=camera
        self.result=NULL
        self.delay=delay
        self.faceDet=faceDetector
        self.landDet=landmarkDetector

    def do_work(self):
        self.thread = FaceDetector(1, "Thread-1",self.camera, self.delay, self.faceDet,self.landDet,self.on_work_done)
        self.thread.start()

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

    def close(self):
        self.thread.finish()



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
    