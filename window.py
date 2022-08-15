from tkinter import Tk, Frame
from frames.typing_page import TypingPage
from frames.result_page import ResultPage

_visible_frame = ""


def visible_frame():
    return visible_frame


class Window:

    def __init__(self):
        # initialize the window
        window = Tk()
        # sets the title of the window
        window.title("Typing Speed App")
        # sets the minimum width and height of the window
        window.minsize(width=800, height=500)
        window.grid_rowconfigure(0, weight=1)
        window.grid_columnconfigure(0, weight=1)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = Frame(window)
        container.grid(column=0, row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # creates a dictionary with the key being the name of the frame ad the value the frame itself
        for f in (TypingPage, ResultPage):
            frame_name = f.__name__
            frame = f(parent=container, show_frame=self.show_frame)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # opens with the start page
        self.show_frame("TypingPage")

        # keep the window active and running
        window.mainloop()

    def show_frame(self, frame_name: str):
        global _visible_frame
        frame = self.frames[frame_name]
        frame.tkraise()
        _visible_frame = frame_name
