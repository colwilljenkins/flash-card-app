from tkinter import *
import pandas as pd
import random

# -------------Data Handling---------------- #
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}
try:
    data = pd.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pd.read_csv('data/german_words.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')
# ------------------------------------------ #


def change_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    card.itemconfig(card_background, image=front_image)
    card.itemconfig(title, text='German', fill = 'black')
    card.itemconfig(word, text=f"{current_card['German']}", fill = 'black')
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    card.itemconfig(card_background, image=back_image)
    card.itemconfig(title, text='English', fill = 'white')
    card.itemconfig(word, text=f"{current_card['English']}", fill = 'white')

def is_known():
    to_learn.remove(current_card)
    learn_data = pd.DataFrame(to_learn)
    learn_data.to_csv('data/words_to_learn.csv', index = False)
    change_word()
# ----------------GUI----------------------- #


window = Tk()
window.title('Study German')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func = flip_card)

# image imports
cross_image = PhotoImage(file='images/wrong.png')
tick_image = PhotoImage(file='images/right.png')
front_image = PhotoImage(file='images/card_front.png')
back_image = PhotoImage(file='images/card_back.png')

# Card area
card = Canvas(width=800, height=526)
card_background = card.create_image(400, 263, image=front_image)
card.config(bg=BACKGROUND_COLOR, highlightthickness=0)
title = card.create_text(400, 150, font=('Arial', 40, 'italic'))
word = card.create_text(400, 263, font=('Arial', 60, 'bold'))
card.grid(column=0, row=0, columnspan=2)

# Correct button
correct_button = Button(image=tick_image, command=is_known)
correct_button.config(highlightthickness=0, relief='flat', bg=BACKGROUND_COLOR)
correct_button.grid(column=0, row=1)

# Wrong button
unknown_button = Button(image=cross_image, command=change_word)
unknown_button.config(highlightthickness=0, relief='flat', bg=BACKGROUND_COLOR)
unknown_button.grid(column=1, row=1)

change_word()

window.mainloop()
