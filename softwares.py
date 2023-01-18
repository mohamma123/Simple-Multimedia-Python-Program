import tkinter as tk
from tkinter import filedialog, Canvas, NW
from PIL import Image, ImageTk, ImageOps
from moviepy.editor import VideoFileClip
import pygame
import pyaudio
import wave

def text_editor():
    text_editor_window = tk.Toplevel(root)
    text_box = tk.Text(text_editor_window)
    text_box.pack()
    save_button = tk.Button(text_editor_window, text="Save", command=lambda: save_text(text_box))
    save_button.pack()

def save_text(text_box):
    text = text_box.get("1.0", "end-1c")
    file = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if file:
        file.write(text)
        file.close()

def photo_editor():
    filepath = filedialog.askopenfilename()
    im = Image.open(filepath)
    im_copy = im.copy()
    photo_editor_window = tk.Toplevel(root)
    canvas = Canvas(photo_editor_window, width=im.width, height=im.height)
    canvas.pack()
    image = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0, image=image, anchor="nw")
    canvas.image = image 
    start_x, start_y, end_x, end_y = None, None, None, None
    def on_press(event):
        nonlocal start_x, start_y
        start_x, start_y = event.x, event.y
        canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='white')

    def on_release(event):
        nonlocal end_x, end_y
        end_x, end_y = event.x, event.y
        canvas.create_rectangle(start_x, start_y, end_x, end_y, outline='white')

    def apply_crop():
        im_copy.crop((start_x, start_y, end_x, end_y)).show()
        im_copy.save("cropped_image.jpg")

    def black_and_white():
        im_copy = Image.open(filepath)
        im_copy = im_copy.convert("L")
        im_copy.show()

    def invert_colors():
        im_copy = Image.open(filepath)
        im_copy = ImageOps.invert(im_copy)
        im_copy.show()

    canvas.bind("<Button-1>", on_press)
    canvas.bind("<ButtonRelease-1>", on_release)
    apply_crop_button = tk.Button(photo_editor_window, text="Apply Crop", command=apply_crop)
    apply_crop_button.pack()
    black_and_white_button = tk.Button(photo_editor_window, text="Black and White", command=black_and_white)
    black_and_white_button.pack()
    invert_colors_button = tk.Button(photo_editor_window, text="Invert Colors", command=invert_colors)
    invert_colors_button.pack()


def video_editor():
    filepath = filedialog.askopenfilename()
    clip = VideoFileClip(filepath)
    clip.preview()


def sound_editor():
    filepath = filedialog.askopenfilename()
    wf = wave.open(filepath, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(1024)

    while data:
        stream.write(data)
        data = wf.readframes(1024)

    stream.stop_stream()
    stream.close()
    p.terminate()



root = tk.Tk()
text_button = tk.Button(root, text="Text Editor", command=text_editor)
text_button.pack()
photo_button = tk.Button(root, text="Photo Editor", command=photo_editor)
photo_button.pack()
video_button = tk.Button(root, text="Video Editor", command=video_editor)
video_button.pack()
sound_button = tk.Button(root, text="Sound Editor", command=sound_editor)
sound_button.pack()
root.mainloop()
