import os.path
import customtkinter as CTk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo
import whisper


class Application(CTk.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("540x500")
        self.title("Транскрибатор")
        self.resizable(False, False)

        self.text_frame = CTk.CTkFrame(master=self, fg_color="transparent")
        self.text_frame.grid(row=0, column=0, padx=(30, 30), pady=(20, 20))

        self.dsp_lbl = CTk.CTkLabel(master=self.text_frame, text="ДСП", font=("Bold", 20))
        self.dsp_lbl.grid(row=0, column=0, pady=(5, 5))

        self.msh_lbl = CTk.CTkLabel(master=self.text_frame, text="Машинист", font=("Bold", 20))
        self.msh_lbl.grid(row=0, column=1, pady=(5, 5))

        self.dsp_text = CTk.CTkTextbox(master=self.text_frame, border_width=2, border_color="gray")
        self.dsp_text.grid(row=1, column=0, padx=(20, 20), pady=(10, 10))

        self.msh_text = CTk.CTkTextbox(master=self.text_frame, border_width=2, border_color="gray")
        self.msh_text.grid(row=1, column=1, padx=(20, 20), pady=(10, 10))

        self.msh_text.configure(state="disable")
        self.dsp_text.configure(state="disable")

        self.menu_frame = CTk.CTkFrame(master=self, fg_color="transparent", border_width=2, border_color="gray")
        self.menu_frame.grid(row=2, column=0, padx=(10, 10))

        self.menu_lbl = CTk.CTkLabel(master=self.menu_frame, text="Панель управления", font=("Bold", 16))
        self.menu_lbl.place(x=190, y=10)

        self.findFile_btn = CTk.CTkButton(master=self.menu_frame, text="Выбрать файлы", font=("Bold", 16), command=self.choose_file)
        self.findFile_btn.grid(row=1, column=0, padx=(50, 50), pady=(50, 10), ipadx=10)

        self.startFile_btn = CTk.CTkButton(master=self.menu_frame, text="Запуск", font=("Bold", 16), command=self.transcribe)
        self.startFile_btn.grid(row=1, column=1, padx=(50, 50), pady=(50, 10), ipadx=10)

        self.clear_btn = CTk.CTkButton(master=self.menu_frame, text="Очистить поля", font=("Bold", 16), command=self.clear)
        self.clear_btn.grid(row=2, column=0, padx=(50, 50), pady=(10, 15), ipadx=10)

        self.saveTranscribe_btn = CTk.CTkButton(master=self.menu_frame, text="ИПС", font=("Bold", 16))
        self.saveTranscribe_btn.grid(row=2, column=1, padx=(50, 50), pady=(10, 15), ipadx=10)

        self.dsp_file_path_lbl = CTk.CTkLabel(master=self, text="Файл не выбран.")
        self.dsp_file_path_lbl.grid(row=3, column=0)

        self.msh_file_path_lbl = CTk.CTkLabel(master=self, text="Файл не выбран.")
        self.msh_file_path_lbl.grid(row=4, column=0)

    def choose_file(self):
        global dsp_file_path
        global msh_file_path

        dsp_file_path = filedialog.askopenfilename()
        name = os.path.split(dsp_file_path)[-1]
        self.dsp_file_path_lbl.configure(text=name)

        msh_file_path = filedialog.askopenfilename()
        name = os.path.split(msh_file_path)[-1]
        self.msh_file_path_lbl.configure(text=name)

    def transcribe(self):
        if not (dsp_file_path and msh_file_path):
            showwarning("Предупреждение", "Пожалуйста, выберите файлы для транскрибации.")
            return

        try:
            self.showProgressWindow()
            model = whisper.load_model("base")

            dsp_audio = whisper.load_audio(dsp_file_path)
            dsp_result = model.transcribe(dsp_audio)

            self.dsp_text.configure(state="normal")
            self.dsp_text.delete("1.0", "end-1c")
            self.dsp_text.insert("1.0", dsp_result["text"])
            self.dsp_text.configure(state="disabled")

            msh_audio = whisper.load_audio(msh_file_path)
            msh_result = model.transcribe(msh_audio)

            self.msh_text.configure(state="normal")
            self.msh_text.delete("1.0", "end-1c")
            self.msh_text.insert("1.0", msh_result["text"])
            self.msh_text.configure(state="disabled")

        except Exception as e:
            showerror("Ошибка", f"Произошла ошибка при транскрибации: {str(e)}")

    def showProgressWindow(self):
        global info_window
        info_window = CTk.CTkToplevel(self)
        info_window.title("Транскрибация")
        info_window.geometry("200x100")
        info_window.focus()

        label = CTk.CTkLabel(master=info_window, text="This is some custom information.")
        label.pack()

        close_button = CTk.CTkButton(master=info_window, text="Close", command=info_window.destroy)
        close_button.pack()

    def clear(self):
        self.msh_text.configure(state="normal")
        self.dsp_text.configure(state="normal")
        self.dsp_text.delete("1.0", "end-1c")
        self.msh_text.delete("1.0", "end-1c")
        self.msh_text.configure(state="disable")
        self.dsp_text.configure(state="disable")

        self.dsp_file_path_lbl.configure(text="Файл не выбран.")
        self.msh_file_path_lbl.configure(text="Файл не выбран.")


if __name__ == "__main__":
    app = Application()
    app.mainloop()