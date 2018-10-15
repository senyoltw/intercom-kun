#!/usr/bin/env python3

import os
import sys
import tempfile
import traceback

import aiy.audio

AIY_CARDS = {
    'sndrpigooglevoi': 'Voice HAT (v1)',
    'aiyvoicebonnet': 'Voice Bonnet (v2)'
}

RECORD_DURATION_SECONDS = int(sys.argv[2])
filename = sys.argv[1]

def check_microphone_works():
    with open(filename, 'wb') as f:
        f.close()
        input('When you are ready, press Enter and say')
        print('Recording for %d seconds...' % RECORD_DURATION_SECONDS)
        aiy.audio.record_to_wave(f.name, RECORD_DURATION_SECONDS)
        print('Playing back recorded audio...')
        aiy.audio.play_wave(f.name)

    return True

def main():
    if not check_microphone_works():
        return

    print('mic record!')

if __name__ == '__main__':
    try:
        main()
    except:
        traceback.print_exc()
    finally:
        input('Press Enter to close...')