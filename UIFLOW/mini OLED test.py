from m5stack import *
from m5ui import *
from uiflow import *
import time
import unit


setScreenColor(0x272727)
mini_oled_0 = unit.get(unit.MINI_OLED, unit.PORTA)




i = None
x = None



label0 = M5TextBox(21, 45, "screen of Unit Mini OLED will draw a text", lcd.FONT_Default, 0xfa7205, rotate=0)
title0 = M5Title(title="MINI-OLED-DEMO", x=100, fgcolor=0xFFFFFF, bgcolor=0x0000FF)
label1 = M5TextBox(35, 87, "Unit MINI OLED Example", lcd.FONT_DejaVu18, 0xff0000, rotate=0)
label2 = M5TextBox(21, 224, "TEXT-SCROLL", lcd.FONT_Default, 0xff0000, rotate=0)
label3 = M5TextBox(107, 190, "RANDOM-BOX", lcd.FONT_Default, 0xff0000, rotate=0)
label4 = M5TextBox(182, 224, "RANDOM-SQUARE", lcd.FONT_Default, 0xff0000, rotate=0)

import random


# Describe this function...
def random_square():
  global i, x
  mini_oled_0.fill(0)
  for count in range(40):
    i = random.randint(5, 67)
    x = random.randint(5, 35)
    mini_oled_0.fill_rect(i, x, 8, 8, 1)
    mini_oled_0.show()
    wait_ms(100)
  mini_oled_0.fill(0)
  mini_oled_0.show()

# Describe this function...
def text_scroll():
  global i, x
  mini_oled_0.fill(0)
  mini_oled_0.text('WELCOME', 8, 4, 1)
  mini_oled_0.text('M5', 30, 18, 1)
  mini_oled_0.text('MINI OLED', 0, 32, 1)
  mini_oled_0.show()
  for count2 in range(5):
    mini_oled_0.invert(1)
    mini_oled_0.show()
    wait_ms(250)
    mini_oled_0.invert(0)
    mini_oled_0.show()
    wait_ms(250)
  for i in range(11):
    mini_oled_0.scroll(i, i)
    mini_oled_0.show()
    wait_ms(250)

# Describe this function...
def random_box():
  global i, x
  mini_oled_0.fill(0)
  for i in range(0, 36, 3):
    mini_oled_0.rect(i, i, 10, 10, 1)
    mini_oled_0.rect((40 + i), i, 10, 10, 1)
    mini_oled_0.show()
    wait_ms(100)
  mini_oled_0.fill(0)
  mini_oled_0.show()


def buttonA_wasPressed():
  global i, x
  text_scroll()
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonC_wasPressed():
  global i, x
  random_square()
  pass
btnC.wasPressed(buttonC_wasPressed)

def buttonB_wasPressed():
  global i, x
  random_box()
  pass
btnB.wasPressed(buttonB_wasPressed)


text_scroll()
wait_ms(200)
random_box()
wait_ms(200)
random_square()
