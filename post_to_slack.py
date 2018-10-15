import requests
import json

import cv2
import numpy as np

def text_to_slack(text):
    #post to slack
    param = {
        'token':TOKEN,
        'channel':CHANNEL,
        'text':text,
        'as_user':'true'
    }
    requests.post(url="https://slack.com/api/chat.postMessage",params=param)


def cap_to_slack(cap, text):
    ret, frame = cap.read()
    frame = cv2.flip(frame, -1) #カメラ上下左右反転

    #画面の輝度補正｡暗いとき用
    #frame = (frame - np.mean(frame))/np.std(frame)*16+96

    path = "photo.jpg"
    cv2.imwrite(path,frame)

    #post to slack
    files = {'file': open("photo.jpg", 'rb')}
    param = {
        'token':TOKEN,
        'channels':CHANNEL,
        #'filename':"filename",
        'initial_comment':text,
        #'title': "title"
    }
    requests.post(url="https://slack.com/api/files.upload",params=param, files=files)
    os.remove('photo.jpg')