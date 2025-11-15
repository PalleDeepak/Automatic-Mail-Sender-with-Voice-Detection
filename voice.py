import speech_recognition as sr
import time

recognizer = sr.Recognizer()

def _recognize_audio(audio, recognizer=recognizer):
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print("Speech API error:", e)
        return None

def listen_for_phrase(timeout=5, phrase_time_limit=6):
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.8)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except Exception:
            return None
    return _recognize_audio(audio)

def listen_for_text(timeout=8, phrase_time_limit=12):
    # wrapper that tries a couple times for longer texts
    attempt = 0
    while attempt < 3:
        txt = listen_for_phrase(timeout=timeout, phrase_time_limit=phrase_time_limit)
        if txt:
            # help: convert spoken ' at ' / ' dot ' to symbols if user speaks like that
            txt = txt.replace(" at ", "@").replace(" dot ", ".").replace(" underscore ", "_")
            return txt
        attempt += 1
        time.sleep(0.5)
    return None
