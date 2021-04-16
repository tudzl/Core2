#IIC scan debug code by l.zhou
#V2.2 ported to core2 
#V2.1 improve display ,  
#V2.0 added loop time display , LCD brightness display
from m5stack import *
from m5stack_ui import *
from uiflow import *
import  machine
import i2c_bus
import time


#Btn A: DISPLAY BK light control
def buttonA_wasPressed():
  # global params
  global LCD_EN
  #speaker.tone(446, 120, 1)
  LCD_EN = LCD_EN+5
  if LCD_EN > 100:
     LCD_EN = 100
  else:
     LCD_EN = 10 
  wait(0.1)
  pass

#Btn B: DISPLAY BK light control
def buttonB_wasPressed():
  # global params
  global LCD_EN
  #speaker.tone(1046, 120, 1)
  LCD_EN = LCD_EN-1
  if LCD_EN <= 0:
     LCD_EN = 20
  wait(0.1)
  pass

#Btn C: Sleep ON OFF
def buttonC_wasPressed():
  # global params
  global Sleep_EN
  #speaker.tone(646, 120, 1)
  Sleep_EN = 1-Sleep_EN
  wait(0.1)
  pass



screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x111111)
screen.set_screen_brightness(50)

Sleep_EN = 0
LCD_EN = 75
image_BG = M5Img("res/BMW_next.png", x=0, y=0, parent=None)
#lcd.image(lcd.CENTER, lcd.CENTER, 'res/ghost_in_the_shell.jpg')
time.sleep(2) 

#label0 =M5Label('Text', x=54, y=35, color=0x000, font=FONT_MONT_14, parent=None)
#title = M5Title(title="  ESP32 IIC debug v2.1, list iic addresses", x=3 , fgcolor=0xff99aa, bgcolor=0x1F1F1F)
title = M5Label('Core2 IIC debug v2.2, list iic addresses', x=2, y=0, color=0xff99aa, font=FONT_MONT_14, parent=None)
#a = i2c_bus.get(i2c_bus.PORTA)
i2c0 = i2c_bus.easyI2C(i2c_bus.PORTA, 0x68, freq=100000)
label_t = M5Label("Current IIC address list:",x=10, y=20, font=FONT_MONT_14,color=0xF0DFA0)
label1 = M5Label("IIC address list",x=10, y=40, font=FONT_MONT_14,color=0xFFFFAA)

label_info1 = M5Label("iic sacn loop:",x=20, y=200,color=0xDFCF1F,font=FONT_MONT_18)
label_info2 = M5Label("text loop:",x=20, y=220,color=0xDFCF1F,font=FONT_MONT_18)
label_info3 = M5Label("sleep:",x=190, y=225,color=0xDFCF1F,font=FONT_MONT_14)
#label2 = M5TextBox(10, 100, "Text", lcd.FONT_DejaVu24,0xFFAAAA, rotate=0)
image_BG.set_hidden(True)
while True:
    #lcd.setBrightness(0)  
    #start = time.ticks_ms() # get millisecond counter
    if btnC.isPressed():
       buttonC_wasPressed()   
    if btnB.isPressed():
       buttonB_wasPressed()
    if btnA.isPressed():
       buttonA_wasPressed()   

    #lcd.setBrightness(LCD_EN)
    screen.set_screen_brightness(LCD_EN)
    start = time.ticks_ms() # get millisecond counter   
    addrList = i2c0.scan()
    delta_IIC = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    print(addrList)
    l=len(addrList)
    label1.set_text(str(addrList))
    #lcd.print("%02x%%" % ((addrList)), 10, 100, COLOR_GREEN)
    lcd.print("0x", 10, 80, 0xFFAAAA)
    #------display in hex format
    for i in range(0, l, 1):
     lcd.print("%x%%" % ((addrList[i])), 45+i*60, 80, 0xFFAAAA)
    lcd.print( "total addr:     ", 10, 150, 0xFFAAFF)
    lcd.print( str(l), 110, 150, 0xFFAACC)
    #lcd.print( " ".join(hex(ord(n)) for n in addrList),10, 200, COLOR_GREEN)
    #-------------time diff -----------------
    #delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    label_info1.set_text("IIC scan loop: "+str(delta_IIC)+" ms")  #takes about 2ms
    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    label_info2.set_text("text loop: "+str(delta)+" ms")
    start = time.ticks_ms() # get millisecond counter   
    #machine.deepsleep(1000)# put the device to sleep for 1 seconds
    time.sleep_ms(100)
    delta = time.ticks_diff(time.ticks_ms(), start) # compute time difference
    label_info3.set_text("sleep: "+str(delta)+" ms")
    #if Sleep_EN:
       #machine.deepsleep(2000)# put the device to sleep for 1 seconds
    #if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    #label_info2.print('woke from a deep sleep')
    #time.sleep_ms(100)