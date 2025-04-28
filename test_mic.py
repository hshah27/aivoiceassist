import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone() as source:
    print("Please speak something...")
    audio = r.listen(source, timeout=10)
    try:
        print("You said: " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")