import customtkinter as ctk
import random 
import time 

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")
letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z space"

class TypeSpeedTest():
    def __init__(self): 
        self.window = ctk.CTk()
        self.window.config(padx=30, pady=30)
        self.window.title("SpeedTest")
        self.letter_index = -1 
        self.value = ""
        self.text = "a"
        self.flag = True
        self.start_time = 0 
        self.secs = 0 
        self.mistakes = 0 

        self.entry = ctk.CTkEntry(self.window, width=300, height=30, font=("Arial", 25))
        self.entry.grid(column=1, row=1, padx=20, pady=10)
        self.entry.bind("<KeyRelease>", self.handle_text)
        self.entry.bind("<space>", self.clear_text)
        self.entry.bind("<BackSpace>", self.back)

        self.textbox = ctk.CTkTextbox(self.window, width=600, height=200, font=("Arial", 25), spacing2=10, wrap="word")
        self.textbox.grid(column=1, row=0, pady=10)
        self.get_words(30)
        
        self.textbox.tag_config("red", foreground="red")
        self.textbox.tag_config("green", foreground="green")
        self.textbox.tag_config("center", justify="center")

        self.restart_btn = ctk.CTkButton(self.window, height=30, text="Restart", command=lambda: self.get_words(30), font=("TkDefaultFont", 15, "bold"))
        self.restart_btn.grid(column=1, row=2, padx=20, pady=10)
        
        self.btn_frame = ctk.CTkFrame(self.window)
        self.btn_frame.grid(column=1, row=3, pady=10)

        self.btn_10 = ctk.CTkButton(self.btn_frame, height=30, width=50, text="10", command=lambda: self.get_words(10), font=("TkDefaultFont", 15, "bold"))
        self.btn_10.grid(column=0, row=0, padx=10, pady=10)

        self.btn_20 = ctk.CTkButton(self.btn_frame, height=30, width=50, text="20", command=lambda: self.get_words(20), font=("TkDefaultFont", 15, "bold"))
        self.btn_20.grid(column=1, row=0, padx=10, pady=10)

        self.btn_30 = ctk.CTkButton(self.btn_frame, height=30, width=50, text="30", command=lambda: self.get_words(30), font=("TkDefaultFont", 15, "bold"))
        self.btn_30.grid(column=2, row=0, padx=10, pady=10)

    def handle_text(self, event):
            if self.flag:
                self.start_time = time.time()
                self.flag = False
            try:
                self.value = self.entry.get()
            except:
                self.value = ""
            if event.keysym in letters:
                self.letter_index += 1 
                
                expected_value = self.textbox.get("1.0", "end")

                if expected_value[self.letter_index] == self.value[-1]:
                        self.textbox.tag_add("green", f"1.{self.letter_index}")
                        self.textbox.tag_remove("red", f"1.{self.letter_index}")
                else:
                    self.mistakes += 1
                    self.textbox.tag_add("red", f"1.{self.letter_index}")
                    self.textbox.tag_remove("green", f"1.{self.letter_index}")

    def clear_text(self, event):
        if self.value == self.text.split()[-1] or self.value == " " + self.text.split()[-1]:
            self.secs = time.time() - self.start_time
            self.textbox.configure(state="normal")
            self.textbox.delete("1.0", "end")
            self.wpm = round(len(self.text.split()) / self.secs * 60)
            self.cpm = round((len(self.text) - 2) / self.secs * 60)
            self.accuracy = round((1 - self.mistakes / (len(self.text) - 2)) * 100)
            self.data = f"WPM: {self.wpm} \n CPM: {self.cpm} \n Mistakes: {self.mistakes} \n Accuracy: {self.accuracy}%"
            self.textbox.insert("1.0", self.data, "center")
            self.textbox.configure(state="disabled")
        self.entry.delete(0, "end")
        
    def back(self, event):
         if self.value != "" and self.value != " ":
            self.textbox.tag_remove("red", f"1.{self.letter_index}")
            self.textbox.tag_remove("green", f"1.{self.letter_index}")
            self.letter_index -= 1

    def get_words(self, x):
        self.letter_index = -1 
        self.value = ""
        self.clear_text(None)
        self.flag = True
        self.start_time = 0 
        self.secs = 0 
        self.mistakes = 0 

        with open("words.txt") as file:
            words = file.read().split()
            self.text = " ".join(random.choice(words) for _ in range(x))
        self.textbox.configure(state="normal")
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", self.text, "center")
        self.textbox.configure(state="disabled")

if __name__ == "__main__":
    app = TypeSpeedTest()
    app.window.mainloop()