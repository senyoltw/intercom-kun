#!/usr/bin/env python3

import os
import aiy.audio

def execution(voice_name):
    voice_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'voice', voice_name) + '.py'
    if os.path.exists(voice_path) == True:
       print('voice', voice_path, 'found!')
       print('voice play start!')
       aiy.audio.play_wave(voice_path)
       print('voice play end!')
       return result
    else:
       return None