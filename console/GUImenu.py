#! /usr/bin/env python

import platform
import sys
import console_actions_events
import console_actions_home_backup
import console_actions_sikuli
import console_actions_display_remote_time
import console_actions_play_random_track

import Tkinter
from Tkinter import *

class App:

    def __init__(self, master):
        frame = Frame(master)

        Label(frame, text="Play Random MP3", width=50).pack(side=TOP)
        self.action30 = Button(frame, text="Play Track", fg="SeaGreen", command=self.action30)
        self.action30.pack(side=TOP)

        Label(frame, text="Events", width=50).pack(side=TOP)
        self.action1 = Button(frame, text="Add Event", fg="SeaGreen", command=self.action1)
        self.action1.pack(side=TOP)

        Label(frame, text="Home Backup").pack(side=TOP)
        self.action10 = Button(frame, text="Delete USB HDD and copy everything again", fg="SeaGreen", command=self.action2)
        self.action10.pack(side=TOP)
        self.action11 = Button(frame, text="Delete QNAP HDD and copy everything again", fg="SeaGreen", command=self.action3)
        self.action11.pack(side=TOP)

        Label(frame, text="-------------").pack(side=TOP)
        self.button = Button(frame, text="Quit", fg="red", command=frame.quit)
        self.button.pack()

        frame.pack()
        
    def action1(self):
        console_actions_events.add_event()

    def action2(self):
        console_actions_home_backup.delete_backup_and_recopy_to_USB_HDD()

    def action3(self):
        console_actions_home_backup.delete_backup_and_recopy_to_QNAP_HDD()

    def action30(self):
        console_actions_play_random_track.play_random_mp3()


root = Tk()
root.title("AlluCloud2")
root.geometry("640x480+20+60")

app = App(root)
 
root.mainloop()
