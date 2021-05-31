#MAX30102 Heart rate and SpO sensor demo for core2
#V0.1
#ref https://github.com/m5stack/M5StickC-Plus/blob/master/examples/Hat/HEART_RATE_MAX30102/HEART_RATE_MAX30102.ino
from m5stack import *
from m5stack_ui import *
from uiflow import *
import unit

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
heart0 = unit.get(unit.HEART, unit.PORTA)

label_HR = M5Label('Heart rate:', x=60, y=60, color=0xA22252, font=FONT_MONT_26, parent=None)
label_SPO=  M5Label('SPO:', x=60, y=100, color=0xCEBE00, font=FONT_MONT_26, parent=None)





heart0.setMode(0x03)
heart0.setLedCurrent(0x03, 0x03)
HeartRate=0
SpO =0

while(True):
  HeartRate=heart0.getHeartRate()
  SpO=heart0.getSpO2()
  label_HR.set_text ('Heart rate:'+str(HeartRate) )
  label_SPO.set_text ('SPO:'+str(SpO) )
  print('Heart rate:'+str(HeartRate) )
  print('SPO:'+str(SpO))
  wait_ms(100)