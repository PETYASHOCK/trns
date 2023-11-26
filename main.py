from tkinter import *
from tkinter import ttk, Tk
from tkinter import filedialog
import tkinter as tk
import whisper
import os
from tkinter.messagebox import showerror, showwarning

root = Tk()


flag = False


def choose_file():
    file_path = filedialog.askopenfilename()
    name = os.path.split(file_path)[-1]
    dsp_filePATH.config(text=name)
    global dPath
    dPath = file_path

    file_path = filedialog.askopenfilename()
    name = os.path.split(file_path)[-1]
    msh_filePATH.config(text=name)
    global mPath
    mPath = file_path
    global flag
    flag = True

    if dPath == "" or mPath == "":
        dsp_filePATH.config(text="Файл не выбран")
        msh_filePATH.config(text="Файл не выбран")
        showwarning("Внимание", "Необходимо выбрать 2 файла.")


def transcribe():
    if flag:
        model = whisper.load_model("base")

        audio = whisper.load_audio(dPath)
        result = model.transcribe(audio)
        dspText.insert("1.0", result["text"])

        audio = whisper.load_audio(mPath)
        result = model.transcribe(audio)
        trainAnswer.insert("1.0", result["text"])

        verdict()
    else:
        showerror(title="Ошибка", message="Файл для транскрибации не выбран")


def verdict():
    dsp = dspText.get("1.0", "end")
    msh = trainAnswer.get("1.0", "end")
    if dsp == msh:
        resultLabel.config(text="Результат: Верно")
    else:
        resultLabel.config(text="Результат: Не верно. Повторите сообщение машинисту")


root.title("Траскрибатор")
root.geometry('530x350')
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

dsp_filePATH = tk.Label(text="Файл не выбран")
dsp_filePATH.place(x=154, y=201)

mshPATH_lbl = ttk.Label(text="Машинист")
mshPATH_lbl.place(x=154, y=224)

msh_filePATH = tk.Label(text="Файл не выбран")
msh_filePATH.place(x=154, y=240)

transcribe_btn = ttk.Button(text="Пуск", command=transcribe)
transcribe_btn.place(x=50, y=238)

verdictLabel = ""
resultLabel = ttk.Label(text="Результат: " + verdictLabel)
resultLabel.place(x=50, y=270)

root.mainloop()
