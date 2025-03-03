from vosk import Model, KaldiRecognizer
import pyaudio


class SpeechToText:
    def __init__(self, model) -> None:
        self.model = Model(model)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.microphone = pyaudio.PyAudio()
        self.stream = self.microphone.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8192
        )
        self.stream.start_stream()

    def recognize(self) -> None:
        while True:
            data = self.stream.read(4096)

            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                text = result[14:-3]
                print(text)

                if text in ("stop", "quit", "end", "exit"):
                    print("Stopping the program...")
                    break

    def close(self) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.microphone.terminate()


if __name__ == "__main__":
    model_path = r"C:\Users\User\PycharmProjects\SpeechToText\vosk-model-small-en-us-0.15"  # English
    # model_path = r"C:\Users\User\PycharmProjects\SpeechToText\vosk-model-small-pl-0.22"  # Polish
    stt = SpeechToText(model_path)

    try:
        stt.recognize()
    finally:
        stt.close()
