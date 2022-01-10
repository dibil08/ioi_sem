import cv2
import dlib
from imutils import face_utils
from scipy.spatial import distance as dist

def faceLandmarks(im,faceDetector,landmarkDetector,debug=False):

    # Path for the detection model, you can download it from here: https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat
    # Create object to detect the face
   

    # Create object to detect the facial landmarks
    

    # Detect faces
    faceRects = faceDetector(im, 0)

    # Initialize landmarksAll array
    landmarksAll = []

    # For each face detected in the image, this chunk of code creates a ROI around the face and pass it as an argument to the 
    # facial landmark detector and append the result to the array landmarks 
    for i in range(0, len(faceRects)):
        newRect = dlib.rectangle(int(faceRects[i].left()),
                            int(faceRects[i].top()),
                            int(faceRects[i].right()),
                            int(faceRects[i].bottom()))
        landmarks = landmarkDetector(im, newRect)
        landmarksAll.append(landmarks)

    return landmarksAll, faceRects


def renderFacialLandmarks(im, landmarks):
    
    # Convert landmarks into iteratable array
    points = []
    [points.append((p.x, p.y)) for p in landmarks.parts()]

    # Loop through array and draw a circle for each landmark
    for p in points:
        cv2.circle(im, (int(p[0]),int(p[1])), 2, (255,0,0),-1)

    # Return image with facial landmarks 
    return im

def isSmile2(landmarks):
    (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
    mouth=face_utils.shape_to_np(landmarks)[mStart:mEnd]
    A = dist.euclidean(mouth[3], mouth[9])
    B = dist.euclidean(mouth[2], mouth[10])
    C = dist.euclidean(mouth[4], mouth[8])
    avg = (A+B+C)/3
    D = dist.euclidean(mouth[0], mouth[6])
    mar=avg/D
    if mar <= .2 or mar > .30 :
         result = "Smile"
    else:
        result = "No Smile"
    return (result, mar,mouth)
    

def isSmile1(landmarks):

    # Render the landmarks on the first face detected. You can specify the face by passing the desired index to the landmarks array.
    # In this case, one face was detected, so I'm passing landmarks[0] as the argument.

    # Calculate lips width
    lips_width = abs(landmarks.parts()[49].x - landmarks.parts()[55].x)

    # Calculate jaw width
    jaw_width = abs(landmarks.parts()[3].x - landmarks.parts()[15].x)

    # Calculate the ratio of lips and jaw widths
    ratio = lips_width/jaw_width
    print(ratio)

    # Evaluate ratio
    if ratio > 0.32 :
        result = "Smile"
    else:
        result = "No Smile"
    
    return (result,ratio)

def isSmile(landmarks):
    return isSmile2(landmarks)

def detect(frame,face_cascade,smile_cascade): 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), ((x + w), (y + h)), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
 
        for (sx, sy, sw, sh) in smiles:
            cv2.rectangle(roi_color, (sx, sy), ((sx + sw), (sy + sh)), (0, 0, 255), 2)
    return frame