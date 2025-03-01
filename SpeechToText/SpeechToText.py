from vosk import Model, KaldiRecognizer
import pyaudio

model = Model(r"C:\Users\User\PycharmProjects\AudioToText\vosk-model-small-en-us-0.15")  # Path to vosk model
recognizer = KaldiRecognizer(model, 16000)

microphone = pyaudio.PyAudio()
stream = microphone.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
stream.start_stream()

while True:
    data = stream.read(4096)

    if recognizer.AcceptWaveform(data):
        text = recognizer.Result()
        print(text[14:-3])
        