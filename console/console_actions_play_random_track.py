import subprocess
import os
import random

MUSIC_COLLECTION = "D:\\ALLUSTORE\\allanBackup\\music"

def play_random_mp3():

    # Get all files
    file_list = []
    mp3_list = []
    for root, _, filenames in os.walk(MUSIC_COLLECTION):
        for filename in filenames:
            file_list.append(os.path.join(root, filename))

    for x in file_list:
        if x[-3:] == "mp3":
            mp3_list.append(x)

    # Play random track
    TRACK = mp3_list[random.randrange(len(mp3_list))]

    print("Track = " + TRACK)

    p = subprocess.Popen(["C:\\Program Files\\VideoLAN\VLC\\vlc.exe", TRACK])
