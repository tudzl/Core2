#wav_player v1.1
from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5stack import mic
import os
import gc
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


image_BG = M5Img("res/SmartENV_logo.png", x=0, y=0, parent=None)
Title = M5Label('Core2 wav player demo', x=20, y=5, color=0x2517de, font=FONT_MONT_14, parent=None)


print(os.listdir())
folder_path= 'res'
print(os.listdir(folder_path))

label1 = M5Label('BtnA->Mic Record 3s', x=20, y=40, color=0x000, font=FONT_MONT_14, parent=None)
label2 = M5Label('BtnB->play Recording.wav', x=20, y=60, color=0xaaaa00, font=FONT_MONT_14, parent=None)
label3 = M5Label('BtnC->play Mic Rec', x=20, y=80, color=0x000, font=FONT_MONT_14, parent=None)


def buttonA_wasPressed():
  # global params
  #global 
  speaker.playTone(220, 1)
  rgb.setColorAll(0xc01a95)
  print('buttonA was Pressed')
  mic.record2file(2, 'flash/res/mic_tmp.wav')
  #power.setVibrationEnable(False)
  wait_ms(200)
  rgb.setColorAll(0x000000)
  pass
btnA.wasPressed(buttonA_wasPressed)


def buttonB_wasPressed():
  # global params
  #global debug_print_EN
  rgb.setColorAll(0xc51a25)
  print('buttonB was Pressed')
  speaker.playWAV('res/Recording.wav', rate='44100', channel=speaker.CHN_LR)
  wait_ms(100)
  rgb.setColorAll(0x000000)
  pass
btnB.wasPressed(buttonB_wasPressed)


def buttonC_wasPressed():
  # global params
  #global PWM_Freq,PWM0
  rgb.setColorAll(0x11aa55)
  print('buttonC was Pressed')
  speaker.playWAV('flash/res/mic_tmp.wav', rate='44100', channel=speaker.CHN_LR)
  wait_ms(100)
  rgb.setColorAll(0x000044)
  pass
btnC.wasPressed(buttonC_wasPressed)


print('while(1) loop running now...')
while(1):
  try:
    rgb.setColorAll(0x111111)
    print('>>PLAY hotel5s.wav...')
    speaker.playWAV('res/hotel5s.wav', rate='44100', channel=speaker.CHN_LR)
  except:
    print('wav play error')
    pass
  rgb.setColorAll(0x000000)
  wait_ms(1000)
  print('>waited 1000ms')
    #speaker.playWAV('4S_HotelCalifornia.wav', rate='44100', dataf=speaker.F16B, channel=speaker.CHN_LR)
    