from tkinter import *
from tkinter import filedialog
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root = Tk()
root.title('Music Player')
root.geometry("600x350")

pygame.mixer.init()

def play_time():
    if stopped:
        return
    
    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Habiba/Desktop/Music Player/Songs/{song}.mp3'
    song_mut = MP3(song)
    
    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))
    
    current_time += 1
    if int(my_slider.get()) == int(current_time):
        status_bar.config(text = f'Time Elapsed: {converted_song_length}')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_position = int(song_length)
        my_slider.config(to = slider_position, value = int(current_time))
    else:
        slider_position = int(song_length)
        my_slider.config(to = slider_position, value = int(my_slider.get()))
        converted_current_time = time.strftime('%M:%S', time.gmtime(my_slider.get()))
        status_bar.config(text=f'Time Elapsed: {converted_current_time} of {converted_song_length}')
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)
        
    status_bar.after(1000, play_time)
    
def add_song():
    song = filedialog.askopenfilename(initialdir ='Songs/', title = "Choose a Song", filetypes = (("mp3 Files", "*.mp3"), ))
    song = song.replace("C:/Users/Habiba/Desktop/Music Player/Songs/", "")
    song = song.replace(".mp3", "")
    song_box.insert(END, song)

def add_many_song():
    songs = filedialog.askopenfilenames(initialdir = 'Songs/', title = "Choose a Song", filetypes = (("mp3 Files", "*.mp3"), ))
    
    for song in songs:
        song = song.replace("C:/Users/Habiba/Desktop/Music Player/Songs/", "")
        song = song.replace(".mp3", "") 
        song_box.insert(END, song)

def delete_song():
    stop()
    song_box.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    song_box.delete(0, END)
    pygame.mixer.music.stop()
    
def play():
    stopped = False
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Habiba/Desktop/Music Player/Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_time()
    
def back():
    back_one = song_box.curselection()
    back_one = back_one[0] - 1
    song = song_box.get(back_one)
    song = f'C:/Users/Habiba/Desktop/Music Player/Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0)
    song_box.selection_clear(0, END)
    song_box.activate(back_one)
    song_box.selection_set(back_one, last = None)

def next():
    next_one = song_box.curselection()
    next_one = next_one[0] + 1
    song = song_box.get(next_one)
    song = f'C:/Users/Habiba/Desktop/Music Player/Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0)
    song_box.selection_clear(0, END)
    song_box.activate(next_one)
    song_box.selection_set(next_one, last = None)

global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused
    
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True
        
global stopped
stopped = False
 
def stop():
    status_bar.config(text = '')
    my_slider.config(value = 0)
    pygame.mixer.music.stop()
    song_box.selection_clear(ACTIVE)
    status_bar.config(text = '')
    global stopped
    stopped = True 
    
def slider(X):
    song = song_box.get(ACTIVE)
    song = f'C:/Users/Habiba/Desktop/Music Player/Songs/{song}.mp3'
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops = 0, start = int(my_slider.get()))

def volume(X):
  pygame.mixer.music.set_volume(volume_slider.get()) 
  current_volume = pygame.mixer.music.get_volume()
  current_volume = int(current_volume * 100)
  volume_label.config(text = current_volume)
    
master_frame = Frame(root)
master_frame.pack(pady = 20)

volume_frame = LabelFrame(master_frame, text = "Volume")
volume_frame.grid(row = 0, column = 1)
volume_label = Label(master_frame, text = "100")
volume_label.grid(row = 1, column = 1)


song_box = Listbox(master_frame, bg = "black", fg = "green", width = 60, selectbackground = "gray", selectforeground = "black")
song_box.grid(row=0, column=0)

back_btn = PhotoImage(file = 'Images/back.png')
next_btn = PhotoImage(file = 'Images/next.png')
play_btn = PhotoImage(file = 'Images/play.png')
pause_btn = PhotoImage(file = 'Images/pause.png')
stop_btn = PhotoImage(file = 'Images/stop.png')

control_frame = Frame(master_frame)
control_frame.grid(row = 1, column = 0)

back_button = Button(control_frame, image = back_btn, borderwidth = 0, command = back)
next_button = Button(control_frame, image = next_btn, borderwidth = 0, command = next)
play_button = Button(control_frame, image = play_btn, borderwidth = 0, command = play)
pause_button = Button(control_frame, image = pause_btn, borderwidth = 0, command = lambda: pause(paused))
stop_button = Button(control_frame, image = stop_btn, borderwidth = 0,command = stop)

back_button.grid(row = 0, column = 0)
next_button.grid(row = 0, column = 1)
play_button.grid(row = 0, column = 2)
pause_button.grid(row = 0, column = 3)
stop_button.grid(row = 0, column = 4)

my_menu = Menu(root)
root.config(menu = my_menu)

add_songs = Menu(my_menu)
my_menu.add_cascade(label = "Add Songs", menu = add_songs)
add_songs.add_command(label = "Add One Song to Playlist" , command = add_song)
add_songs.add_command(label = "Add Many Song to Playlist" , command = add_many_song)

remove_songs = Menu(my_menu)
my_menu.add_cascade(label = "Remove Songs", menu = remove_songs)
remove_songs.add_command(label = "Delete A Song from Playlist", command = delete_song)
remove_songs.add_command(label = "Delete All Songs from Playlist", command = delete_all_songs)

status_bar = Label(root, text = '', bd = 1, relief = GROOVE, anchor = E)
status_bar.pack(fill = X, side = BOTTOM, ipady = 2)

my_slider = ttk.Scale(master_frame, from_ = 0, to = 100, orient = HORIZONTAL, value = 0, command = slider, length = 360)
my_slider.grid(row = 2, column = 0)

volume_slider = ttk.Scale(volume_frame, from_ = 0, to = 1, orient = VERTICAL, value = 1, command = volume, length = 125)
volume_slider.pack()

root.mainloop()