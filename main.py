import os
from tkinter import *
import tkinter.messagebox as mb
import tkinter.filedialog as fs
from mutagen.mp3 import MP3  #for getting metadata from the file bcz in pygame mixer it does not work for mp3 file due to large size
from pygame import mixer
import time
import threading

root = Tk()

# Root Window = filelabel, statusbar
# Left Frame = ListBox(Playlist)
# Right Frame = total_time, current_time, play,stop,pause buttons, volume slider, mute, restart button

# create the menubar
menubar = Menu(root)
root.config(menu=menubar)

# playList --> fullpath + filename 
# playListBox --> filename

playList = []

def open_file():
    global filename_path
    filename_path = fs.askopenfilename()
    statusbar['text'] = os.path.basename(filename_path) + " Loaded"
    add_to_playList(filename_path)
    # print(filename_path)

def add_to_playList(filename):
    #Songs playlist
    filename=os.path.basename(filename)
    index = 0
    playListBox.insert(index, filename)
    playList.insert(index, filename_path)
    index+=1


def about_us():
    mb.showinfo('About Melody',
                'The is the music listening app created by Sayuj')



# create the submenu
subMenu = Menu(menubar, tearoff=0)  # tearoff --> remove the dashed line

menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=open_file)
subMenu.add_separator()
subMenu.add_command(label="Exit", command=root.destroy)

subMenu = Menu(menubar, tearoff=0)  # tearoff --> remove the dashed line
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

# root.resizable(False, False)
mixer.init()  # initializing the mixer

# root.geometry('500x500')

root.title('Melody')
root.iconbitmap(r'melody.ico')

filelabel = Label(root, text='Listen Your Favorites Songs')
filelabel.pack()

statusbar = Label(root, text='Welcome to Music App', relief=SUNKEN, anchor=W)
statusbar.pack(side=BOTTOM, fill=X)

############################Left Frame ####################################
leftFrame = Frame(root)
leftFrame.pack(side=LEFT,padx=30)

playListBox = Listbox(leftFrame)
playListBox.pack()

addBtn = Button(leftFrame, text="+ Add", command=open_file)
addBtn.pack(side=LEFT)

delBtn = Button(leftFrame, text="- Delete")
delBtn.pack(side=LEFT)

##########################################################################

##############################Right Frame ################################
rightFrame = Frame(root)
rightFrame.pack()

lengthlabel = Label(rightFrame, text='Total Length  --:--')
lengthlabel.pack(pady=5)

Currentlabel = Label(rightFrame, text='Current Length  --:--', relief = GROOVE)
Currentlabel.pack()


# set volume
def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

def start_count(t):
    global pause
    current_time = 0
    while current_time<=t and mixer.music.get_busy():  # if mixer get stop it returns false
        if pause:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            Currentlabel['text'] = 'Current Length '+ timeformat
            time.sleep(1) #value is in second
            current_time = current_time+1


#show details
def show_details(play_song):
    filelabel['text'] = "Playing " + " - " + os.path.basename(play_song)  # printing loaded play_song
    
    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()
    
    #divmod - total_length//60, total_length%60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    lengthlabel['text'] = 'Total Length '+ timeformat

    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()
    # start_count(total_length)

playSong = ''

def play_music():
    try:
        paused  # checking if pause variable is initialized or not
    except:
        try:
            mixer.music.stop()
            time.sleep(1)
            selectedSong = playListBox.curselection() #getting selected song from the listBox
            selectedSong = int(selectedSong[0])
            globals()['playSong'] = playList[selectedSong]
            # mixer.music.load(filename_path)
            mixer.music.load(playSong)
            mixer.music.play()
            # statusbar['text'] = "Playing Music : " + " " +  os.path.basename(filename_path)  # printing loaded filename_path
            statusbar['text'] = "Playing Music : " + " " +  os.path.basename(playSong)
            globals()['music_loaded'] = TRUE
            show_details(playSong)

        except:
            mb.showerror('No File', 'No File Choosen')
    else:  # this block will execute if try block executed successfully
        try:
            music_stopped
        except:
            mixer.music.unpause()
            statusbar['text'] = "Music Resumed : " + os.path.basename(playSong)
        else:
            # print(music_stopped)
            if(music_stopped == 0):
                mixer.music.unpause()
                global pause
                pause = FALSE
                statusbar['text'] = "Music Resumed : " + \
                    os.path.basename(playSong)
            else:
                mixer.music.play()
                statusbar['text'] = "Playing Music : " + \
                    " " + os.path.basename(playSong)
                show_details(playSong)

# stop music

def stop_music():
    try:
        music_loaded
    except:
        mb.showerror('', 'No Music File Found')
    else:
        mixer.music.stop()
        statusbar['text'] = "Music Stopped : " + os.path.basename(playSong)
        globals()['music_stopped'] = TRUE
        globals()['music_paused'] = FALSE

pause = FALSE
def pause_music():
    try:
        music_loaded
    except:
        mb.showerror('', 'No Music File Found')
    else:
        globals()['paused'] = TRUE
        global pause
        pause = TRUE
        mixer.music.pause()
        statusbar['text'] = "Music Paused : " + os.path.basename(playSong)
        globals()['music_stopped'] = FALSE


def music_rewind():
    stop_music()
    time.sleep(1) 
    play_music()
    statusbar['text'] = "Music Restarted : " + os.path.basename(playSong)


muted = FALSE
def mute_music():
    global muted
    if muted:  # unmute the music
        mixer.music.set_volume(0)
        scale.set(20)
        volumeBtn['image'] = volume_photo
        muted = FALSE
        # volumeBtn.configure(image=mute_photo)
    else:  # mute the music
        mixer.music.set_volume(0)
        scale.set(0)
        volumeBtn['image'] = mute_photo
        muted = TRUE


#####################################################middle frame containing buttons ##############################################################
mframe = Frame(rightFrame, relief=RAISED)
mframe.pack(padx=30, pady=30)

# play button
play_photo = PhotoImage(file='images/play.png')
playBtn = Button(mframe, image=play_photo, command=play_music)
playBtn.grid(row=0, column=0, padx=10)  # pack(side=LEFT, padx=10)

# stop button
stop_photo = PhotoImage(file='images/stop.png')
stopBtn = Button(mframe, image=stop_photo, command=stop_music)
stopBtn.grid(row=0, column=2, padx=10)

# pause button
pause_photo = PhotoImage(file='images/pause.png')
pauseBtn = Button(mframe, image=pause_photo, command=pause_music)
pauseBtn.grid(row=0, column=1, padx=10)

################################## Middle Frame End ##################################

################################## Bottom Frame Frame ##################################
bottomFrame = Frame(rightFrame)
bottomFrame.pack(pady=15)

# rewind button
rewind_photo = PhotoImage(file='images/previous.png')
rewindBtn = Button(bottomFrame, image=rewind_photo, command=music_rewind)
rewindBtn.grid(row=0, column=0)

volume_photo = PhotoImage(file='images/volume.png')
mute_photo = PhotoImage(file='images/mute.png')
volumeBtn = Button(bottomFrame, image=volume_photo, command=mute_music)
volumeBtn.grid(row=0, column=1)


# volume Control
scale = Scale(bottomFrame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(20)  # setting default value of the scale
mixer.music.set_volume(0.2)  # setting default volume
scale.grid(row=0, column=2, padx=30)

################################## Bottom Frame End ##################################

def on_closing():    
    mixer.music.stop() #for stopping music before exiting to avoid the main thread error
    root.destroy()
    
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
