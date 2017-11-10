#! /usr/bin/env python

import sys
import console_actions_events
import console_actions_home_backup
import console_actions_sikuli
import Tkinter
from Tkinter import *

class App:

    def __init__(self, master):
        frame = Frame(master)

        Label(frame, text="Events", width=50).pack(side=TOP)
        self.action1 = Button(frame, text="Add Event", fg="SeaGreen", command=self.action1)
        self.action1.pack(side=TOP)

        Label(frame, text="Home Backup").pack(side=TOP)
        self.action10 = Button(frame, text="Delete USB HDD and copy everything again", fg="SeaGreen", command=self.action2)
        self.action10.pack(side=TOP)
        self.action11 = Button(frame, text="Delete QNAP HDD and copy everything again", fg="SeaGreen", command=self.action3)
        self.action11.pack(side=TOP)

        Label(frame, text="Open With Sikuli", width=50).pack(side=TOP)
        self.action20 = Button(frame, text="Facebook", fg="SeaGreen", command=self.action4)
        self.action20.pack(side=TOP)
        self.action21 = Button(frame, text="Workflowy", fg="SeaGreen", command=self.action5)
        self.action21.pack(side=TOP)
        self.action22 = Button(frame, text="Freecodecamp", fg="SeaGreen", command=self.action6)
        self.action22.pack(side=TOP)
        self.action22 = Button(frame, text="Own website", fg="#cc33ff", command=self.action7)
        self.action22.pack(side=TOP)

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

    def action4(self):
        console_actions_sikuli.open_facebook()

    def action5(self):
        console_actions_sikuli.open_workflowy()

    def action6(self):
        console_actions_sikuli.open_freecodecamp()

    def action7(self):
        console_actions_sikuli.open_allan_wilson_net()


root = Tk()
root.title("AlluCloud2")

app = App(root)
 
root.mainloop()
