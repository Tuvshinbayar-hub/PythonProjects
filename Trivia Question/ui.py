import tkinter as tk

from tkinter import messagebox
from quiz_brain import QuizBrain
THEME_COLOR = "#375362"
FONT_MAIN = ('Arial', 16, 'italic')


class QuizInterface:
    def __init__(self, quiz_brain: QuizBrain):
        self.quiz_brain = quiz_brain
        self.window = tk.Tk()
        self.window.title('Quizzler')
        self.window.config(bg=THEME_COLOR)
        self.canvas = tk.Canvas()
        self.canvas.config(width=300, height=250)
        self.canvas.grid(column=0, row=1, columnspan=2, pady=30, padx=20)
        self.text = self.canvas.create_text(
            150,
            125,
            width=280,
            font=FONT_MAIN,
            text='Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        self.score = tk.Label(text='Score: 0')
        self.score.config(bg=THEME_COLOR, fg='white')
        self.score.grid(column=1, row=0, pady=20)

        photo_image_true = tk.PhotoImage(file='images/true.png')
        photo_image_false = tk.PhotoImage(file='images/false.png')
        self.button_true = tk.Button(image=photo_image_true)
        self.button_true.config(highlightthickness=0, highlightbackground=THEME_COLOR, borderwidth=0,
                                command=self.true_button_pressed)
        self.button_true.grid(column=0, row=2, pady=20)
        self.button_false = tk.Button(image=photo_image_false)
        self.button_false.config(highlightthickness=0, highlightbackground=THEME_COLOR, borderwidth=0,
                                 command=self.false_button_pressed)
        self.button_false.grid(column=1, row=2, pady=20)

        self.get_next_question()

        self.window.mainloop()

    def get_next_question(self):
        self.canvas.config(bg='white')

        if self.quiz_brain.still_has_questions():
            self.score.config(text=f'Score: {self.quiz_brain.score}')
            self.canvas.itemconfig(self.text, text=self.quiz_brain.next_question())

        else:
            self.button_false.config(state='disabled')
            self.button_true.config(state='disabled')
            messagebox.showinfo(
                title='Score!',
                message=f"Your current score is: {self.quiz_brain.score}/{self.quiz_brain.question_number}")

    def true_button_pressed(self):
        if self.quiz_brain.check_answer('true'):
            self.canvas.config(bg='green')
        else:
            self.canvas.config(bg='red')

        self.window.after(700, self.get_next_question)

    def false_button_pressed(self):
        if self.quiz_brain.check_answer('false'):
            self.canvas.config(bg='green')
        else:
            self.canvas.config(bg='red')

        self.window.after(700, self.get_next_question)
