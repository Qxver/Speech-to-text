from vosk import Model, KaldiRecognizer
import pyaudio


def speech_to_text() -> None:
    model = Model(r"C:\Users\User\PycharmProjects\SpeechToText\vosk-model-small-en-us-0.15")  # English
    #model = Model(r"C:\Users\User\PycharmProjects\SpeechToText\vosk-model-small-pl-0.22")  # Polish
    recognizer = KaldiRecognizer(model, 16000)

    microphone = pyaudio.PyAudio()
    stream = microphone.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    while True:
        data = stream.read(4096)

        if recognizer.AcceptWaveform(data):
            text = recognizer.Result()
            text = text[14:-3]
            print(text)

            if text == "stop" or text == "quit":
                print("Stopping the program...")
                break


speech_to_text()
        