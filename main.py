import os.path
import customtkinter as CTk
from tkinter import filedialog
# import tkinter as tk
from tkinter.messagebox import showwarning, showinfo
import whisper
# from PIL import Image


class Application(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("540x540")
        self.title("Транскрибатор")
        self.resizable(False, False)
        self.configure(fg_color="#c3c2c0")
        self.theme = CTk.set_default_color_theme("green")

        self.text_frame = CTk.CTkFrame(master=self, fg_color="#d9d9d9")
        self.text_frame.grid(row=0, column=0, padx=(30, 30), pady=(20, 10))

        self.dsp_lbl = CTk.CTkLabel(master=self.text_frame, text="ДСП", font=("Bold", 25), text_color="#686868")
        self.dsp_lbl.grid(row=0, column=0, pady=(5, 5))

        self.msh_lbl = CTk.CTkLabel(master=self.text_frame, text="Машинист", font=("Bold", 25), text_color="#686868")
        self.msh_lbl.grid(row=0, column=1, pady=(5, 5))

        self.dsp_text = CTk.CTkTextbox(master=self.text_frame, border_width=5, border_color="#c3c2c0",
                                       fg_color="white", text_color="#686868")
        self.dsp_text.grid(row=1, column=0, padx=(20, 20), pady=(10, 10))

        self.msh_text = CTk.CTkTextbox(master=self.text_frame, border_width=5, border_color="#c3c2c0",
                                       fg_color="white", text_color="#686868")
        self.msh_text.grid(row=1, column=1, padx=(20, 20), pady=(10, 10))

        self.msh_text.configure(state="disable")
        self.dsp_text.configure(state="disable")

        self.menu_frame = CTk.CTkFrame(master=self, fg_color="#d9d9d9")
        self.menu_frame.grid(row=2, column=0, padx=(10, 10), pady=(10, 0))

        self.menu_lbl = CTk.CTkLabel(master=self.menu_frame, text="Панель управления",
                                     font=("Bold", 20), text_color="#686868")
        self.menu_lbl.place(x=170, y=10)

        self.findFile_btn = CTk.CTkButton(master=self.menu_frame, text="Выбрать файлы",
                                          font=("Bold", 16), command=self.choose_file)
        self.findFile_btn.grid(row=1, column=0, padx=(50, 50), pady=(50, 10), ipadx=10)

        self.startTr_btn = CTk.CTkButton(master=self.menu_frame,
                                         text="Запуск", font=("Bold", 16), command=self.startTranscribe)
        self.startTr_btn.grid(row=1, column=1, padx=(50, 50), pady=(50, 10), ipadx=10)

        self.clear_btn = CTk.CTkButton(master=self.menu_frame, text="Очистить поля",
                                       font=("Bold", 16), command=self.clear)
        self.clear_btn.grid(row=2, column=0, padx=(50, 50), pady=(10, 15), ipadx=10)

        self.saveTranscribe_btn = CTk.CTkButton(master=self.menu_frame, text="Проверка ответа",
                                                font=("Bold", 16), command=self.predict)
        self.saveTranscribe_btn.grid(row=2, column=1, padx=(50, 50), pady=(10, 15), ipadx=10)

        self.paths_frame = CTk.CTkFrame(master=self.text_frame, fg_color="#d9d9d9", border_width=2, border_color="gray")
        self.paths_frame.grid(row=2, column=0, padx=(0, 10), pady=(10, 10))

        self.path_main_label = CTk.CTkLabel(master=self, text_color="#686868", text="Выбранные файлы",
                                            bg_color="#d9d9d9")
        self.path_main_label.place(x=215, y=270)

        self.dsp_file_path_lbl = CTk.CTkLabel(master=self.paths_frame, text="Файл не выбран.", text_color="#686868")
        self.dsp_file_path_lbl.grid(row=2, column=0)

        self.msh_file_path_lbl = CTk.CTkLabel(master=self.paths_frame, text="Файл не выбран.", text_color="#686868")
        self.msh_file_path_lbl.grid(row=3, column=0)

        # self.label_loading = tk.Label(master=self.menu_frame, foreground="#2d2d2d", bg="#2d2d2d", borderwidth=0)
        # self.label_loading.place(x=285, y=70)

        # self.update_frame(1)

    # def update_frame(self, frame_num):
    #     gif_path = "SVKl.gif"
    #     gif = Image.open(gif_path)
    #     num_frames = gif.n_frames
    #     photo = tk.PhotoImage(format="gif -index {}".format(frame_num), file=gif_path)
    #     self.label_loading.configure(image=photo)
    #     self.label_loading.image = photo
    #     self.after(20, self.update_frame, (frame_num + 1) % num_frames)

    def choose_file(self):
        global dsp_file_path
        global msh_file_path

        dsp_file_path = filedialog.askopenfilename()
        name = os.path.split(dsp_file_path)[-1]
        self.dsp_file_path_lbl.configure(text=name)

        msh_file_path = filedialog.askopenfilename()
        name = os.path.split(msh_file_path)[-1]
        self.msh_file_path_lbl.configure(text=name)

        self.dsp_file_path = ""
        self.msh_file_path = ""

    def startTranscribe(self):
        global dsp_file_path
        global msh_file_path

        if dsp_file_path == "" and msh_file_path == "":
            showwarning("Внимание", "Не выбраны файлы для транскрибации")
        else:
            try:
                global dsp
                global msh
                global dsp_result
                global msh_result
                model = whisper.load_model("small")
                dsp_audio = whisper.load_audio(dsp_file_path)
                dsp_result = model.transcribe(dsp_audio)

                dsp_result["text"] = dsp_result["text"].split()
                dsp = ""
                for words in dsp_result["text"]:
                    dsp += words.lower() + "\n"

                dsp = dsp.replace('.', '').replace(',', '').replace('-', '')

                self.dsp_text.configure(state="normal")
                self.dsp_text.delete("1.0", "end-1c")
                self.dsp_text.insert("1.0", dsp)
                self.dsp_text.configure(state="disabled")

                msh_audio = whisper.load_audio(msh_file_path)
                msh_result = model.transcribe(msh_audio)

                msh_result["text"] = msh_result["text"].split()
                msh = ""

                for words in msh_result["text"]:
                    msh += words.lower() + "\n"
                msh = msh.replace('.', '').replace(',', '').replace('-', '')

                self.msh_text.configure(state="normal")
                self.msh_text.delete("1.0", "end-1c")
                self.msh_text.insert("1.0", msh)
                self.msh_text.configure(state="disabled")

            except Exception as err:
                print(err)

    def clear(self):
        global dsp_file_path
        global msh_file_path
        dsp_file_path = ""
        msh_file_path = ""

        self.msh_text.configure(state="normal")
        self.dsp_text.configure(state="normal")
        self.dsp_text.delete("1.0", "end-1c")
        self.msh_text.delete("1.0", "end-1c")
        self.msh_text.configure(state="disable")
        self.dsp_text.configure(state="disable")

        self.dsp_file_path_lbl.configure(text="Файл не выбран.")
        self.msh_file_path_lbl.configure(text="Файл не выбран.")


    def predict(self):
        global dsp
        global msh

        dictionary = [
            "нулевой", "первый", "второй", "первого", "третьего", "второго",
            "третий", "четвёртый", "пятый", "четвёртого", "пятого",
            "шестой", "седьмой", "восьмой", "седьмого", "восьмого", "седьмого",
            "девятый", "десятый", "одиннадцатый", "десятого", "одиннадцатого", "десятого",
            "двенадцатый", "тринадцатый", "четырнадцатый", "тринадцатого", "четырнадцатого", "тринадцатого",
            "пятнадцатый", "шестнадцатый", "семнадцатый", "шестнадцатого", "семнадцатого", "шестнадцатого",
            "восемнадцатый", "девятнадцатый", "двадцатый", "девятнадцатого", "двадцатого", "девятнадцатого",
            "двадцать первый", "двадцать второй", "двадцать третий", "двадцать второго", "двадцать третьего",
            "двадцать второго", "двадцать четвёртый", "двадцать пятый", "двадцать шестой", "двадцать пятого",
            "двадцать шестого", "двадцать пятого", "двадцать седьмой", "двадцать восьмой", "двадцать девятый",
            "двадцать восьмого", "двадцать девятого", "двадцать восьмого", "тридцатый", "тридцать первый",
            "тридцать второй", "тридцать первого", "тридцать второго", "тридцать первого", "тридцать третий",
            "тридцать четвёртый", "тридцать пятый", "тридцать четвёртого", "тридцать пятого", "тридцать четвёртого",
            "тридцать шестой", "тридцать седьмой", "тридцать восьмой", "тридцать седьмого", "тридцать восьмого",
            "тридцать седьмого", "тридцать девятый", "сороковой", "сорок первый", "сорокового", "сорок первого",
            "сорокового", "сорок второй", "сорок третий", "сорок четвёртый", "сорок третьего", "сорок четвёртого",
            "сорок третьего", "сорок пятый", "сорок шестой", "сорок седьмой", "сорок шестого", "сорок седьмого",
            "сорок шестого", "сорок восьмой", "сорок девятый", "пятидесятый", "сорок девятого", "пятидесятого",
            "сорок девятого", "за", "с", "на", "м3", "m3" "м1", "m1", "м2", "m2", "м4", "m4", "м5", "m5", "м6", "m6",
            "путь", "пути" "тупик", "свободный", "свободен", "занят", "занятый"
        ]

        dsprap = dsp.split()
        mshrap = msh.split()

        arr1 = []
        arr2 = []

        for word1 in dsprap:
            for word2 in dictionary:
                if word1 == word2:
                    arr1.append(word1)
                    continue

        for word1 in mshrap:
            for word2 in dictionary:
                if word1 == word2:
                    arr2.append(word1)
                    continue

        arr1 = "\n".join(arr1)
        arr2 = "\n".join(arr2)
        self.dsp_text.configure(state="normal")
        self.dsp_text.delete("1.0", "end-1c")
        self.dsp_text.insert("1.0", str(arr1))
        self.dsp_text.configure(state="disabled")

        self.msh_text.configure(state="normal")
        self.msh_text.delete("1.0", "end-1c")
        self.msh_text.insert("1.0", str(arr2))
        self.msh_text.configure(state="disabled")

        if (arr1 == arr2):
            showinfo("Уведомление", "Реперные точки доклада совпадают")
        else:
            arr1 = arr1.split()
            arr2 = arr2.split()

            err = []
            for i, j in zip(arr1, arr2):
                if i != j:
                    err.append(i)
            errors = str(err)

            showwarning("Внимание", "Несовпадения в строчках: "+errors)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
