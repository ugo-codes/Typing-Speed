from tkinter import Frame, END, Text, Label, Button
from frames.result_page import update
from wonderwords import RandomSentence

TARGET_INDEX = 42
TIMER = 61


class TypingPage(Frame):

    def __init__(self, parent, show_frame):
        Frame.__init__(self, parent)
        self.config(padx=10, pady=10)

        self.show_frame = show_frame

        self.text_position = [1.0, 1.3]
        self.sentence = ""
        self._after = None
        self.show_frame = show_frame

        self.generated_sentence_text = Text(self, height=7, width=50, bg="black", fg="white", wrap="word")
        self.generated_sentence_text.focus()
        self.generated_sentence_text.place(x=200, y=0)

        self.typing_text = Text(self, height=7, width=50)
        self.typing_text.bind(sequence="<space>", func=self.highlight_word)
        self.typing_text.place(x=200, y=150)

        self.time = Label(self)
        self.time.place(x=700, y=400)

        self.start_button = Button(self, text="Start", command=self.start)
        self.start_button.place(x=200, y=400)

    def start(self):
        self.text_position = [1.0, 1.3]
        self.sentence = ""
        self._after = None

        self.populate_generated_sentence_text()
        self.typing_text.focus()
        self.start_button.config(state="disabled")
        self.periodic()

    def generate_sentence(self) -> str:
        """
        This function generates the sentence the user will type then returns he sentence
        :return: (str) the randomly generated sentence
        """
        s = RandomSentence()
        full = ""
        for _ in range(100):
            full += f"{s.sentence()[:-1]}"
            full += " "

        full = full.lower()
        self.sentence = full
        return full

    def populate_generated_sentence_text(self):
        """
        THis function populates the text field where the user can see the sentence to type
        :return: None
        """
        sentence = self.generate_sentence()
        self.generated_sentence_text.config(state="normal")
        self.generated_sentence_text.insert("1.0", sentence)
        self.generated_sentence_text.config(state="disabled")
        self.generated_sentence_text.tag_add("pos", self.text_position[0], self.text_position[1])
        self.generated_sentence_text.tag_configure('pos', background="blue")

    def auto_scroll(self):
        """
        This method will automatically scroll the text view once the user is about to finish typing
        :return: None
        """
        global TARGET_INDEX

        try:
            target_word = self.generated_sentence_text.get("1.0", END).split()[TARGET_INDEX]
        except IndexError:
            pass
        else:
            typing_word = ""
            try:
                typing_word = self.typing_text.get("1.0", END).split()[-1]
            except IndexError:
                pass
            if typing_word == target_word:
                TARGET_INDEX += 30

                for _ in range(7):
                    self.generated_sentence_text.yview_scroll("11.0", "pixels")

    def highlight_word(self, e):
        # get the last word the user typed
        user_last_word = self.typing_text.get("1.0", END).split()[-1]
        # get all the text that's on screen
        all_text = self.generated_sentence_text.get("1.0", END)
        # split all the text into array
        all_text = all_text.split()
        # find the index of the word the user last typed then get the next index from all_text
        try:
            user_word_index = all_text.index(user_last_word) + 1
        except ValueError:
            self.generated_sentence_text.tag_configure('pos', background="red")
        else:
            # get the word at that index
            word = all_text[user_word_index]
            # replaces the word at that index
            all_text[user_word_index - 1] = "xxx"
            # find the length of the word and add one to represent the space left
            word_length = len(word) + 1
            # get the last number in the list
            # separate it by "." then pick the last value
            # convert it to an integer
            _position = int(f"{self.text_position[1]}".split(".")[1])
            # replace the end test position with a new one
            self.text_position[1] = float(f"1.{word_length + _position}")
            print(self.text_position[1])
            # remove the current tag
            # add the tag back with a new position
            # color the tag background blue
            self.generated_sentence_text.tag_delete('pos')
            self.generated_sentence_text.tag_add("pos", self.text_position[0], self.text_position[1])
            self.generated_sentence_text.tag_configure('pos', background="blue")

    def count_down(self, time: int):
        global TIMER
        self.time.config(text=f"{time}")
        TIMER = time

    def periodic(self):
        self.auto_scroll()
        self.count_down(TIMER - 1)

        if TIMER == 0:
            self.after_cancel(self._after)
            self.show_frame("ResultPage")
            self.start_button.config(state="normal")
            update(self.typing_text.get("1.0", END))
            return

        self._after = self.after(1000, self.periodic)
