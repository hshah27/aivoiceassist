import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)

    try:
        eel.DisplayMessage(text)
    except:
        print("[Warning] Cannot send DisplayMessage, socket might be closed.")

    engine.say(text)

    try:
        eel.receiverText(text)
    except:
        print("[Warning] Cannot send receiverText, socket might be closed.")

    engine.runAndWait()



def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
       
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        try:
            eel.senderText(query)
        except:
            print("[Warning] Cannot send text, socket might be closed.")
    else:
        query = message
        try:
            eel.senderText(query)
        except:
            print("[Warning] Cannot send text, socket might be closed.")

    try:
        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            flag = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):
                if "send message" in query:
                    flag = 'message'
                    speak("what message to send")
                    query = takecommand()
                    
                elif "phone call" in query:
                    flag = 'call'
                    speak("who do you want to call?")
                    name = takecommand()
                else:
                    flag = 'video call'
                whatsApp(contact_no, query, flag, name)
        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print(f"[ERROR] Command execution failed: {e}")

    try:
        eel.ShowHood()
    except:
        print("[Warning] Cannot update UI, socket might be closed.")

    # eel.ShowHood()