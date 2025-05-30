import sys
sys.path.append(r"d:\miniproject\envjarvis\Lib\site-packages")

import os
import re
import sqlite3
import struct
import time
import webbrowser
import pywhatkit as kit
from playsound import playsound
import eel
import pyaudio
import pvporcupine
import subprocess
import pyautogui
from engine.command import speak
from engine.helper import remove_words
# from pipes import quote
import shlex
from engine.helper import extract_yt_term
from engine.config import ASSISTANT_NAME
from hugchat import hugchat

# Initialize eel
eel.init('web')

# Database connection
conn = sqlite3.connect("jarvis.db")
cursor = conn.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    app_name = query.strip().lower()

    if app_name != "":
        try:
            # Check in sys_command
            cursor.execute(
                'SELECT path FROM sys_command WHERE name = ?', (app_name,))
            results = cursor.fetchall()

            if results:
                speak(f"Opening {app_name}")
                os.startfile(results[0][0])
            else:
                # Check in web_command
                cursor.execute(
                    'SELECT url FROM web_command WHERE name = ?', (app_name,))
                results = cursor.fetchall()

                if results:
                    speak(f"Opening {app_name}")
                    webbrowser.open(results[0][0])
                else:
                    # Attempt to open as a system app
                    speak(f"Opening {app_name}")
                    try:
                        os.system(f'start {app_name}')
                    except Exception:
                        speak(f"Could not open {app_name}")
        except Exception as e:
            speak(f"Something went wrong: {str(e)}")
    else:
        speak("Command not found")

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak(f"Playing {search_term} on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Could not understand the YouTube search term.")


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
       
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["nova"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detetcted for not
            if keyword_index>=0:
                print("hotword detected")

                # pressing shorcut key win+j
                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")
                
    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

def findContact(query):
    
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'wahtsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0


def whatsApp(mobile_no, message, flag, name):
    if flag == 'message':
        encoded_message = shlex.quote(message)
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        nova_message = f"Message sent successfully to {name}"

    elif flag == 'call':
        whatsapp_url = f"whatsapp://call?phone={mobile_no}"
        nova_message = f"Calling {name}"

    else:  # Video call
        whatsapp_url = f"whatsapp://send?phone={mobile_no}"  # Open chat first
        nova_message = f"Starting video call with {name}"

    # Open WhatsApp using os.system
    os.system(f'start "" "{whatsapp_url}"')
    time.sleep(5)  # Allow WhatsApp to open

    # For messages, press Enter to send
    if flag == 'message':
        pyautogui.press('enter')

    # For video calls, trigger the video call shortcut
    elif flag == 'video call':
        pyautogui.hotkey('ctrl', 'shift', 'v')  # WhatsApp video call shortcut
        time.sleep(1)
        pyautogui.press('enter')

    speak(nova_message)

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response =  chatbot.chat(user_input)
    print(response)
    speak(response)
    return response