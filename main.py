import eel
from engine.features import *
from engine.command import *

def start():
    eel.init("www")
    playAssistantSound()
    eel.start('index.html', mode='edge', host='localhost')

#  d:\miniproject\envjarvis\Scripts\activate       for activating venv
# for running only py code file      python -u "d:\miniproject\engine\command.py"      python -u "d:\aivoiceassist\run.py"   