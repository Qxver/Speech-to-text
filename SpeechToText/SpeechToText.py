from vosk import Model, KaldiRecognizer
import pyaudio
import time
import os.path


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
        print("Listening...")
        print("Say 'stop', 'exit', 'quit' or 'end' to stop.")

        text_file = time.strftime("%d-%m-%Y-%H-%M-%S", time.localtime())
        log_dir = os.path.join(os.getcwd(), "logs")
        log_path = os.path.join(log_dir, f"{text_file}.log")

        with open(log_path, "w") as file:
            while True:
                data = self.stream.read(4096)

                if self.recognizer.AcceptWaveform(data):
                    result = self.recognizer.Result()
                    text: str = result[14:-3]

                    if text.strip():
                        print(text)
                        file.write(f"{text}\n")

                    if text in ("stop", "quit", "end", "exit"):
                        print("Stopping the program...")
                        break

    def close(self) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.microphone.terminate()


if __name__ == "__main__":
    ####################################################################################################
    model_path = r"C:\Users\User\PycharmProjects\SpeechToText\vosk-model-small-en-us-0.15"  # English  #
    # model_path = r"C:\Users\User\PycharmProjects\SpeechToText\vosk-model-small-pl-0.22"  # Polish    #
    ####################################################################################################
    stt = SpeechToText(model_path)

    try:
        stt.recognize()
    finally:
        stt.close()
