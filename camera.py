import cv2

class Camera:
    def __init__(self,cameraIndex, width=1280, height=720) -> None:
        self.cam=cv2.VideoCapture(cameraIndex,cv2.CAP_DSHOW)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    def getPicture(self):
        if (self.cam.isOpened()):
            ret = self.cam.grab()
            if not ret:
                raise Exception("Failed to get the picture")
            ret, img=self.cam.retrieve()
            return cv2.flip(img,1)
        else:
            raise Exception("Camera is not initialized correctly")
            
    def close(self):
        self.cam.release()

def image_tresholder(img, lower_color, upper_color):
    #gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    mask=cv2.inRange(img,lower_color,upper_color)
    mask_rgb=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    return img & mask_rgb


def image_adaptive_tresholder(img, lower_color, upper_color):
    #gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    mask=cv2.inRange(img,lower_color,upper_color)
    mask_rgb=cv2.cvtColor(mask,cv2.COLOR_GRAY2RGB)
    return img & mask_rgb