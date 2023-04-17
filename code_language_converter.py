#modules:
from tkinter.messagebox import *
from customtkinter import *
import pyperclip as pc
import tkinter as tk
import threading
import openai
import os


class APP(CTk):
    def __init__(self):
        super().__init__()
        self.title("Convert code from one language to another")
        self.geometry("1100x700")
        self.resizable(0, 0)
        self.display()

    def paste(self, interface):
        cliptext = self.clipboard_get()
        interface.insert(CURRENT, cliptext)

    def clear(self, interface):
        interface.delete(1.0, END)

    def copy(self, interface):
        text_to_copy = interface.get(1.0, END)
        pc.copy(text_to_copy)

    def convert_handler(self):
        self.code_to_convert = self.current_code_entry.get(1.0, END)
        self.convert_from = self.convert_from_select.get()
        self.convert_to = self.convert_to_select.get()
        self.convert_button['state'] = DISABLED
        self.convert_code = threading.Thread(
            target=lambda: self.convert(self.code_to_convert, self.convert_from, self.convert_to))
        self.convert_code.start()
        self.monitor(self.convert_code)

    def monitor(self, thread):
        if thread.is_alive():
            self.after(1000, lambda: self.monitor(thread))
            self.pb.start()
        else:
            self.pb.stop()
            self.convert_button['state'] = NORMAL
            self.convert_code.join()

    def display(self):
        self.current_code_frame = CTkFrame(master=self, width=550, height=680)
        self.current_code_frame.pack(padx=10, pady=10, side=LEFT)
        self.converted_code_frame = CTkFrame(self, width=550, height=680)
        self.converted_code_frame.pack(padx=10, pady=10, side=RIGHT)

        self.frame_label = CTkLabel(self.current_code_frame, text='Code on Hand', font=("Verdana", 20))
        self.frame_label.grid(row=0, column=0, columnspan=3)
        self.current_code_entry = CTkTextbox(self.current_code_frame, width=500, height=600,
                                             font=("DejaVu Sans Mono", 12))
        self.current_code_entry.grid(row=2, column=0, columnspan=3)
        self.current_entry_scroll = CTkScrollbar(self.current_code_entry)
        self.current_entry_scroll.place(relheight=1, relx=0.974)

        self.convert_from_select = CTkComboBox(master=self.current_code_frame,
                                               values=['Python', 'Java', 'C++', 'C', 'C#'])
        self.convert_from_select.grid(row=1, column=0, columnspan=2)
        self.convert_to_select = CTkComboBox(master=self.current_code_frame,
                                             values=['Python', 'Java', 'C++', 'C', 'C#'])
        self.convert_to_select.grid(row=1, column=2)
        self.frame_label = CTkLabel(self.converted_code_frame, text='Converted code', font=("Verdana", 20))
        self.frame_label.grid(row=0, column=0, columnspan=3)
        self.converted_code_entry = CTkTextbox(self.converted_code_frame, width=500, height=600,
                                               font=("DejaVu Sans Mono", 12))
        self.converted_code_entry.grid(row=1, column=0, columnspan=3)
        self.converted_entry_scroll = CTkScrollbar(self.converted_code_entry)
        self.converted_entry_scroll.place(relheight=1, relx=0.974)
        self.pb = CTkProgressBar(master=self.converted_code_frame, orientation='horizontal', mode='intermediate',
                                 width=500, progress_color='yellow')
        self.pb.grid(row=2, column=0, columnspan=3)
        self.pb.set(0.001)

        self.paste_button = CTkButton(self.current_code_frame, text="PASTE", font=("Sans-serif", 15),
                                      command=lambda: self.paste(self.current_code_entry))
        self.paste_button.grid(row=3, column=0)
        self.clear_button = CTkButton(self.current_code_frame, text="CLEAR", font=("Sans-serif", 15),
                                      command=lambda: self.clear(self.current_code_entry))
        self.clear_button.grid(row=3, column=1)

        self.convert_button = CTkButton(self.current_code_frame, text="CONVERT", font=("Sans-serif", 15),
                                        command=self.convert_handler)
        self.convert_button.grid(row=3, column=2)

        self.copy_button = CTkButton(self.converted_code_frame, text="COPY", font=("Sans-serif", 15),
                                     command=lambda: self.copy(self.converted_code_entry))
        self.copy_button.grid(row=3, column=0)
        self.clear_button1 = CTkButton(self.converted_code_frame, text="CLEAR", font=("Sans-serif", 15),
                                       command=lambda: self.clear(self.converted_code_entry))
        self.clear_button1.grid(row=3, column=1)

    def error_display(self, error):
        showerror(title="Encountered an error", message=error)

    def convert(self, code_to_convert, convert_from, convert_to):
        openai.api_key = ("OPEN_API_KEY")
        try:
            response = openai.Completion.create(
                model="code-davinci-002",
                prompt=f"##### Translate this function from {convert_from} into {convert_to}\n### {convert_from}\n{code_to_convert}\n### {convert_to}",
                temperature=0,
                max_tokens=54,
                top_p=1.0,
                frequency_penalty=0.0,
                presence_penalty=0.0,
                stop=["###"]
            )
            answer = response.choices[0].text
            self.converted_code_entry.insert(END, answer)
        except (openai.APIError, openai.InvalidRequestError) as e:
            self.error_display(e)
        except openai.error.APIConnectionError:
            self.error_display("Please connect to the internet")


app = APP()
app.mainloop()
