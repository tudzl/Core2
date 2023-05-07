#PWM APP V0.9 by Zell， 2023.5.7
#PWM output on PORT C, G14, middle GPIO  with Ferq from 1K to 10K
from m5stack import *
from m5stack_ui import *
from uiflow import *
import machine


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xf3eabc)


PWM_Duty = 50
PWM_Freq = 1000
var0 = None



image_BG = M5Img("res/PWM_APP_BG.png", x=0, y=0, parent=None)
label_duty = M5Label('Duty_Cycle:', x=20, y=40, color=0xec990e, font=FONT_MONT_14, parent=None)
switch_ON = M5Switch(x=200, y=48, w=70, h=30, bg_c=0xCCCCCC, color=0x0c9405, parent=None)
label_freq = M5Label('Freq:', x=20, y=20, color=0xf80303, font=FONT_MONT_14, parent=None)
slider_freq = M5Slider(x=210, y=190, w=100, h=16, min=0, max=100, bg_c=0xa0a0a0, color=0xf23c2f, parent=None)
touch_button_D25 = M5Btn(text='25%', x=105, y=100, w=70, h=30, bg_c=0xFFFFFF, text_c=0x5147f5, font=FONT_MONT_14, parent=None)
touch_button_D50 = M5Btn(text='50%', x=105, y=150, w=70, h=30, bg_c=0xFFFFFF, text_c=0x20f170, font=FONT_MONT_14, parent=None)
touch_button_75 = M5Btn(text='75%', x=105, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0xed1212, font=FONT_MONT_14, parent=None)
slider_duty = M5Slider(x=210, y=120, w=100, h=16, min=0, max=100, bg_c=0xa0a0a0, color=0xec990e, parent=None)
label_F_var = M5Label('1000', x=60, y=20, color=0xf233a1, font=FONT_MONT_14, parent=None)
label_D_var = M5Label('50', x=106, y=40, color=0x1f09ec, font=FONT_MONT_14, parent=None)



def slider_freq_changed(var0):
  global PWM_Freq, PWM0
  print(slider_freq.get_value())
  PWM0.pause()
  PWM_Freq = slider_freq.get_value()
  PWM_Freq = PWM_Freq * 100
  if PWM_Freq < 500 :
    PWM_Freq = 500
  if (PWM_Freq > 0) and (PWM_Freq<=10000):  
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
  global PWM_Duty, PWM_Freq, var0, PWM0
  PWM0.pause()
  PWM_Duty = 50
  PWM0.duty(PWM_Duty)
  PWM0.resume()
  pass
touch_button_D50.pressed(touch_button_D50_pressed)

def touch_button_75_pressed():
  global PWM_Duty, PWM_Freq, var0, PWM0
  PWM0.pause()
  PWM_Duty = 75
  PWM0.duty(PWM_Duty)
  PWM0.resume()
  pass
touch_button_75.pressed(touch_button_75_pressed)


image_BG.set_align(ALIGN_CENTER, x=0, y=0, ref=screen.obj)
PWM_Duty = 50
PWM_Freq = 1000
PWM0 = machine.PWM(14, freq=PWM_Freq, duty=PWM_Duty, timer=0)
PWM0.pause()
power.setVibrationEnable(True)
wait(0.2)
power.setVibrationEnable(False)
var0 = 1
while var0:
  #print(PWM_Freq)
  #print(PWM_Duty)
  label_F_var.set_text(str(str(PWM_Freq)))
  label_D_var.set_text(str(str(PWM_Duty)))
  wait(0.02)
