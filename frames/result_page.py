from tkinter import Label, Frame
# from window import visible_frame

result = None


def update(words):
    if result is None:
        return
    words = len(words.split())
    result.config(text=f"WPM: {words}")


class ResultPage(Frame):
    def __init__(self, parent, show_frame):
        global result
        Frame.__init__(self, parent)
        self.config(padx=10, pady=10)

        result = Label(self, text="WPM")
        result.place(x=250, y=200)
