
    from os import path
import yaml
from pydub import AudioSegment
import speech_recognition as sr
from google.cloud import speech_v1p1beta1 as speech
def mp3ToYML(fileName):
    inputFile = AudioSegment.from_mp3(fileName)
    inputFile.export(fileName + ".wav", format="wav")
    AUDIO_FILE = fileName + ".wav"
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        r.adjust_for_ambient_noise(source)
        audio = r.record(source)
        client = speech.SpeechClient()
        with open(audio, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code="en-US",
            enable_speaker_diarization=True,
            diarization_speaker_count=2,
        )
        response = client.recognize(config=config, audio=audio)
        result = response.results[-1]

        words_info = result.alternatives[0].words

        for word_info in words_info:
            print(
                u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
            )

        #converstations = [{'converstations' : ['soccer', 'football']}]
        #with open(r'E:\data\store_file.yaml', 'w') as file:
            #documents = yaml.dump(converstations, file)