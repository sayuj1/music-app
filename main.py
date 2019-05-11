from tkinter import *
from pygame import mixer

root = Tk()

mixer.init() #initializing the mixer

root.geometry('500x500')

root.title('Melody')
root.iconbitmap(r'melody.ico')
text = Label(root, text='Lets make some noise')
text.pack()

#set volume
def set_vol(val):
    volume = int(val)/100
    mixer.music.set_volume(volume)

#play music
def play_music():
    mixer.music.load('ChillingMusic.wav')
    mixer.music.play()

#stop music
def stop_music():
    mixer.music.stop()

play_photo = PhotoImage(file='play.png')
playBtn = Button(root, image = play_photo, command=play_music)
playBtn.pack()

stop_photo = PhotoImage(file='stop.png')
stopBtn = Button(root, image = stop_photo, command=stop_music)
stopBtn.pack()

scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(20)
scale.pack()

root.mainloop()