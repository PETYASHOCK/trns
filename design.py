from tkinter import *
from tkinter import ttk

root = Tk()

root.title("Траскрибатор")
root.geometry("550x400")
root.resizable(False, False)

dspLabel = ttk.Label(text="ДСП (вопрос)")
dspLabel.grid(row=0, column=0)

dspText = Text(height=10, width=20)
dspText.grid(row=1, column=0, padx=50)

trainLabel = ttk.Label(text="Машинист (ответ)")
trainLabel.grid(row=0, column=1, padx=40)

trainAnswer = Text(height=10, width=20)
trainAnswer.grid(row=1, column=1, padx=50)

chooseFile_btn = ttk.Button(text="Выбрать файл")
chooseFile_btn.place(x=50, y=200)

filePATH = ttk.Entry()
filePATH.place(x=154, y=201)

transcribe_btn = ttk.Button(text="Пуск")
transcribe_btn.place(x=50, y=230)

verdictLabel = ""
resultLabel = ttk.Label(text="Результат: "+verdictLabel)
resultLabel.place(x=50, y=270)

root.mainloop()
