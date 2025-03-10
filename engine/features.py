import sys
sys.path.append(r"d:\miniproject\envjarvis\Lib\site-packages")

from playsound import playsound
import eel
@eel.expose


# Playing assiatnt sound function
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    