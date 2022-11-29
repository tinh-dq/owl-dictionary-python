import json
from tkinter import LEFT

import customtkinter as ctk
import requests

ss = requests.session()
f = open('token.json', 'r')
token = json.loads(f.read())['token']
f.close()
header = {"Authorization": f"Token {token}"}
url = "https://owlbot.info/api/v4/dictionary/"


class MainUI:
    def __init__(self, parent: ctk.CTk):
        self.content = ctk.CTkFrame(parent)
        self.content.grid(row=0, column=0, padx=10, pady=10, sticky='nswe')
        self.content.grid_columnconfigure(0, weight=1)
        self.input = ctk.CTkEntry(self.content)
        self.input.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
        ctk.CTkButton(self.content, text='Find', command=self.find).grid(row=0, column=1, padx=5, pady=5)
        self.output = ctk.CTkLabel(self.content, text='Welcome to Owlbot Dictionary.\nVisit: '
                                                      'https://github.com/tinh-dq/owl-dictionary-python',
                                   wraplength=500, anchor='w', justify=LEFT)
        self.output.grid(row=1, column=0, columnspan=2, sticky='nswe')

    def find(self):
        word = self.input.get()
        response = ss.get(url + word, headers=header)
        data = json.loads(response.text)
        # print(data)
        text = f'{word}:\nPronunciation: {data["pronunciation"]}'

        cnt = 1
        for i in data['definitions']:
            text += f'\n\n{cnt}. ({i["type"]}) {i["definition"]}'
            if not i['example'] is None:
                text += f'\nExample: {i["example"]}'
            cnt += 1
        self.output.set_text(text)


window = ctk.CTk()
window.title("Owl Dictionary")
window.geometry("550x500")
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)
main_ui = MainUI(window)
window.mainloop()
