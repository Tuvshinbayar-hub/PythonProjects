import tkinter as tk
from tkinter import messagebox

import pandas as pd
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
CARD_BACK_COLOR = "#91c2af"
FONT_LANGUAGE = ('Ariel', 40, 'italic')
FONT_WORD = ('Ariel', 60, 'bold')
id_current_timer = 0
current_word = {}
has_words = True

window = tk.Tk()
window.title('Flash Card App')
window.config(padx=50, pady=50, background=BACKGROUND_COLOR)

# Canvas section
canvas = tk.Canvas(height=526, width=800)
canvas.config(highlightthickness=0, relief='ridge', background=BACKGROUND_COLOR)
canvas.grid(row=0, column=0, columnspan=2)

# Image section
card_back_file = tk.PhotoImage(file='./images/card_back.png')
card_front_file = tk.PhotoImage(file='./images/card_front.png')
right_file = tk.PhotoImage(file='./images/right.png')
wrong_file = tk.PhotoImage(file='./images/wrong.png')

canvas_card_img = canvas.create_image(400, 263, image=card_front_file)

# Label section
language_label = tk.Label(text='Title', font=FONT_LANGUAGE, background='white')
language_label.place(x=400, y=150, anchor='center')
word_label = tk.Label(text='word', font=FONT_WORD, background='white')
word_label.place(x=400, y=263, anchor='center')

# Data section
path = 'data/words_to_learn.csv'
data_frame = None

if os.path.exists(path):
    try:
        if os.stat(path).st_size > 0:
            data_frame = pd.read_csv('data/words_to_learn.csv')
    except pd.errors.EmptyDataError:
        messagebox.showinfo(title='Congratulations!', message="You've learned them all")
        has_words = False
else:
    data_frame = pd.read_csv('data/french_words.csv')

if has_words:
    data_dicts = data_frame.to_dict(orient='records')



def remove_from_list():
    global current_word, data_dicts
    data_dicts.remove(current_word)
    pd.DataFrame(data_dicts).to_csv(path, index=False)


def flip_card(english_word):
    canvas.itemconfig(canvas_card_img, image=card_back_file)
    language_label.config(fg='white', bg=CARD_BACK_COLOR)
    word_label.config(fg='white', bg=CARD_BACK_COLOR, text=english_word)


# Button section
def next_word():
    global id_current_timer, current_word

    try:
        random_word = random.choice(data_dicts)
    except IndexError:
        messagebox.showinfo(title='Congratulations!', message="You've learned them all")
    else:
        current_word = random_word
        canvas.itemconfig(canvas_card_img, image=card_front_file)
        language_label.config(fg='black', bg='white')
        word_label.config(fg='black', bg='white', text=random_word['French'])
        if id_current_timer != 0:
            window.after_cancel(id_current_timer)
        id_current_timer = window.after(3000, flip_card, random_word['English'])


def right_button_commands():
    next_word()
    remove_from_list()


wrong_button = tk.Button(image=wrong_file, borderwidth=0, highlightthickness=0,
                         command=next_word)
wrong_button.grid(row=1, column=0)
right_button = tk.Button(image=right_file, borderwidth=0, highlightthickness=0,
                         command=right_button_commands)
right_button.grid(row=1, column=1)

if has_words:
    next_word()


window.mainloop()
