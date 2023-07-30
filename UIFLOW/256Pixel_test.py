from m5stack import *
from m5stack_ui import *
from uiflow import *
import time
import unit


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)
neopixel_0 = unit.get(unit.NEOPIXEL, unit.PORTB, 256)


value = None
Pixel_R_value = 0
Pixel_G_Value = 0
Pixel_B_value = 0
Pixel_value = 0

screen.clean_screen()
screen.set_screen_bg_color(0x00cccc)

slider_R = M5Slider(x=10, y=40, w=300, h=15, min=0, max=100, bg_c=0xa0a0a0, color=0xff0000, parent=None)
label_title = M5Label('256 Pixel LED panel demo', x=5, y=2, color=0xf62929, font=FONT_MONT_22, parent=None)
slider_G = M5Slider(x=10, y=80, w=300, h=15, min=0, max=100, bg_c=0xa0a0a0, color=0x00ff00, parent=None)
slider_B = M5Slider(x=10, y=120, w=300, h=15, min=0, max=100, bg_c=0xa0a0a0, color=0x0303ff, parent=None)
label_Pixel = M5Label('Pixel value:0x000000', x=10, y=180, color=0xf98803, font=FONT_MONT_18, parent=None)
label_Pixel_hex = M5Label('Pixel value:0x000000', x=10, y=210, color=0xf98803, font=FONT_MONT_18, parent=None)


def slider_R_changed(value):
  global Pixel_R_value, Pixel_G_Value, Pixel_B_value
  Pixel_R_value = slider_R.get_value()
  pass
slider_R.changed(slider_R_changed)

def slider_G_changed(value):
  global Pixel_R_value, Pixel_G_Value, Pixel_B_value
  Pixel_G_Value = slider_G.get_value()
  pass
slider_G.changed(slider_G_changed)

def slider_B_changed(value):
  global Pixel_R_value, Pixel_G_Value, Pixel_B_value
  Pixel_B_value = slider_B.get_value()
  pass
slider_B.changed(slider_B_changed)

def buttonC_wasPressed():
  global Pixel_R_value, Pixel_G_Value, Pixel_B_value
  screen.set_screen_brightness(30)
  neopixel_0.setColorFrom(1, 256, 0x33ff33)
  pass
btnC.wasPressed(buttonC_wasPressed)

def buttonB_wasPressed():
  global Pixel_R_value, Pixel_G_Value, Pixel_B_value
  neopixel_0.setColorFrom(1, 256, 0x333333)
  wait_ms(500)
  neopixel_0.setColorFrom(1,256,(Pixel_R_value << 16) | (Pixel_G_Value << 8) | Pixel_B_value)
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonA_wasPressed():
  global Pixel_R_value, Pixel_G_Value, Pixel_B_value
  neopixel_0.setColorFrom(1, 256, 0xff0000)
  pass
btnA.wasPressed(buttonA_wasPressed)



neopixel_0.setColorFrom(1, 24, 0xff0000)
slider_R.set_range(0, 255)
slider_G.set_range(0, 255)
slider_B.set_range(0, 255)
#label_Pixel.set_text_color( (Pixel_R_value << 16) | (Pixel_G_Value << 8) | Pixel_B_value)
while 1:
  Pixel_value = (Pixel_R_value <<16 )+ (Pixel_G_Value <<8) + Pixel_B_value
  #label_Pixel.set_text("Pixel Value:")
  label_Pixel.set_text("Pixel Value:R-"+ str(Pixel_R_value) + " G-" + str(Pixel_G_Value) + " B-" + str(Pixel_B_value) )
  label_Pixel.set_text_color(Pixel_value)
  label_Pixel_hex.set_text("Pixel Value:%06x" % Pixel_value)
  wait_ms(50)
#label_Pixel.set_text('Pixel Value:R-'+ str(Pixel_R_value) + ' G-' + str(Pixel_G_Value) + ' B-' + str(Pixel_B_value) )
#label_Pixel.set_text('Pixel Value:R-')
#neopixel_0.setColorFrom(1,8,(Pixel_R_value << 16) | (Pixel_G_Value << 8) | Pixel_B_value)
neopixel_0.setColorFrom(1,8,(222 << 16) | (33 << 8) | 55)



