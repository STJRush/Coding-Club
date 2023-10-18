import numpy as np
import cv2

try:
    cap = cv2.VideoCapture(0)
     
    while(True):
        ret, frame = cap.read()
        #frame = cv2.flip(frame, -1) # Flip camera vertically
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    
except:
    print("no worky")
    cap.release()
    cv2.destroyAllWindows()
