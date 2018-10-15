#!/usr/bin/env python3

import cv2
import numpy as np

import mod.snowboydecoder as snowboydecoder
import mod.detect_intent_texts as detect_intent_texts

import sys
import os
import subprocess
import uuid
import logging
import threading

import aiy.audio
import aiy.cloudspeech
import aiy.voicehat
import aiy.i18n

import detect_motion
import play_voice
import post_to_slack

#Slack token and channel
TOKEN = '好きなトークンを入れてね'
CHANNEL = '好きなチャンネルを選んでね'

# set log
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)

#set voice detect
#好きなホットワード的なインターホン音を引数にしてね
if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

model = sys.argv[1]

#i18n and uuid
aiy.i18n.set_language_code('ja-JP')
myuuid = str(uuid.uuid4())

def main():
    recognizer = aiy.cloudspeech.get_recognizer()

    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()
    player=aiy.audio.get_player()
    text_recognizer = detect_intent_texts.get_recognizer()
    aiy.audio.get_recorder().start()

    text_to_slack(":robot_face: イン君 : こんにちは｡私は自動応答機械､中国語の部屋の中の英国人｡ \n インターホン君｡略してイン君といいます｡只今よりあなたの代わりに受付しますね｡")
    text_to_slack(":robot_face: イン君 : 私のソースコードはこちらです｡ https://github.com/senyoltw/intercom-kun")

    while(True):
        cap = cv2.VideoCapture(0)
        cap.set(3,640) # set Width
        cap.set(4,480) # set Height

        print('detect motion')
        detect_motion_thread = threading.Thread(target=detect_motion, args=(cap,))
        detect_motion_thread.start()

        print('detect hotword')
        detect_audio_thread = threading.Thread(target=detector.start)
        detect_audio_thread.start()

        detect_motion_thread.join()
        detect_audio_thread.join()
        print('hit! motion and hotword!')

        text_to_slack(":robot_face: イン君 : あれ､誰か来たみたいです｡")

        print('cap 2 slack')
        cap_to_skack_thread = threading.Thread(target=cap_to_slack, args=(cap, ":robot_face: イン君 : 玄関の写真です",))
        cap_to_skack_thread.start()

        to_the_end = False
        while to_the_end == False:
            print('Listening...')
            text = recognizer.recognize()

            #会話中のモーションを判定｡ヒットしなければ消えたものとする
            detect_motion_thread = threading.Thread(target=detect_motion, args=(cap,))
            detect_motion_thread.start()

            if not text:
                print('Sorry, I did not hear you.')
            else:
                print('text 2 slack')
                slack_text = ':dog2: 来客者 : ' + text
                text_to_slack(slack_text)

                print('You said "', text, '"')
                answer = text_recognizer.recognize(myuuid, text)
                print('Dialogflow Intents:"', answer.query_result.intent.display_name, '"')
                print('Dialogflow result :"', answer.query_result.fulfillment_text, '"')

                print('text 2 slack')
                slack_text = ':robot_face: イン君 : ' + answer.query_result.fulfillment_text
                text_to_slack(slack_text)

                to_the_end = answer.query_result.all_required_params_present
                if to_the_end == False:
                    continue

            detect_motion_thread.join(timeout=5)
            if detect_motion_thread.is_alive() == False:
                to_the_end = False
            else:
                to_the_end = True

        print('The ENDってね')
        text_to_slack(":robot_face: イン君 : いなくなりました｡会話を終了します｡")
        cap.release()

if __name__ == '__main__':
    main()