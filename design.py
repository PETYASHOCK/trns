from tkinter import *
from tkinter import ttk, Tk
from tkinter import filedialog
import tkinter as tk

import main

root: Tk = Tk()


def choose_file():
    file_path = filedialog.askopenfilename()
    dsp_filePATH.config(text=file_path)
    file_path = filedialog.askopenfilename()
    msh_filePATH.config(text=file_path)


root.title("Траскрибатор")
root.geometry('650x400')
root.resizable(False, False)

dspLabel = ttk.Label(text="ДСП (вопрос)")
dspLabel.grid(row=0, column=0)

dspText = Text(height=10, width=20)
dspText.grid(row=1, column=0, padx=50)

trainLabel = ttk.Label(text="Машинист (ответ)")
trainLabel.grid(row=0, column=1, padx=40)

trainAnswer = Text(height=10, width=20)
trainAnswer.grid(row=1, column=1, padx=50)

chooseFile_btn = ttk.Button(text="Выбрать файл", command=choose_file)
chooseFile_btn.place(x=50, y=200)

dspPATH_lbl = ttk.Label(text="ДСП")
dspPATH_lbl.place(x=154, y=185)

dsp_filePATH = tk.Label()
dsp_filePATH.place(x=154, y=201)

mshPATH_lbl = ttk.Label(text="Машинист")
mshPATH_lbl.place(x=154, y=224)

msh_filePATH = tk.Label()
msh_filePATH.place(x=154, y=240)

transcribe_btn = ttk.Button(text="Пуск")
transcribe_btn.place(x=50, y=238)

verdictLabel = ""
resultLabel = ttk.Label(text="Результат: " + verdictLabel)
resultLabel.place(x=50, y=270)

root.mainloop()
