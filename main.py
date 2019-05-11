from tkinter import *
from pygame import mixer

root = Tk()

mixer.init() #initializing the mixer

root.geometry('500x500')

root.title('Melody')
root.iconbitmap(r'melody.ico')
text = Label(root, text='Lets make some noise')
text.pack()

photo = PhotoImage(file='play.png')

def play_music():
    mixer.music.load('ChillingMusic.wav')
    mixer.music.play()

playBtn = Button(root, image = photo, command=play_music)
playBtn.pack()

root.mainloop()