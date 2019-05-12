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
    statusbar['text'] = os.path.basename(filename) + " Loaded"
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

# root.geometry('500x500')

root.title('Melody')
root.iconbitmap(r'melody.ico')
text = Label(root, text='Lets make some noise')
text.pack(pady=10)

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
            statusbar['text'] = "Music Resumed : " + os.path.basename(filename)
        else:
            # print(music_stopped)
            if(music_stopped==0):
                mixer.music.unpause()
                statusbar['text'] = "Music Resumed : " + os.path.basename(filename)
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
       statusbar['text'] = "Music Stopped : " + os.path.basename(filename)
       globals()['music_stopped'] = TRUE
       globals()['music_paused'] = FALSE

def pause_music():
    try:
        music_loaded
    except:
        mb.showerror('', 'No Music File Found')
    else:
        globals()['paused'] = TRUE
        mixer.music.pause()
        statusbar['text'] = "Music Paused : " + os.path.basename(filename)
        globals()['music_stopped'] = FALSE

def music_rewind():
    play_music()
    statusbar['text'] = "Music Restarted : " + os.path.basename(filename)

muted = FALSE

def mute_music():
    global muted
    if muted:  #unmute the music
        mixer.music.set_volume(0)
        scale.set(20)
        volumeBtn['image']=volume_photo
        muted=FALSE
        # volumeBtn.configure(image=mute_photo)
    else:  #mute the music
        mixer.music.set_volume(0)
        scale.set(0)
        volumeBtn['image']=mute_photo
        muted = TRUE


#####################################################middle frame containing buttons ##############################################################
mframe = Frame(root, relief = RAISED)
mframe.pack(padx=30, pady=30)

# play button
play_photo = PhotoImage(file='play.png')
playBtn = Button(mframe, image=play_photo, command=play_music)
playBtn.grid(row=0, column=0, padx=10)              #pack(side=LEFT, padx=10)

# stop button
stop_photo = PhotoImage(file='stop.png')
stopBtn = Button(mframe, image=stop_photo, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

#pause button
pause_photo = PhotoImage(file='pause.png')
pauseBtn = Button(mframe, image=pause_photo, command = pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

################################## Middle Frame End ##################################

################################## Bottom Frame Frame ##################################
bottomFrame = Frame(root)
bottomFrame.pack(pady=15)

#rewind button
rewind_photo = PhotoImage(file='previous.png')
rewindBtn = Button(bottomFrame, image=rewind_photo, command = music_rewind)
rewindBtn.grid(row = 0, column = 0)

volume_photo = PhotoImage(file='volume.png')
mute_photo = PhotoImage(file='mute.png')
volumeBtn = Button(bottomFrame, image=volume_photo, command = mute_music)
volumeBtn.grid(row = 0, column = 1)


# volume Control
scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(20)  #setting default value of the scale
mixer.music.set_volume(0.2)  # setting default volume
scale.grid(row = 0, column = 2, padx=30)

################################## Bottom Frame End ##################################

statusbar = Label(root, text='Welcome to Music App', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

root.mainloop()
