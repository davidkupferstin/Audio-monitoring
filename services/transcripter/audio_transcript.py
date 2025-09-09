import speech_recognition as sr
import io

class AudioTranscript:

    def __init__(self):
        self.r = sr.Recognizer()

    def audio_content_to_readable_transcription(self, audio_binary_data):
        audio_file_like_object = io.BytesIO(audio_binary_data)

        with sr.AudioFile(audio_file_like_object) as source:
            audio = self.r.record(source)
        try:
            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

