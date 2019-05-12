import os
from tkinter import *
import tkinter.messagebox as mb
import tkinter.filedialog as fs
from pygame import mixer

root = Tk()

# create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# create the submenu
subMenu = Menu(menubar, tearoff=0)  # tearoff --> remove the dashed line


def open_file():
    global filename
    filename = fs.askopenfilename()
    # print(filename)


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=open_file)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=root.destroy)


def about_us():
    mb.showinfo('About Melody',
                'The is the music listening app created by Sayuj')


subMenu = Menu(menubar, tearoff=0)  # tearoff --> remove the dashed line
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

# root.resizable(False, False)
mixer.init()  # initializing the mixer

root.geometry('500x500')

root.title('Melody')
root.iconbitmap(r'melody.ico')
text = Label(root, text='Lets make some noise')
text.pack()

# set volume


def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

# play music


def play_music():
    #
    try:
        paused  #checking if pause variable is initialized or not
    except:
        try:
            mixer.music.load(filename)
            mixer.music.play()
            statusbar['text'] = "Playing Music : " + " " + os.path.basename(filename)  # printing loaded filename
            globals()['music_loaded'] = TRUE

        except:
            mb.showerror('No File', 'No File Choosen')
    else: #this block will execute if try block executed successfully
        try:
            music_stopped
        except:
            mixer.music.unpause()
            statusbar['text'] = "Music Resumed"
        else:
            # print(music_stopped)
            if(music_stopped==0):
                mixer.music.unpause()
                statusbar['text'] = "Music Resumed"
            else:
                mixer.music.play()
                statusbar['text'] = "Playing Music : " + " " + os.path.basename(filename)

# stop music
def stop_music():
    try:
        music_loaded
    except:
        mb.showerror('', 'No Music File Found')
    else:
       mixer.music.stop()
       statusbar['text'] = "Music Stopped"
       globals()['music_stopped'] = TRUE

def pause_music():
    try:
        music_loaded
    except:
        mb.showerror('', 'No Music File Found')
    else:
        global paused
        paused = TRUE
        mixer.music.pause()
        statusbar['text'] = "Music Paused"
        globals()['music_stopped'] = FALSE

# play button
play_photo = PhotoImage(file='play.png')
playBtn = Button(root, image=play_photo, command=play_music)
playBtn.pack()

# stop button
stop_photo = PhotoImage(file='stop.png')
stopBtn = Button(root, image=stop_photo, command=stop_music)
stopBtn.pack()

#pause button
pause_photo = PhotoImage(file='pause.png')
pauseBtn = Button(root, image=pause_photo, command = pause_music)
pauseBtn.pack()

# volume Control
scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(20)
mixer.music.set_volume(0.2)  # setting default volume
scale.pack()

statusbar = Label(root, text='Welcome to Music App', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.mainloop()
