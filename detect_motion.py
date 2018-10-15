import cv2
import numpy as np

def detect_motion(cap):
    avg = None
    while(cap.isOpened()):
        ret, frame = cap.read()
        frame = cv2.flip(frame, -1) #カメラ上下左右反転
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if avg is None:
            avg = gray.copy().astype('float')
            continue

        #加重平均によるフレーム差分
        cv2.accumulateWeighted(gray, avg, 0.5)
        frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
        thresh = cv2.threshold(frameDelta, 3, 255, cv2.THRESH_BINARY)[1]
        contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        max_area = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if max_area < area and area < 10000 and area > 1000:
                max_area = area
        if max_area > 1000:
            #print('hit motion')
            break
    else:
        cap.release()
        #sys.exit(1)