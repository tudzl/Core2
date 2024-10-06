#INA260_Core2 demo V2.8  0162C86C
#Zell 2024.10.6
#hall speed detect
#port B G26,G36: pin26 not working as digitalRead,
from m5stack import *
from m5stack_ui import *
from uiflow import *
from MediaTrans.AudioPlay import AudioPlay

from easyIO import *
import i2c_bus
import time



Sensor_pin = 36 #PortB last pin
PWM_pin = 26
PWM_Freq = 4
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)



PWM0 = machine.PWM(26, freq=PWM_Freq, duty=98, timer=0)
PWM_EN = 1
#PWM0.pause()
#PWM0.resume()
#image_BG = M5Img("res/BMW_next.png", x=0, y=0, parent=None)
image_BG = M5Img("res/BMW_coupit BG3.png", x=0, y=0, parent=None)
Title = M5Label('INA260_Core2 Hall demo V2.8', x=20, y=5, color=0x2517de, font=FONT_MONT_14, parent=None)

label_vol = M5Label('Vbus_In:', x=20, y=40, color=0xEE9E00, font=FONT_MONT_18, parent=None)
label_Cur = M5Label('Current:', x=20, y=60, color=0xEE1E00, font=FONT_MONT_18, parent=None)
label_Pow = M5Label('Power  :', x=20, y=80, color=0xCCCCCC, font=FONT_MONT_18, parent=None)

#label_Hall = M5Label('Hall:', x=220, y=40, color=0xEEAE00, font=FONT_MONT_16, parent=None)
#label_Hall2 = M5Label('Hall2:', x=220, y=100, color=0xEE1E00, font=FONT_MONT_16, parent=None)
#label_speed = M5Label('speed:', x=200, y=80, color=0x4EEE10, font=FONT_MONT_18, parent=None)
#label_speed_num = M5Label('22', x=150, y=100, color=0xCEEEC0, font=FONT_MONT_34, parent=None)
#label_speed_kmh = M5Label('km/h', x=260, y=110, color=0xEEAE00, font=FONT_MONT_20, parent=None)
#label_T_cycle = M5Label('CycleT:', x=160, y=160, color=0xA22252, font=FONT_MONT_16, parent=None)
#label_PWM_FREQ=  M5Label('PWM:', x=160, y=180, color=0xCEBE00, font=FONT_MONT_16, parent=None)
label_sysinfo = M5Label('Sys_cnt', x=130, y=220, color=0xA0C0A0, font=FONT_MONT_12, parent=None)
label_Akkuinfo = M5Label('Akku', x=280, y=5, color=0x504020, font=FONT_MONT_12, parent=None)

touch_button_HighPrecision = M5Btn(text='PWM', x=225, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)
#touch_button_HighPrecision = M5Btn(text='HiRes', x=225, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)
touch_button_INA = M5Btn(text='INA', x=25, y=200, w=70, h=30, bg_c=0xFFFFFF, text_c=0x85d612, font=FONT_MONT_14, parent=None)


def touch_button_HighPrecision_pressed():
  # global params
  global PWM_EN
  print('HiRes button was Touched')
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

T_alert = 35  #in C degree
T_OS1= (T_alert* 32*8 )
T_OS1_reg_data = T_OS1.to_bytes(2,'b') 






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


#class LM75(object):
class LM75():
	def __init__(self, mode=LM75_CONF_OS_COMP_INT, address=LM75_ADDRESS):
		self._mode = mode
		self._address = address
		#self._bus = smbus.SMBus(busnum)
		self._bus =i2c_bus.i2c0
		#i2c0.read_reg(0x00, 2))

	def regdata2float (self, regdata):
		return (regdata / 32.0) / 8.0
	def toFah(self, temp):
		return (temp * (9.0/5.0)) + 32.0
	#def setTosReg(value) 
	  #i2c0.write_u16(LM75_TOS_REGISTER,value, byteorder="big") # not working
	  #i2c0.write_mem_data(LM75_TOS_REGISTER, value, i2c_bus.INT16LE)
	  #i2c0.write_data(0, i2c_bus.UINT8LE)
	  #return 0

	def getRawTemp():
		"""Reads the raw temp from the LM75 sensor"""
		#raw = self._bus.read_word_data(self._address, LM75_TEMP_REGISTER) & 0xFFFF
		raw = i2c0.read_reg(LM75_TEMP_REGISTER,2)
		#print "raw: "
		#print raw
		#raw_int = ((raw << 8) & 0xFF00) + (raw >> 8)
		return raw
	def CalcTemp(raw):
		"""calc the temp from the raw LM75 sensor value(11bit), LSB 0.125 C"""
		#raw = self._bus.read_word_data(self._address, LM75_TEMP_REGISTER) & 0xFFFF
		Temp_int = int.from_bytes(raw,'b') #B uint8; b int8
		Temp_F = (Temp_int / 32.0) / 8.0 
		#Temp_F = Temp_F * (9.0/5.0) + 32.0
		#print "raw: "
		#print raw
		#raw_int = ((raw << 8) & 0xFF00) + (raw >> 8)
		return Temp_F
		
	def getTemp(self): #not working!
		"""Reads the temp from the LM75 sensor"""
		#raw = self._bus.read_word_data(self._address, LM75_TEMP_REGISTER) & 0xFFFF
		raw = self._bus.read_reg(LM75_TEMP_REGISTER,2) & 0xFFFF
		#print "raw: "
		#print raw
		#raw = ((raw << 8) & 0xFF00) + (raw >> 8)
		return self.toFah(self.regdata2float(raw))

print('Core2 INA260 measurement & Hall speed coupit V2.6B ')
print('Author: Zell, 22.April.2021')

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
T_interval = 250
T_cycle = 1000
WheelSPD = 0
WheelSPD_KMH = 0
#i2c0 = i2c_bus.easyI2C((26, 32), LM75_ADDRESS, freq=100000)
i2c0 = i2c_bus.easyI2C(IIC_PORTA, LM75_ADDRESS2, freq=400000)
LM75_sensor = LM75
Scan_EN = True
Scan_cnt = 0
OUT_EN = True
gun_stop_cnt = 0
while (Scan_EN):
    try :
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
           
        if (LM75_ADDRESS == addrList[i]):
           print('>:LM75_1 detected!')
           LM75A1_OK = True   
                      
        if (LM75_ADDRESS2 == addrList[i]):
           print('>:LM75_2 detected!')
           LM75A2_OK = True   
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
      if(Scan_cnt>5):
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
T_start = time.ticks_ms() # get millisecond counter  
T_Hall = T_start
T_cycle_tmp = T_Hall
T_loop_delta = 0
Wheel_run_cnt = 0
Wheel_pos = 0 #1 @ sensor in position, 0@ other positions (359 degree?)
while 1:
    
    T_loop = time.ticks_ms()
    if(INA_OK):
      try:
        i2c0 = i2c_bus.easyI2C(IIC_PORTA, INA260_ADDRESS, freq=100000)
        Current_raw = i2c0.read_reg(INA260_REG_CURRENT,2)
        #print ('Current_raw: '+str(Current_raw))
         #positive values   
        Current = int.from_bytes(Current_raw, True) #B uint8; b int8;signed 
        #negative values   
        if(Current > 32768):
           Current = Current - 65536
        Current = 1.25*Current

        #----------OCP-------------
        #stop gun@ over current

           
        Voltage_raw = i2c0.read_reg(INA260_REG_BUSVOLTAGE,2)
        Vbus =  int.from_bytes(Voltage_raw, 'b') #B uint8; b int8;signed 
        Vbus = 1.25*Vbus/1000.0
        
        
        Power_raw = i2c0.read_reg(INA260_REG_POWER,2)
        Power_INA =  10.0* int.from_bytes(Power_raw, 'b') #B uint8; b int8;signed 
        #----------debug print-------------
        if(debug_print_EN):
          if ((abs(Current)>1000)):
            print ('Current: '+str(Current/1000.0)+'A')
          else:
            print ('Current: '+str(Current)+'mA')
          print ('Vbus: '+str(Vbus)+'V')
          print ('Power: '+str(Power_INA)+'mW')
      except:
        print('INA260 read error')
        rgb.setColorAll(0xff1133)
        wait_ms(100)
        rgb.setColorAll(0x000000)
        #continue
        

    sys_cnt = sys_cnt + 1

    if(T_delta>=T_interval):
       rgb.setColor(1, 0x000099)
       rgb.setColor(10, 0x000099)
       if (INA_OK):
           tmp_str ='Vbus_In:'+'%2.3F' % Vbus+ 'V'
           label_vol.set_text(tmp_str)
           
           if ((abs(Current)>1000)):
              label_Cur.set_text ('Current:'+str(Current/1000.0)+'A')
           else:
              label_Cur.set_text ('Current:'+str(Current)+'mA')
           Power_calc = Vbus*Current/1000.0  
           label_Pow.set_text('Power  :'+str(Power_calc)+'W')
           #print('Sys run cnt:'+str(Hall_status))
       else:
           touch_button_INA.set_hidden(True)
       #WheelSPD = Wheel_length/T_cycle #m/s
       Wheel_run_cnt = Wheel_run_cnt+1

       
       tmp_str = '%1.2F' % power.getBatVoltage()
       label_Akkuinfo.set_text(tmp_str+' V')
       #label_Akkuinfo.set_text(str(power.getBatVoltage())+' V')
       label_sysinfo.set_text('Sys fps:'+str(1000*sys_cnt/T_delta))
       if(debug_print_EN):
          print('Speed:'+str(WheelSPD_KMH)+'Km/h')
          print('T_delta:'+str(T_delta))
          print('Sys cnt:'+str(sys_cnt))
          print('Sys fps:'+str(1000*sys_cnt/T_delta))
          print('sensor loop:'+str(T_loop_delta)+'ms')
          print("Akku status:"+str(map_value((power.getBatVoltage()), 3.7, 4.1, 0, 100))+'%')
          print('')
       #label_sysinfo.set_text('run_cnt:'+str(sys_cnt))
       #rgb.setColorAll(0x000000)
       sys_cnt=0
       T_start=time.ticks_ms()#must stay at the end, print process cost about 300ms
       
    T_loop_delta = time.ticks_diff(time.ticks_ms(), T_loop)   


