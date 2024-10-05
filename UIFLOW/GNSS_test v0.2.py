from m5stack import *
from m5stack_ui import *
from uiflow import *
from machine import WDT
import time
import unit
remoteInit()

screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
gps_0 = unit.get(unit.GPS, unit.PORTC)


joystick_x_value = None
joystick_y_value = None
slider_value = None
CO2_PPM = None
Joy_X = None
Joy_y = None
sys_tck = None



CO2 = M5Label('label_CO2', x=20, y=58, color=0x4853e4, font=FONT_MONT_18, parent=None)
Jo_X = M5Label('Joy_X', x=16, y=100, color=0x000, font=FONT_MONT_14, parent=None)
Joy_Y = M5Label('Joy_Y', x=16, y=140, color=0x000, font=FONT_MONT_14, parent=None)
label_title = M5Label('GNSS_view demo v0.1', x=10, y=0, color=0x1ff379, font=FONT_MONT_14, parent=None)
lcd.qrcode('http://flow-remote.m5stack.com/?remote=1040050301446389760', 72, 32, 176)
wait_ms(1000)


def joystick_1_callback(joystick_x_value, joystick_y_value):
  global CO2_PPM, slider_value, Joy_X, Joy_y, sys_tck, wdt, PWM0, gps_0 
  print(joystick_y_value)
  print(joystick_x_value)
  Joy_X = joystick_x_value
  Joy_y = joystick_y_value

def slider_CO2_SIM_callback(slider_value):
  global CO2_PPM, joystick_y_value, joystick_x_value, Joy_X, Joy_y, sys_tck, wdt, PWM0, gps_0 
  print(slider_value)
  CO2_PPM = slider_value

def gauge_AirQ_callback():
  global CO2_PPM, joystick_y_value, slider_value, joystick_x_value, Joy_X, Joy_y, sys_tck, wdt, PWM0, gps_0 
  return CO2_PPM
screen.set_screen_bg_color(0x000000)
gps_0.uart_port_id(1)
gps_0.set_time_zone(8)
CO2_PPM = 99
Joy_X = 0
Joy_y = 0
wdt = WDT(timeout=2000)
lcd.print('GNSS Demo V0.1', 16, 0, 0xffccff, rotate=0)
while True:
  wdt.feed()
  sys_tck = time.ticks_ms()
  print(gps_0.gps_time)
  print(slider_value)
  print(joystick_x_value)
  print(joystick_y_value)
  CO2.set_text(str(CO2_PPM))
  Jo_X.set_text(str(Joy_X))
  Joy_Y.set_text(str(Joy_y))
  if CO2_PPM > 500:
    rgb.setColorAll(0xff0000)
  else:
    rgb.setColorAll(0x33ff33)
  wait_ms(2)
