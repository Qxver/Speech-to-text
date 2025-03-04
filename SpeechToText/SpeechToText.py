from vosk import Model, KaldiRecognizer
import pyaudio


class SpeechToText:
    def __init__(self, model, text_file) -> None:
        self.model = Model(model)
        self.text_file = text_file
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

        with open(self.text_file, "w") as file:
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
    file_name = "audio.txt"  # Text file where speech output will be stored                            #
    ####################################################################################################
    stt = SpeechToText(model_path, file_name)

    try:
        stt.recognize()
    finally:
        stt.close()
