#Pixel IMU game for Core2 by Zell, V3.0  2022.Aug.07
# for core2 with MPU6886
#8.08.2022 created for core2
#Written by ZELL
from m5stack import *
from m5stack_ui import *
from uiflow import *
import unit
import imu
import math
import gc
import esp32
import  machine
import random


win_cnt =0

upside_down = False
Pixel_pos_pre = 28
Pixel_pos_init = 28
Pixel_pos =0
Pixel_target_index = 32
Pixel_row_num= 4
Pixel_col_num= 4
Pixel_brightness =30
Pixel_brightness_m = 15
Pixel_brightness_dk = 5

Color_Blue = 0x0000FF
Color_Red = 0xFF0000
Color_Green = 0x00FF00
Color_Orange = 0xFFA500
Color_Yellow = 0xFFFF00
Color_White = 0xFFFFE0
Color_BK = 0x000000
Color_RedPink = 0xFF1644
Color_DeepPink = 0xFF198C
Color_Random = 0x000000

rgb.setColorAll(0xcc66cc)
power.setVibrationEnable(True)
wait(0.2)
power.setVibrationEnable(False)
rgb.setColorAll(0x99ff99)
neopixe64_panel = unit.get(unit.NEOPIXEL, unit.PORTB, 64)
# offset calibration
def buttonB_wasPressed():
  # global params
  global ACC_X_offset,ACC_Y_offset,ACC_Z_offset
  ACC_X_offset = imu0.acceleration[0]
  ACC_Y_offset = imu0.acceleration[1]
  ACC_Z_offset = imu0.acceleration[2]
  pass


def get_bmm150_status():
    import bmm150
    state = 0
    bmm = bmm150.Bmm150()
    if bmm.available():
        if bmm.readID() == 0x32:
            state = 1
            bmm.set_normal_mode()
            if bmm.readData()[1] == 0:
                time.sleep_ms(200)
                if bmm.readData()[1] == 0:
                    state = 0
    return state
def get_IMU_status():
    #core2 MPU6886
    state = 0
    
    if (imu0.acceleration[0]!=0):
        state = 1
        
    return state 
    
 
    
def tilt_calc(x,y,z):
    unit_g =  x**2 + y**2 + z**2
    unit_g = math.sqrt(unit_g)
    if z<0:
      z= -z
    if (unit_g < 1.25):
       tilt_angle = math.acos(z / unit_g)
    else:
       tilt_angle = math.acos(z / unit_g) #need improve
    tilt_angle = tilt_angle * 57.296 #RAD_TO_DEG
    return tilt_angle
    
    
def init_puzzle(Pixel_pos,Pixel_target_index):
      #page 1
      #global Pixel_target_index
      neopixe64_panel.setColorFrom(1, 64, 0x000000)
      neopixe64_panel.setColor(Pixel_pos, Color_Yellow)
      neopixe64_panel.setColor(Pixel_target_index, Color_Green)
      
      pass


def win_flag():
      #clear
      neopixe64_panel.setColorFrom(1, 64, 0x000000)
      wait(0.05)
      #frame
      neopixe64_panel.setColorFrom(2, 7, Color_Yellow)
      neopixe64_panel.setColor(9, Color_Yellow)
      neopixe64_panel.setColor(16, Color_Yellow)
      neopixe64_panel.setColor(17, Color_Yellow)
      neopixe64_panel.setColor(24, Color_Yellow)
      neopixe64_panel.setColor(25, Color_Yellow)
      neopixe64_panel.setColor(32, Color_Yellow)
      neopixe64_panel.setColor(34, Color_Yellow)
      neopixe64_panel.setColor(39, Color_Yellow)
      neopixe64_panel.setColor(42, Color_Yellow)
      neopixe64_panel.setColor(47, Color_Yellow)
      neopixe64_panel.setColor(51, Color_Yellow)
      neopixe64_panel.setColor(54, Color_Yellow)
      neopixe64_panel.setColorFrom(60, 61, Color_Yellow)
      #!
      neopixe64_panel.setColorFrom(12, 13, Color_Red)
      neopixe64_panel.setColorFrom(20, 21, Color_Red)
      neopixe64_panel.setColorFrom(28, 29, Color_Red)
      neopixe64_panel.setColorFrom(36, 37, Color_Red)
      neopixe64_panel.setColorFrom(52, 53, Color_RedPink)
      wait(0.5)
      neopixe64_panel.setColorFrom(12, 13, 0x000000)
      neopixe64_panel.setColorFrom(20, 21, 0x000000)
      neopixe64_panel.setColorFrom(28, 29, 0x000000)
      neopixe64_panel.setColorFrom(36, 37, 0x000000)
      neopixe64_panel.setColorFrom(52, 53, 0x000000)
      wait(0.5)
      neopixe64_panel.setColorFrom(12, 13, Color_Red)
      neopixe64_panel.setColorFrom(20, 21, Color_Red)
      neopixe64_panel.setColorFrom(28, 29, Color_Red)
      neopixe64_panel.setColorFrom(36, 37, Color_Red)
      neopixe64_panel.setColorFrom(52, 53, Color_RedPink)
      wait(0.25)
      neopixe64_panel.setColorFrom(1, 64, 0x000000)
      pass
    
def win_5():
    global Pixel_brightness_dk,Pixel_brightness
    #clear
    neopixe64_panel.setColorFrom(1, 64, 0x000000)
    wait(0.05)
    neopixe64_panel.setBrightness(Pixel_brightness_dk)
    neopixe64_panel.setColorFrom(1, 64, Color_Green)
    Pixel_brightness = Pixel_brightness_dk
    while(Pixel_brightness<100):
      neopixe64_panel.setBrightness(Pixel_brightness)
      Pixel_brightness = Pixel_brightness+2
      wait(0.05)
      
    Pixel_brightness =30
    wait(0.25)
    neopixe64_panel.setBrightness(Pixel_brightness)
    pass
      
def pixel_row_col_update(Pixel_pos):
    global Pixel_row_num, Pixel_col_num
    Pixel_row_num =int(math.floor((Pixel_pos-1)/8)+1 )
    if Pixel_pos>8:
        Pixel_col_num = int(math.fmod(Pixel_pos, 8) )
        if Pixel_col_num ==0:
           Pixel_col_num =8
    else:
        Pixel_col_num = int(Pixel_pos)
   
    pass   

def pixel_up():
    global Pixel_pos, Pixel_pos_pre
    Pixel_pos = Pixel_pos_pre -8
    

    pass    
  
def pixel_down():
    global Pixel_pos, Pixel_pos_pre
    Pixel_pos = Pixel_pos_pre +8
    

    pass    
def pixel_update(pos, pos_pre):
      #page 1
      #neopixe64_panel.setColorFrom(1, 64, 0x000000)
      neopixe64_panel.setBrightness(Pixel_brightness_m)
      wait(0.15)
      neopixe64_panel.setBrightness(Pixel_brightness_dk)
      neopixe64_panel.setColor(pos_pre, int(Color_Yellow/3))
      neopixe64_panel.setColor(pos, int(Color_Yellow/2))
      wait(0.05)
      neopixe64_panel.setBrightness(Pixel_brightness_m)
      neopixe64_panel.setColor(pos_pre, int(Color_Yellow/2))
      neopixe64_panel.setColor(pos, int(Color_Yellow/3))
      wait(0.05)
      neopixe64_panel.setBrightness(Pixel_brightness)
      neopixe64_panel.setColor(pos_pre, Color_BK)
      neopixe64_panel.setColor(pos, Color_Yellow)
      wait(0.1)
      pass
   
def pixel_draw(pos, color):
      #page 1
      #neopixe64_panel.setColorFrom(1, 64, 0x000000)
      neopixe64_panel.setColor(pos, color)
      wait(0.05)
      pass
ACC_X_offset =0
ACC_Y_offset =0
ACC_Z_offset =0
run_cnt = 0
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0x003300)
#neopixe64_panel = unit.get(unit.NEOPIXEL, unit.PORTB, 64)
neopixe64_panel.setBrightness(Pixel_brightness)
#label0 = M5Label('label0', x=45, y=36, color=0x000, font=FONT_MONT_14, parent=None)

label0 = M5Label( "Pixel puzzle demo v1.01",6, 10,0xFFFFFF, font=FONT_UNICODE_24, parent=None)
     #lcd.set_fg(lcd.WHITE)
label1 = M5Label("IMU status:",20, 40,  0xAFCFFF,font=FONT_MONT_14, parent=None)
#labelT = M5TextBox(20, 140, "Tilt:", lcd.FONT_Default,0xAFCFFF, parent=None)
label_data_T_CPU = M5Label( "T_CPU:",125, 225, 0xAFCFFF,font=FONT_MONT_14, parent=None)
label_pixel = M5Label("Pixel:", 20, 180, 0xAFCF3F,font=FONT_MONT_14, parent=None)
label_cnt = M5Label("CNT: ", 220, 225,0xFFEEBB,font=FONT_MONT_14, parent=None)
#Vb values
label_akku = M5Label("Akku",20, 225, 0xFFFFAA, font=FONT_MONT_14, parent=None)
label_sys = M5Label("sys: ",20, 205, 0xF0CEAA,font=FONT_MONT_14, parent=None)
labelT = M5Label("Tilt:",20,140,  0xAFCFFF, font=FONT_UNICODE_24, parent=None)
#label_ACC = M5TextBox(20, 60, "Acc_X: ", lcd.FONT_Default,0xCFCFCF, parent=None)
Pixel_target_index = random.randint(1, 60)
init_puzzle(Pixel_pos_init,Pixel_target_index)
Pixel_pos_pre = Pixel_pos_init
Pixel_pos = Pixel_pos_pre
imu0 = imu.IMU()

#if get_bmm150_status(): 
if get_IMU_status(): 
   label1.set_text("IMU status: OK")
   wait(0.2)
   ACC_X_offset = imu0.acceleration[0]
   ACC_Y_offset = imu0.acceleration[1]
   ACC_Z_offset = imu0.acceleration[2]
   Tilt_angel=tilt_calc(ACC_X_offset,ACC_Y_offset,ACC_Z_offset)
   if ACC_Z_offset<-0.5:
      upside_down = True
   if (Tilt_angel>5):
        label1.set_text("Offset compensation failed")
   else:
        label1.set_text("Offset compensation OK")
   wait(0.05)
 
#speaker.setVolume(1)
speaker.playTone(220, 1)
wait_ms(100)
#speaker.playTone(220, 1)

while True:
      run_cnt = run_cnt+1
  #try:
      #roll = imu0.ypr[2]
      ACC_X = imu0.acceleration[0]-ACC_X_offset
      ACC_Y = imu0.acceleration[1]-ACC_Y_offset
      ACC_Z = imu0.acceleration[2]
      if ACC_Z<-0.5:
         upside_down = True
      else:
         upside_down = False
      Tilt_angel=tilt_calc(ACC_X,ACC_Y,ACC_Z)
      #ACC_total = (ACC_X**2+ACC_Y**2+ACC_Z**2)**0.5
      lcd.print("Acc_X: "+"%.3f" % (ACC_X)+" ", 20, 60, 0xFFAAAA)
      lcd.print("Acc_Y: "+"%.3f" % (ACC_Y)+" ", 20, 80, 0xFFAAAA)
      lcd.print("Acc_Z: "+"%.3f" % (ACC_Z)+" ", 20, 100, 0xFFAAAA)
      labelT.set_text("Tilt: "+str(Tilt_angel))
      
      pixel_row_col_update(Pixel_pos)
      
      if Tilt_angel>12:
        #speaker.playTone(220, 1)
        if ACC_X> 0.3 :
          
             if upside_down:
                if Pixel_col_num<8 :
                  Pixel_pos= Pixel_pos_pre +1
                else:
                  speaker.playTone(180, 1)
             else:
                if Pixel_col_num>1 :
                  Pixel_pos= Pixel_pos_pre -1
                else:
                  speaker.playTone(220, 1)
             
             
        elif ACC_X <-0.3:
           
              if upside_down:
                if Pixel_col_num>1 :
                   Pixel_pos= Pixel_pos_pre -1
                else:
                   speaker.playTone(180, 1)
              else:
                if Pixel_col_num<8 :
                   Pixel_pos= Pixel_pos_pre +1
                else:
                   speaker.playTone(220, 1)
                   wait_ms(100)

          
        if ACC_Y> 0.3 :
          if Pixel_row_num<8 :
             pixel_down()
          else:
             speaker.playTone(180, 1)
        elif ACC_Y< -0.3 :
            if Pixel_row_num>1 :
               pixel_up()
            else:
               #speaker.playTone(180, 1)
               speaker.playTone(448, 2)
        
        #speaker.playTone(220, 1)
        if Pixel_pos>64:
           Pixel_pos = 64
           speaker.playTone(220, 1)
        if Pixel_pos<1:
           Pixel_pos = 1
           speaker.playTone(220, 1)
           
        pixel_update(Pixel_pos, Pixel_pos_pre)  
        #pixel_draw(Pixel_pos, Pixel_pos_pre)  
        Pixel_pos_pre = Pixel_pos 
      
      
      if Pixel_pos == Pixel_target_index:
             win_cnt = win_cnt +1
             if (win_cnt > 5):
                 win_5()
             label_pixel.set_text("Pixel: "+str(Pixel_pos)+" Col:"+str(Pixel_col_num)+ "Target:"+str(Pixel_target_index))
             speaker.playTone(660, 1)
             wait(0.15)
             win_flag()
             wait(0.15)
             #try:
                #contain bugs!!!
             Pixel_target_index = int (math.fmod(run_cnt,64)+1)
             Pixel_pos = int(random.randint(1, 63)+1)
             label_pixel.set_text("Pixel: " + str(Pixel_pos)+ " Col:" + str(Pixel_col_num) +" Row:" + str(Pixel_row_num) + "Target:"+str(Pixel_target_index))
             #except:
               # label_data_T_CPU.set_text("win funct error")
                #label1.set_text("random.randint error")
                #pass
             label1.set_text("Reset puzzle now!")
             init_puzzle(Pixel_pos,Pixel_target_index)
             Color_Random = int(random.randint(0x1F, 0xffffff))
             pixel_draw(Pixel_target_index, Color_Random)
             wait(0.25)
      #Btn B: reset acc value
      if btnB.isPressed():
         buttonB_wasPressed() 
      gc.collect()
      label_pixel.set_text("Pixel: " + str(Pixel_pos)+ " Col:" + str(Pixel_col_num) +" Row:" + str(Pixel_row_num) + "Target:"+str(Pixel_target_index))
      label_sys.set_text("Free HEAP: "+str(gc.mem_free())+" Bytes" )
      label_data_T_CPU.set_text("")
      label_cnt.set_text("Run: "+str(run_cnt) )
  #except:
      #label_data_T_CPU.set_text("Unknown error occurred")
      #time.sleep(0.1) 
      #pass

  