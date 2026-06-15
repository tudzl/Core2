from m5stack import *
from m5stack_ui import *
from uiflow import *
from m5stack import touch


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x000000)




mode = None
Color = None
size = None
x = None
y = None



label0 = M5Label('Color', x=50, y=220, color=0xFFFFFF, font=FONT_MONT_18, parent=None)
label1 = M5Label('Size:5', x=145, y=220, color=0xFFFFFF, font=FONT_MONT_18, parent=None)
label2 = M5Label('Clear', x=235, y=220, color=0xFFFFFF, font=FONT_MONT_18, parent=None)


# Describe this function...
def DrawPoint():
  global mode, Color, size, x, y
  if Color==0:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0xffffff)
  elif Color==1:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0xff0000)
  elif Color==2:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0x33cc00)
  elif Color==3:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0x3333ff)
  elif Color==4:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0xcc33cc)
  elif Color==5:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0xffff00)
  else:
    lcd.circle(x, y, size, fillcolor=0x000000)
    lcd.circle(x, y, size, color=0xff6600)

# Describe this function...
def ChangeColor():
  global mode, Color, size, x, y
  Color = Color + 1
  if Color == 7:
    Color = 0
  if Color==0:
    label0.set_text_color(0xffffff)
  elif Color==1:
    label0.set_text_color(0xff0000)
  elif Color==2:
    label0.set_text_color(0x33cc00)
  elif Color==3:
    label0.set_text_color(0x3333ff)
  elif Color==4:
    label0.set_text_color(0xcc33cc)
  elif Color==5:
    label0.set_text_color(0xffff00)
  else:
    label0.set_text_color(0xff6600)

# Describe this function...
def DrawPoints():
  global mode, Color, size, x, y
  if touch.status():
    x = touch.read()[0]
    y = touch.read()[1]
    if Limit():
      DrawPoint()

# Describe this function...
def Clear():
  global mode, Color, size, x, y
  screen.set_screen_bg_color(0x000000)
  label0.set_hidden(False)
  label1.set_hidden(False)
  label2.set_hidden(False)

# Describe this function...
def ChangeSize():
  global mode, Color, size, x, y
  size = size + 5
  if size == 20:
    size = 5
  label1.set_text(str((str('Size:') + str(size))))

# Describe this function...
def Limit():
  global mode, Color, size, x, y
  if y >= 220 - size:
    return False
  return True


def buttonA_wasPressed():
  global mode, Color, size, x, y
  mode = 1
  pass
btnA.wasPressed(buttonA_wasPressed)

def buttonB_wasPressed():
  global mode, Color, size, x, y
  mode = 2
  pass
btnB.wasPressed(buttonB_wasPressed)

def buttonC_wasPressed():
  global mode, Color, size, x, y
  mode = 3
  pass
btnC.wasPressed(buttonC_wasPressed)


Clear()
lv.obj.set_click(lv.scr_act(), False)
size = 5
Color = 0
mode = 0
while True:
  if mode == 1:
    ChangeColor()
  elif mode == 2:
    ChangeSize()
  elif mode == 3:
    Clear()
  mode = 0
  DrawPoints()
  wait_ms(2)
