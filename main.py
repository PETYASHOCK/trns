from design import *
import whisper

model = whisper.load_model("base")
audio = whisper.load_audio("") #вставлять адрес выбранный по кнопке
result = model.transcribe(audio)

dspText = result


