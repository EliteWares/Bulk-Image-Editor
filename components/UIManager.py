from tkinter import Tk, filedialog, Button

import os
import components.FaceDetection as Fd
import blemish as bl
import subprocess


BG_COLOR = "#181818"
FONT_COLOR = "#910A67"

class UIManager:

    def __init__(me) -> None:
        me.root = Tk()
        me.input_path = ""
        me.output_path = "imgs/output/"

    def select_upload_folder(me):
        currdir = os.getcwd()
        me.input_path = filedialog.askopenfilename(parent=me.root, initialdir=currdir, title='Please select a directory',)
        
        #currdir = me.input_path.replace("\\","/")
        

    def detect(me):
       Fd.detect_face(me.input_path)

    def remove_blemish(me):
        #bl.start(me.input_path)
        subprocess.run(['python', 'blemish.py', me.input_path])

    def start(me):
        me.root.geometry("500x500")
        me.root.title("Bulk Image Editor")
        #me.root.iconbitmap("ytd_icon.ico")
        me.root.config(background=BG_COLOR)

        upload_btn = Button(me.root, text='Upload Files', command=me.select_upload_folder)
        upload_btn.pack()

        detect_btn = Button(me.root, text='Detect Face', command=me.detect)
        detect_btn.pack()

        blem_btn = Button(me.root, text='Remove Blemish', command=me.remove_blemish)
        blem_btn.pack()

        me.root.mainloop()