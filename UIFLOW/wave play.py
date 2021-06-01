from m5stack import *
from m5stack_ui import *
from uiflow import *
import os
import gc
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)



print(os.listdir())
folder_path= 'res'
print(os.listdir(folder_path))

label0 = M5Label('Recording.wav', x=62, y=44, color=0x000, font=FONT_MONT_14, parent=None)

while(1):
  #try:
  speaker.playWAV('res/Recording.wav', rate='44100', dataf=speaker.F16B, channel=speaker.CHN_LR)
  #except:
    #print('wav play error')
    #pass
  wait_ms(1000)
    #speaker.playWAV('4S_HotelCalifornia.wav', rate='44100', dataf=speaker.F16B, channel=speaker.CHN_LR)