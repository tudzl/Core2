#ID8 Speed Coupit demo V4.1 based on loop scan I/O status plus filtering
#INA260_Core2 demo V2.6B  0162C86C
#hall speed detect
#port B G26,G36: pin26 not working as digitalRead,
from m5stack import *
from m5stack_ui import *
from uiflow import *
from MediaTrans.AudioPlay import AudioPlay

from easyIO import *
import i2c_bus
import time
import gc

gc.collect()
os.statvfs("")
Sensor_pin = 36 #PortB last pin
PWM_pin = 26
PWM_Freq = 4
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)

try:
  wifiCfg.autoConnect(lcdShow=False)
except:
  pass

PWM0 = machine.PWM(26, freq=PWM_Freq, duty=98, timer=0)
PWM_EN = 0
PWM0.pause()
#PWM0.resume()
image_BG = M5Img("res/BMW_coupit BG3.png", x=0, y=0, parent=None)
Title = M5Label('ID8 Speed Coupit demo V4.0B', x=20, y=5, color=0x2517de, font=FONT_MONT_14, parent=None)
#Title.set_hidden(True)
#label_vol = M5Label('Vbus_In:', x=20, y=40, color=0xEE9E00, font=FONT_MONT_18, parent=None)
#label_Cur = M5Label('Current:', x=20, y=60, color=0xEE1E00, font=FONT_MONT_18, parent=None)
#label_Pow = M5Label('Power  :', x=20, y=80, color=0xCCCCCC, font=FONT_MONT_18, parent=None)

label_Hall = M5Label('Hall:', x=160, y=20, color=0xEEAE00, font=FONT_MONT_14, parent=None)
label_Shift = M5Label('S3', x=100, y=120, color=0x2255EF, font=FONT_MONT_28, parent=None)
#label_Hall2 = M5Label('Hall2:', x=220, y=100, color=0xEE1E00, font=FONT_MONT_16, parent=None)
label_speed = M5Label('speed:', x=200, y=80, color=0x4EEE10, font=FONT_MONT_18, parent=None)
label_speed_num = M5Label('22', x=150, y=100, color=0xCEEEB0, font=FONT_MONT_40, parent=None)
label_speed_kmh = M5Label('km/h', x=260, y=110, color=0xEEAE00, font=FONT_MONT_20, parent=None)
label_T_cycle = M5Label('CycleT:', x=160, y=160, color=0xA22252, font=FONT_MONT_16, parent=None)
label_PWM_FREQ=  M5Label('PWM:', x=160, y=180, color=0xCEBE00, font=FONT_MONT_16, parent=None)
label_sysinfo = M5Label('Sys_cnt', x=130, y=220, color=0xA0C0A0, font=FONT_MONT_12, parent=None)
label_Akkuinfo = M5Label('Akku', x=280, y=5, color=0x504020, font=FONT_MONT_12, parent=None)
label_RTCinfo = M5Label('RTC', x=20, y=220, color=0xB0B0A0, font=FONT_MONT_18, parent=None)
line_speed = M5Line(x1=97, y1=220, x2=118, y2=220, color=0x32EF11, width=5, parent=None) #inner line green, length=21  0x007F46
line_speed2 = M5Line(x1=95, y1=220, x2=120, y2=220, color=0xf63f3f, width=7, parent=None)#frame line pink, length=25
#line_speed3 = M5Line(x1=17, y1=100, x2=45, y2=100, color=0xf61f1f, width=5, parent=None)
#line_speed4 = M5Line(x1=15, y1=100, x2=47, y2=100, color=0xF0f0f0, width=7, parent=None)
speed_line_x_b = 95
speed_line_y_b = 220
speed_line_x_B =13
speed_line_y_B = 100
#line_speed.set_opacity(95)
line_speed2.set_opacity(70)
#line_speed4.set_opacity(70)
#line_speed.set_points(speed_line_x+2, speed_line_y, speed_line_x+21, speed_line_y)
#line_speed2.set_points(speed_line_x, speed_line_y, speed_line_x+25, speed_line_y)
#line_speed.set_hidden(True)

touch_button_HighPrecision = M5Btn(text='PWM', x=225, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)
#touch_button_HighPrecision = M5Btn(text='HiRes', x=225, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)
#touch_button_INA = M5Btn(text='INA', x=25, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)
touch_button_HighPrecision.set_bg_color(0x220000)

def touch_button_HighPrecision_pressed():
  # global params
  global PWM_EN
  #print('HiRes button was Touched')
  PWM_EN = 1 - PWM_EN
  if(PWM_EN):
    touch_button_HighPrecision.set_bg_color(0xEEEEEE)
    #touch_button_PWM = M5Btn(text='PWM', x=225, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)
  else:  
    touch_button_HighPrecision.set_bg_color(0x220000)
    #touch_button_PWM = M5Btn(text='PWM', x=225, y=200, w=70, h=30, bg_c=0x220000, text_c=0x85d612, font=FONT_MONT_14, parent=None)

  rgb.setColorFrom(6 , 10 ,0x993399)
  rgb.setColorFrom(1 , 5 ,0x66ffff)
  pass
touch_button_HighPrecision.pressed(touch_button_HighPrecision_pressed)

'''
def touch_button_INA_pressed():
  # global params'
  global   INA_OK
  power.setVibrationIntensity(10)
  power.setVibrationEnable(True)
  print('INA button was Touched')
  INA_OK = 1- INA_OK
  rgb.setColorFrom(6 , 10 ,0x993399)
  rgb.setColorFrom(1 , 5 ,0x66ffff)
  wait_ms(200)
  power.setVibrationEnable(False)
  pass
touch_button_INA.pressed(touch_button_INA_pressed)
'''
IIC_PORTA = (32,33) # I2C  base 485 PCB for 16BV demo
PMOS_gate_pin = 27
INA260_ADDRESS	 = 0x40  #1000000 @ A0,A1=GND
LM75_ADDRESS	 = 0x48
LM75_ADDRESS2	 = 0x49
Wheel_length = 1510 #in cm, 20*1.50 　　1510 mm 　　EA062、FA073
#--------INA260 Reg address---------
INA260_REG_CONFIG = const(0x00)  # CONFIGURATION REGISTER (R/W)
INA260_REG_CURRENT = const(0x01)  # SHUNT VOLTAGE REGISTER (R)
INA260_REG_BUSVOLTAGE = const(0x02)  # BUS VOLTAGE REGISTER (R)
INA260_REG_POWER = const(0x03)  # POWER REGISTER (R)
INA260_REG_MASK_ENABLE = const(0x06)  # MASK ENABLE REGISTER (R/W)
INA260_REG_ALERT_LIMIT = const(0x07)  # ALERT LIMIT REGISTER (R/W)
INA260_REG_MFG_UID = const(0xFE)  # MANUFACTURER UNIQUE ID REGISTER (R)
INA260_REG_DIE_UID = const(0xFF)  # DIE UNIQUE ID REGISTER (R)
TIME_140_us = const(0x0)
TIME_204_us = const(0x1)
TIME_332_us = const(0x2)
TIME_558_us = const(0x3)
TIME_1_1_ms = const(0x4)
TIME_2_116_ms = const(0x5)
TIME_4_156_ms = const(0x6)
TIME_8_244_ms = const(0x7)

COUNT_1 = const(0x0)
COUNT_4 = const(0x1)
COUNT_16 = const(0x2)
COUNT_64 = const(0x3)
COUNT_128 = const(0x4)
COUNT_256 = const(0x5)
COUNT_512 = const(0x6)
COUNT_1024 = const(0x7)

INA260_MODE_SHUTDOWN = const(0x0)
INA260_MODE_TRIGGERED = const(0x3)
INA260_MODE_CONTINUOUS = const(0x7)




LM75_TEMP_REGISTER 	 = 0
LM75_CONF_REGISTER 	 = 1
LM75_THYST_REGISTER 	 = 2
LM75_TOS_REGISTER 	 = 3

LM75_CONF_SHUTDOWN  	 = 0
LM75_CONF_OS_COMP_INT 	 = 1
LM75_CONF_OS_POL 	 = 2
LM75_CONF_OS_F_QUE 	 = 3

#global para vars
debug_print_EN =0
Current_alert = 1900 # in mA
Current_alert_stop = 2500 # in mA
Current_alert_step = 100 # increase step, in mA

def filter_T_cycle(T_pre,T_cur):
    T_Low_lim = T_pre*2-1
    T_Hi_lim = T_pre*2+8
    T_Low3_lim = T_pre*3-1
    T_Hi3_lim = T_pre*3+13
    if((T_cur<T_Hi_lim)&(T_cur>T_Low_lim) ): #doubled time
        return T_pre
    elif((T_cur<T_Hi3_lim)&(T_cur>T_Low3_lim) ): #triple time  
        return T_pre
    else:
        return T_cur



def buttonA_wasPressed():
  # global params
  global debug_print_EN,PWM_Freq,PWM0
  rgb.setColorAll(0xccaa55)
  print('buttonA was Pressed')
  PWM_Freq =PWM_Freq+1
  PWM0 = machine.PWM(26, freq=PWM_Freq, duty=97, timer=0)
  #power.setVibrationEnable(False)
  wait_ms(300)
  rgb.setColorAll(0x000044)
  pass
btnA.wasPressed(buttonA_wasPressed)


#debug en
def buttonB_wasPressed():
  # global params
  global debug_print_EN
  rgb.setColorAll(0xc51a25)
  print('buttonB was Pressed')
  debug_print_EN = 1- debug_print_EN
  #power.setVibrationIntensity(30)
  #power.setVibrationEnable(True)
  if(debug_print_EN):
    print('Serial print enabled!' )
  else:  
    print('Serial print disabled!' )
  speaker.playTone(220, 3)
  #speaker.playWAV('4S_HotelCalifornia.wav/4S_HotelCalifornia.wav')
  wait_ms(500)
  rgb.setColorAll(0x000044)
  pass
btnB.wasPressed(buttonB_wasPressed)



def buttonC_wasPressed():
  # global params
  global PWM_Freq,PWM0
  rgb.setColorAll(0xc01a95)
  print('buttonC was Pressed')
  #power.setVibrationIntensity(30)
  #power.setVibrationEnable(True)
  
  PWM_Freq =PWM_Freq-1#only integer is supported?
  if (PWM_Freq<7):
      PWM0 = machine.PWM(26, freq=PWM_Freq, duty=99, timer=0)
  else:
      PWM0 = machine.PWM(26, freq=PWM_Freq, duty=98, timer=0)
  #INA_OK = 1 -INA_OK
  #print('INA260 status: '+str(INA_OK) )
  wait_ms(300)
  #power.setVibrationEnable(False)
  rgb.setColorAll(0x000044)
  pass
btnC.wasPressed(buttonC_wasPressed)


print('Core2 bycycle Hall speed coupit V4.1')
print('Author: Zell, 22.June.2021')

tmp_str = None
Vbus= 0
Current = 0
Power_INA = 0
T_LM75A = 0
T_LM75B = 0
TF1 = 0
TF2 = 0
SensorA_scan_cnt = 0
SensorB_scan_cnt = 0
INA_OK = False
LM75A1_OK = False
LM75A2_OK = False
Hall_status = None
Hall_status2 = None
sys_cnt = 0
RTC_cnt = 0
T_interval = 250
T_cycle = 50
T_cycle_pre =50
WheelSPD = 0
WheelSPD_KMH = 0
run_dist = 0
#i2c0 = i2c_bus.easyI2C((26, 32), LM75_ADDRESS, freq=100000)
i2c0 = i2c_bus.easyI2C(IIC_PORTA, LM75_ADDRESS2, freq=400000)
Scan_EN = True
Scan_cnt = 0
OUT_EN = True
gun_stop_cnt = 0
while (Scan_EN):
    try :
      #coupit test
      for i in range(0, 48, 1):
        WheelSPD_KMH = i
        if (WheelSPD_KMH>24):
          speed_line_x = speed_line_x_B+ int((WheelSPD_KMH-24)*3)
          speed_line_y = speed_line_y_B- int((WheelSPD_KMH-24)*3)
          line_speed.set_points(speed_line_x+2, speed_line_y, speed_line_x+23, speed_line_y)
          line_speed2.set_points(speed_line_x, speed_line_y, speed_line_x+27, speed_line_y) 
        else:
          speed_line_x = speed_line_x_b- int(WheelSPD_KMH*10/3)
          speed_line_y = speed_line_y_b- int(WheelSPD_KMH*5)
          line_speed.set_points(speed_line_x+2, speed_line_y, speed_line_x+21, speed_line_y)
          line_speed2.set_points(speed_line_x, speed_line_y, speed_line_x+25, speed_line_y) 
        tmp_str ='%2.2F' % WheelSPD_KMH
        label_speed_num.set_text (tmp_str)
        if (WheelSPD_KMH<1):
         label_Shift.set_text ('S3-')
         rgb.setColorAll(0x000000)
         rgb.setBrightness(5)
         WheelSPD = 0
        elif (WheelSPD_KMH<6):
         label_Shift.set_text ('S3')
         rgb.setBrightness(10)
         rgb.setColor(2, 0x00cccc)
         rgb.setColor(9, 0x00cccc)
         rgb.setColor(3, 0x000000)
         rgb.setColor(8, 0x000000)
         rgb.setColor(4, 0x000000)
         rgb.setColor(7, 0x000000)
         rgb.setColor(5, 0x000000)
         rgb.setColor(6, 0x000000)
        elif (WheelSPD_KMH<12):
         label_Shift.set_text ('S3+')
         rgb.setBrightness(15)
         rgb.setColor(3, 0x33dd33)
         rgb.setColor(8, 0x33dd33)
         rgb.setColor(4, 0x000000)
         rgb.setColor(7, 0x000000)
         rgb.setColor(5, 0x000000)
         rgb.setColor(6, 0x000000)
        elif (WheelSPD_KMH<18):
         label_Shift.set_text ('S4+')
         label_Shift.set_text_color(0xe05000)
         rgb.setBrightness(20)
         rgb.setColor(4, 0xaa5600)
         rgb.setColor(7, 0xaa5600)
         rgb.setColor(5, 0x000000)
         rgb.setColor(6, 0x000000)
        elif (WheelSPD_KMH<24):
         label_Shift.set_text ('S5+')
         label_Shift.set_text_color(0xee3000)
         rgb.setBrightness(25)
         rgb.setColor(4, 0xdd5600)
         rgb.setColor(7, 0xdd5600)
         rgb.setColor(5, 0x551200)
         rgb.setColor(6, 0x551200)
        else:
         label_Shift.set_text ('S6+')
         label_Shift.set_text_color(0xff0000)
         rgb.setBrightness(30)
         rgb.setColor(5, 0xee1200)
         rgb.setColor(6, 0xee1200)
        wait_ms(50)
      
      
      addrList = i2c0.scan()
      Dev_cnt=len(addrList)
      print('IIC scan results:')
      #print(addrList)
      #print("0x")
      for i in range(0, Dev_cnt, 1):
        print('0x'+'%2x%%'%((addrList[i])))
        if (INA260_ADDRESS == addrList[i]):
           rgb.setColorAll(0xEEEEBB)
           INA_OK = True
           wait_ms(100)

      print('Total device:'+str(Dev_cnt))
      label_sysinfo.set_text ('Total device:'+str(Dev_cnt))
      if (Dev_cnt>0):
        rgb.setColorAll(0x03ff13)
        Scan_EN = False
      else:
        Scan_cnt = Scan_cnt+1
        rgb.setColorAll(0x101000)
        Scan_EN = True
      #lcd.print("%02x%%" % ((addrList)), 10, 100, COLOR_GREEN)
      #lcd.print("0x", 10, 80, 0xFFAAAA)
      #------display in hex format
      if(Scan_cnt>2):
        Scan_EN  = False
      wait_ms(500)
      rgb.setColorAll(0x000000)
      pass
    except:
      print('IIC scan error')
      rgb.setColorAll(0xff1133)
      wait_ms(100)
      rgb.setColorAll(0x000000)
      continue
print('#>:IIC scan finished, main control starts running')
#config INA260_reg
if(INA_OK):
           i2c0 = i2c_bus.easyI2C(IIC_PORTA, INA260_ADDRESS, freq=100000)
           print('----INA260-config----')
           print('----Conversion time: 1.1 ms def----')
           print('----Averaging mode: 4')
           config_word = i2c0.read_reg(INA260_REG_CONFIG, 2)
           config_def = int.from_bytes(config_word, False) 
           print('----Default config value: '+bin(config_def))
           tmp_config=INA260_MODE_CONTINUOUS+(TIME_2_116_ms<<3)+(TIME_1_1_ms<<6)+(COUNT_4<<9)+(6<<12)
           config_bytes = bytearray(2)
           config_bytes = int.to_bytes(tmp_config,2,"big")
           print('----config_bytes   value: '+bin(int.from_bytes(config_bytes, False) ))
           i2c0.write_u16(INA260_REG_CONFIG, tmp_config, byteorder="big")
           #i2c0.write_u16(INA260_REG_CONFIG, tmp_config, byteorder="big")
           #tmp_config = config_def+ (COUNT_4<<9)assssssss
           #print('----New config reg value: '+bin(tmp_config))
           wait_ms(10)
           config_word = i2c0.read_reg(INA260_REG_CONFIG, 2)
           config_val = int.from_bytes(config_word, False) 
           print('---readback config value: '+bin(config_def))
           label_sysinfo.set_text ('-INA260-config-done!-')
           """
           ----Default config value: 0b110001011101111
           ----config_bytes   value: 0b110001101101111
           ---readback config value: 0b110001011101111
           """
           
RTC_EN = 0
try:
  rtc.settime('ntp', host='cn.pool.ntp.org', tzone=8)
  print("Current Time:"+str(rtc.datetime())) #(2021, 6, 4, 4, 11, 25, 29, 0)
  RTC_EN = 1
except:
  print("NTP time not available, check wifi!")      
if(RTC_EN):
  label_RTCinfo.set_text(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
  
T_start = time.ticks_ms() # get millisecond counter  
T_Hall = T_start
T_cycle_tmp = T_Hall
T_loop_delta = 0
Wheel_run_cnt = 0
Wheel_pos = 0 #1 @ sensor in position, 0@ other positions (359 degree?)
Title.set_hidden(True)
while 1:
    
    T_loop = time.ticks_ms()

    #-------------Port B pin 26 digital read hall Sensor
    Hall_status = digitalRead(Sensor_pin)
    if (Hall_status==0):#active input! 
        T_cycle_interval = time.ticks_diff(time.ticks_ms(), T_Hall) # compute time 
        T_Hall = time.ticks_ms()
        """### old api
        if (T_cycle_tmp< 10): #too fast, not valid sensor reading
          #T_Hall = time.ticks_ms() # get millisecond counter 
          T_cycle=T_cycle
          #T_cycle=T_cycle+T_loop_delta #last cycle time, to decrease speed gradually  #need improve?
        else:
          T_cycle = T_cycle_tmp
          WheelSPD = Wheel_length/T_cycle #m/s
          T_Hall = time.ticks_ms() # get millisecond counter 
          #T_cycle_tmp = T_Hall
          #wait_ms(10)
        """###  
        #Wheel_pos=Wheel_pos-digitalRead(Sensor_pin)# test only
        if (Wheel_pos ==1):
          #T_Hall = time.ticks_ms() # get millisecond counter
          T_cycle = T_cycle_interval
          #wait_ms(1)
          Wheel_pos = 0 
        #elif(Wheel_run_cnt>2):
          #T_cycle = T_cycle+T_loop_delta
          #WheelSPD = Wheel_length/T_cycle #m/s
          #T_Hall = time.ticks_ms() # get millisecond counter
        Wheel_run_cnt = 0   
    #NO input sense      
    else: #decrease speed gradually?
        Wheel_pos=1



    
    sys_cnt = sys_cnt + 1
   
    T_delta = time.ticks_diff(time.ticks_ms(), T_start) # compute time difference
    if(T_delta>=T_interval):
       rgb.setColor(1, 0x000099)
       rgb.setColor(10, 0x000099)
       
       if (T_cycle>65):
          try:  
            T_cycle= filter_T_cycle(T_cycle_pre,T_cycle)
            WheelSPD = Wheel_length/T_cycle #m/s
            T_cycle_pre=T_cycle
            #Wheel_run_cnt = 0# test only
          except:
            pass#print("WheelSPD calc error!"+str(T_cycle2)) 
       
       #WheelSPD = Wheel_length/T_cycle #m/s
       Wheel_run_cnt = Wheel_run_cnt+1
       if (Wheel_run_cnt >4):
          WheelSPD = Wheel_length/(T_cycle+T_delta*Wheel_run_cnt) #m/s
          rgb.setColorAll(0x000000)
       if (Wheel_run_cnt >7):  
          WheelSPD = 0
       WheelSPD_KMH = WheelSPD*3.6 #km/h 
       run_dist += WheelSPD*T_delta/1000.0 #in M
       if (WheelSPD_KMH<1):
         label_Shift.set_text ('S3-')
         label_Shift.set_text_color(0x2255EF)
         rgb.setColorAll(0x000000)
         rgb.setBrightness(5)
         WheelSPD = 0
       elif (WheelSPD_KMH<6):
         label_Shift.set_text ('S3')
         rgb.setBrightness(10)
         rgb.setColor(2, 0x00cccc)
         rgb.setColor(9, 0x00cccc)
         rgb.setColor(3, 0x000000)
         rgb.setColor(8, 0x000000)
         rgb.setColor(4, 0x000000)
         rgb.setColor(7, 0x000000)
         rgb.setColor(5, 0x000000)
         rgb.setColor(6, 0x000000)
       elif (WheelSPD_KMH<12):
         label_Shift.set_text_color(0x22EF11)
         label_Shift.set_text ('S3+')
         rgb.setBrightness(15)
         rgb.setColor(3, 0x33dd33)
         rgb.setColor(8, 0x33dd33)
         rgb.setColor(4, 0x000000)
         rgb.setColor(7, 0x000000)
         rgb.setColor(5, 0x000000)
         rgb.setColor(6, 0x000000)
       elif (WheelSPD_KMH<18):
         label_Shift.set_text_color(0xe05000)
         label_Shift.set_text ('S4+')
         rgb.setBrightness(20)
         rgb.setColor(4, 0xaa0600)
         rgb.setColor(7, 0xaa5600)
         rgb.setColor(5, 0x000000)
         rgb.setColor(6, 0x000000)
       elif (WheelSPD_KMH<24):
         label_Shift.set_text_color(0xee3000)
         label_Shift.set_text ('S5+')
         rgb.setBrightness(25)
         rgb.setColor(4, 0xdd5600)
         rgb.setColor(7, 0xdd5600)
         rgb.setColor(5, 0x551200)
         rgb.setColor(6, 0x551200)
       else:
         label_Shift.set_text_color(0xff1000)
         label_Shift.set_text ('S6+')
         rgb.setBrightness(30)
         rgb.setColor(5, 0xee1200)
         rgb.setColor(6, 0xee1200)
       if (WheelSPD_KMH>80):
         WheelSPD_KMH = 0
         rgb.setColorAll(0x000000)
       
       speed_line_x = speed_line_x_b- int(WheelSPD_KMH*10/3)
       speed_line_y = speed_line_y_b- int(WheelSPD_KMH*5)
       if (WheelSPD_KMH>24):
          speed_line_x = speed_line_x_B+ int((WheelSPD_KMH-24)*3)
          speed_line_y = speed_line_y_B- int((WheelSPD_KMH-24)*3)
          line_speed.set_points(speed_line_x+2, speed_line_y, speed_line_x+23, speed_line_y)
          line_speed2.set_points(speed_line_x, speed_line_y, speed_line_x+27, speed_line_y) 
       else:
          speed_line_x = speed_line_x_b- int(WheelSPD_KMH*10/3)
          speed_line_y = speed_line_y_b- int(WheelSPD_KMH*5)
          line_speed.set_points(speed_line_x+2, speed_line_y, speed_line_x+21, speed_line_y)
          line_speed2.set_points(speed_line_x, speed_line_y, speed_line_x+25, speed_line_y) 
       if (PWM_EN):
          PWM0.resume()
          label_PWM_FREQ.set_text ('PWM:'+str(PWM_Freq)+'Hz')
       else:
          PWM0.pause()
          label_PWM_FREQ.set_text ('PWM: NA.')
          
       tmp_str ='%4.1F' % run_dist
       label_Hall.set_text ('Dist.:'+str(tmp_str)+"M")
       #label_Hall.set_text ('Hall:'+str(Hall_status))
       tmp_str ='%2.2F' % WheelSPD_KMH
       label_speed_num.set_text (tmp_str)
       #label_speed.set_text ('speed:'+str(WheelSPD)+'km/h')
       label_T_cycle.set_text ('CycleT:'+str(T_cycle)+'ms')
       #print('Temperature: %i.%02i °C, RH: %i.%02i %%' % (t_int, t_dec, h_int, h_dec))
       
       tmp_str = '%1.2F' % power.getBatVoltage()
       label_Akkuinfo.set_text(tmp_str+' V')
       #label_Akkuinfo.set_text(str(power.getBatVoltage())+' V')
       tmp_str = '%5.0F' % (1000*sys_cnt/T_delta)
       label_sysinfo.set_text('Sys fps:'+str(tmp_str))
       if(debug_print_EN):
          print('Speed:'+str(WheelSPD_KMH)+'Km/h')
          print('T_delta:'+str(T_delta))
          print('Sys cnt:'+str(sys_cnt))
          print('Sys fps:'+str(1000*sys_cnt/T_delta))
          print('sensor loop:'+str(T_loop_delta)+'ms')
          print("Akku status:"+str(map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100))+'%')
          print('')
       if(RTC_cnt%50 == 0):
         try:
               RTC_cnt =0
               label_RTCinfo.set_text(str(rtc.datetime()[4])+":"+str(rtc.datetime()[5]))
         except:
               print("NTP time not available, check wifi!")
       #label_sysinfo.set_text('run_cnt:'+str(sys_cnt))
       #rgb.setColorAll(0x000000)
       sys_cnt=0
       RTC_cnt = RTC_cnt+1
       T_start=time.ticks_ms()#must stay at the end, print process cost about 300ms
       
    T_loop_delta = time.ticks_diff(time.ticks_ms(), T_loop)   






