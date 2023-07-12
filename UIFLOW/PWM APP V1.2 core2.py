#from machine import Pin

#PWM APP V1.2 by Zell， 2023.6.15
#PWM APP V1.1 by Zell， 2023.6.9
#V1.2 added checkbox for frequency x10 range control and brightness control, and show discharge current, BtnABC controls
#V1.1 added Akku voltage display
#PWM output on PORT C, G14, middle GPIO  with Ferq from 500 to 10K or extended to 5K to 100K 
from m5stack import *
from m5stack_ui import *
from uiflow import *
from easyIO import *
import machine
import time
import random

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xf3eabc)
screen.set_screen_brightness(30)
#print(touch.status())
PWM_Duty = 50
PWM_Freq = 1000
PWM_Freq_scale = 1
var0 = None

Screen_ON_OFF = 1
Zeit_Jetzt= None
Timer_interval = 1000 #ms


image_BG = M5Img("res/PWM_APP_BGV2-min.png", x=0, y=0, parent=None)
label_freq = M5Label('Freq:', x=20, y=20, color=0xf80303, font=FONT_MONT_14, parent=None)
label_duty = M5Label('Duty_Cycle:', x=20, y=40, color=0xec990e, font=FONT_MONT_14, parent=None)
switch_ON = M5Switch(x=200, y=42, w=70, h=30, bg_c=0xCCCCCC, color=0x0c9405, parent=None)
label_Akku = M5Label('Akku:', x=20, y=60, color=0x668303,  font=FONT_MONT_14, parent=None)
label_Akku_V = M5Label('', x=60, y=60, color=0x17c208,  font=FONT_MONT_14, parent=None)
label_Akku2 = M5Label('Ak_C:', x=20, y=76, color=0xec5685,  font=FONT_MONT_14, parent=None)
label_Akku_C = M5Label('', x=60, y=76, color=0xD65503,  font=FONT_MONT_14, parent=None)
slider_freq = M5Slider(x=200, y=190, w=100, h=16, min=0, max=100, bg_c=0xa0a0a0, color=0xf23c2f, parent=None)
touch_button_D25 = M5Btn(text='25%', x=105, y=100, w=70, h=30, bg_c=0xFFFFFF, text_c=0x5147f5, font=FONT_MONT_14, parent=None)
touch_button_D50 = M5Btn(text='50%', x=105, y=150, w=70, h=30, bg_c=0xFFFFFF, text_c=0x20f170, font=FONT_MONT_14, parent=None)
touch_button_75 = M5Btn(text='75%', x=105, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0xed1212, font=FONT_MONT_14, parent=None)
slider_duty = M5Slider(x=200, y=120, w=100, h=16, min=0, max=100, bg_c=0xa0a0a0, color=0xec990e, parent=None)
label_F_var = M5Label('1000', x=60, y=20, color=0xf233a1, font=FONT_MONT_14, parent=None)
label_D_var = M5Label('50', x=106, y=40, color=0x1f09ec, font=FONT_MONT_14, parent=None)

SYS_T = M5Label('T:', x=240, y=220, color=0xef600a, font=FONT_MONT_18, parent=None)


Freq_X10range = M5Checkbox(text='F_x10', x=200, y=76, text_c=0x362bd9, check_c=0xeb4234, font=FONT_MONT_14, parent=None)
Freq_X10range.set_checked(False)

def Freq_X10range_checked():
  # global params
  global PWM_Freq_scale,PWM_Freq,PWM0
  PWM_Freq_scale = 10
  PWM0.pause()
  if PWM_Freq < 500 :
    PWM_Freq = 500
  if (PWM_Freq > 0) and (PWM_Freq<=10000*PWM_Freq_scale):  
    PWM0.freq(PWM_Freq)
  PWM0.resume()
  pass
Freq_X10range.checked(Freq_X10range_checked)

def Freq_X10range_unchecked():
  # global params
  global PWM_Freq_scale,PWM_Freq,PWM0
  PWM_Freq_scale = 1
  PWM0.pause()
  if PWM_Freq < 500 :
    PWM_Freq = 500
  if (PWM_Freq > 0) and (PWM_Freq<=10000*PWM_Freq_scale):  
    PWM0.freq(PWM_Freq)
  PWM0.resume()
  pass
Freq_X10range.unchecked(Freq_X10range_unchecked)

def slider_freq_changed(var0):
  global PWM_Freq, PWM0
  print(slider_freq.get_value())
  PWM0.pause()
  PWM_Freq = slider_freq.get_value()
  PWM_Freq = PWM_Freq * 100*PWM_Freq_scale
  if PWM_Freq < 500 :
    PWM_Freq = 500
  if (PWM_Freq > 0) and (PWM_Freq<=10000*PWM_Freq_scale):  
    PWM0.freq(PWM_Freq)
  wait(0.05)
  PWM0.resume()
  pass
slider_freq.changed(slider_freq_changed)

def slider_duty_changed(var0):
  global PWM_Duty,PWM0
  print(slider_duty.get_value())
  PWM0.pause()
  PWM_Duty = slider_duty.get_value()
  PWM0.duty(PWM_Duty)
  PWM0.resume()
  pass
slider_duty.changed(slider_duty_changed)

def switch_ON_off():
  global PWM_Duty, PWM_Freq, var0, PWM0
  PWM0.pause()
  pass
switch_ON.off(switch_ON_off)

def switch_ON_on():
  global PWM_Duty, PWM_Freq, var0, PWM0
  PWM0.pause()
  PWM0 = machine.PWM(14, freq=PWM_Freq, duty=PWM_Duty, timer=0)
  PWM0.resume()
  power.setVibrationEnable(True)
  wait(0.2)
  power.setVibrationEnable(False)
  pass
switch_ON.on(switch_ON_on)

def touch_button_D25_pressed():
  global PWM_Duty, PWM_Freq, var0, PWM0
  PWM0.pause()
  PWM_Duty = 25
  PWM0.duty(PWM_Duty)
  PWM0.resume()
  pass
touch_button_D25.pressed(touch_button_D25_pressed)

def touch_button_D50_pressed():
  global PWM_Duty, PWM_Freq, PWM0
  PWM0.pause()
  PWM_Duty = 50
  PWM0.duty(PWM_Duty)
  PWM0.resume()
  pass
touch_button_D50.pressed(touch_button_D50_pressed)

def touch_button_75_pressed():
  global PWM_Duty, PWM_Freq, PWM0
  PWM0.pause()
  PWM_Duty = 75
  PWM0.duty(PWM_Duty)
  PWM0.resume()
  pass
touch_button_75.pressed(touch_button_75_pressed)


def buttonA_wasPressed():
  # global params
  global PWM_Freq_scale,PWM_Freq,PWM0
  rgb.setColorAll(0x000000)
  rgb.setColorFrom(6, 10, 0xff0000)
  if (1==PWM_Freq_scale ):
    PWM_Freq_scale = 10
    checkbox0.set_checked(True)
  else:
    PWM_Freq_scale = 1
    checkbox0.set_checked(False)
  PWM_Freq= 10000
  PWM0.pause()
  if PWM_Freq < 500 :
    PWM_Freq = 500
  if (PWM_Freq > 0) and (PWM_Freq<=10000*PWM_Freq_scale):  
    PWM0.freq(PWM_Freq)
  PWM0.resume()
  #screen.set_screen_brightness(30)
  pass
btnA.wasPressed(buttonA_wasPressed)


def buttonB_wasPressed():
  # global params
  global Screen_ON_OFF
  rgb.setColorAll(0x000000)
  rgb.setColorFrom(1, 5, 0x000099)
  Screen_ON_OFF = 1-Screen_ON_OFF
  pass
btnB.wasPressed(buttonB_wasPressed)

#Btn3 to set to preset PWM of 25Khz and 30% duty
def buttonC_wasPressed():
  # global params
  global PWM_Duty, PWM_Freq, PWM0
  rgb.setColorAll(0x000000)
  rgb.setColorFrom(6, 10, 0x009900)
  PWM0.pause()
  PWM_Duty = 30
  PWM_Freq = 25000
  PWM0.duty(PWM_Duty)
  PWM0.freq(PWM_Freq)
  PWM0.resume()
  pass
btnC.wasPressed(buttonC_wasPressed)


print("PWM APP V1.0 by Zell for Core2, PWM out on PortC_G14")
print("Date: 7.May.2023")
screen.set_screen_brightness(40)
print(map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100))
Akku_SOC=map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100)
Akku_V=power.getBatVoltage()
Akku_C=0
AXP192_T = 0
Akku_CHG_status = 0
image_BG.set_align(ALIGN_CENTER, x=0, y=0, ref=screen.obj)
PWM_Duty = 50
PWM_Freq = 1000
PWM0 = machine.PWM(14, freq=PWM_Freq, duty=PWM_Duty, timer=0)
PWM0.pause()
power.setVibrationEnable(True)
wait(0.2)
power.setVibrationEnable(False)
var0 = 1
#RGB LED control
R = random.randint(0, 255)
G = random.randint(0, 255)
B = random.randint(0, 255)
Zeit_Jetzt = time.ticks_ms()
while var0:
  #print(PWM_Freq)
  #print(PWM_Duty)
  if (time.ticks_ms() - Zeit_Jetzt )> Timer_interval:
      Zeit_Jetzt = time.ticks_ms()
      print(power.getBatCurrent())
      print(power.getTempInAXP192())
      Akku_V = power.getBatVoltage()
      Akku_C = power.getBatCurrent()
      Akku_SOC=map_value((Akku_V), 3.6, 4.15, 0, 100)
      label_Akku_V.set_text(str(Akku_V)+"V--"+str(Akku_SOC)+"%")
      label_Akku_C.set_text(str(Akku_C)+"mA")
      print("PWM frequency:"+str(PWM_Freq)+"Hz")
      print("PWM Duty_cycle:"+str(PWM_Duty)+"%")
      print("Akku Current:"+str(label_Akku_C))
      AXP192_T=power.getTempInAXP192()
      print("Board Temp.:"+str(AXP192_T))
      SYS_T.set_text("T:"+str(AXP192_T)+"C")
      #print(power.getTempInAXP192())
      if (0== Screen_ON_OFF):
          screen.set_screen_brightness(0)
      else:
          screen.set_screen_brightness(30)
      #if (Akku_CHG_status ):
      #  rgb.setBrightness(40)
      #else:
      #  rgb.setColorAll(0x000000)   
  Akku_CHG_status = power.getChargeState()
  if (Akku_CHG_status):
        if (Akku_SOC>90) :
          R = random.randint(0, 100-Akku_SOC)
          G = random.randint(200, 255)
          B = random.randint(0, Akku_SOC)
        elif (Akku_SOC>50):
          R = random.randint(0, 255-Akku_SOC)
          G = random.randint(100, 200)
          B = random.randint(0, Akku_SOC)
        else:
          R = random.randint(255-Akku_SOC, 255)
          G = random.randint(0, Akku_SOC)
          B = random.randint(0, Akku_SOC)
        #for i in range(0, 256, 10):
          rgb.setColorFrom(6, 10, (R << 16) | (G << 8) | B)
          rgb.setColorFrom(1, 5, (G << 16) | (R << 8) | B)
          rgb.setBrightness(80)
          #rgb.setBrightness(i)
        #for i in range(255, -1, -10):
          #rgb.setColorFrom(6, 10, (R << 16) | (G << 8) | B)
          #rgb.setColorFrom(1, 5, (G << 16) | (R << 8) | B)
          #rgb.setBrightness(30)
          #rgb.setBrightness(i)
      
  label_F_var.set_text(str(str(PWM_Freq)))
  label_D_var.set_text(str(str(PWM_Duty)))
  wait(0.02)