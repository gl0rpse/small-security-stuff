#imports using opencv + dates and times
import cv2
import time
import datetime

#capture variable to access webcam
cap = cv2.VideoCapture(0) #0 is the index of system camera

#create cascades for face and body and pass classifiers to find faces and bodies
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")

#variable for detection of face/body
detection = False
detection_stopped_time = False
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5


#gives width and height for frame size
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v") #video format

while True:
    #reads a frame from the camera
    _, frame = cap.read()
    
    #create grayscale image for cascades
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #MultiScale(a, b, c) where a is the image, b is the scalefactor [determines accuracy and speed of algo],
    #   and c is the minimum number of "neighbors" we want to detect the faces on the image.
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    #faces and bodies are a list of locations, so if they exist at all
    #   start detection. super elaborate algorithm so 20 videos aren't saved
    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False #reset timer
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") #formats dates and times for video name
            out = cv2.VideoWriter(f"{current_time}.mp4", fourcc, 20, frame_size)
            print("I'm watching you.")
    elif detection: #if detection
        if timer_started:
            if (time.time() - detection_stopped_time) >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release() #save video
                print("Recording Stopped!")
        else:
            timer_started = True
            detection_stopped_time = time.time() #gives current time

    #if detecting, write
    if detection:
        out.write(frame)

    #for loop to create rectangle on face detected
    for (x, y, width, height) in faces:

        #draw rectangle on image in frame, (x,y) is top left corner
        #next is the bottom right point of the rectangle, BGR for color, and pixel width
        cv2.rectangle(frame, (x, y), (x + width, y + height), (255, 0, 0), 3)

    #creates window to show video
    cv2.imshow("Security Cam", frame)

    #if q key is pressed, exit window
    if cv2.waitKey(1) == ord('q'):
        break


out.release()
cap.release()
cv2.destroyAllWindows()

