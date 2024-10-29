#current issue: stuck after some time running! unknown reason,with GC solved?
#V1.7B fixed distance bugs! tested haversine calc working! 
#V1.7A added gc collect and distance calc!!!
#V1.6D fixed max min bug! int(var) for max()
#V1.6C added update from RTC mode, and uiflow debug mode
#V1.6B improved timer callback loops! need test
#V1.6 2024.10.13, added max Altitude record, distance function!
#V1.5D 2024.10.13, added max Altitude record, distance function!
#Zell 2024.10.7.  beta version
#tested working with DX GP-10 moule and UIFLOW 1.13.8 core2!
#9DFA6B05
from m5stack import *
from m5ui import *
from m5stack_ui import *
from uiflow import *
import unit
from machine import WDT
import time
import math
import gc

UIFlow_debug_mode_EN = False
error_rest_threshold = 10
Time_GUI_update_src = 1 #0: from M5 RTC, 1 from GNSS
screen = M5Screen()
#screen.set_screen_brightness(50)
setScreenColor(0x000000)
gps_0 = unit.get(unit.GPS, (14,13))

screen_brightness = 40
screen_brightness_max = 100
screen_brightness_min = 0
Akku_V = 0
Akku_C = 0
error_cnt = 0
sys_cnt = 0

Num_satalite = 0
Num_satalite_tmp = 0
Quality_pos = None
Quality_var = 0
Lon_var = None
Lat_var = None
Time_var = None
Speed_var = None
Alt_var = None
Speed_max = 0
Speed_ave = 0
Altitude_max = 0
Altitude_min = 3000
Distance_sofar = None


Tmr_alive = 0
Tmr_OVF_cnt = 0
#Tmr_threshold = const(9)
Tmr_threshold = 5
GUI_time_refresh_Tmr_threshold  = 2

print('GNSS_test based on DX-GP10 GNSS module(AT6558) V1.7B')
print('Zell beta version  FW @2024.10.29')
image_BG = M5Img("res/BMW_coupit BG3.png", x=0, y=0)
#image_BG = M5Img(0, 0, "res/BMW_coupit BG3.png")
rgb.setColorFrom(6, 10, 0x33ff33)#Left
rgb.setColorFrom(1, 5, 0xff6600)
rgb.setBrightness(10)
if(UIFlow_debug_mode_EN):
  #wifiCfg.autoConnect(lcdShow=False)
  wifi_alive = wifiCfg.wlan_sta.isconnected()
  print('#>:UIflow debug enabled, Wifi shoud be connected:'+str(wifi_alive))
  rtc.settime('ntp', host='cn.pool.ntp.org', tzone=8)
  #print('#>RTC time: hour,min,sec:')
  #print(rtc.datetime()[4])
  #print(rtc.datetime()[5])
  #print(rtc.datetime()[6])
#print(rtc.datetime())
print(rtc.printRTCtime())


title0 = M5Label('GNSS tracker APP v1.7B', x=20,y=0,color=0x0FFFFF, font=FONT_UNICODE_24, parent=None)
label_Time = M5Label('Time:', x=2, y=20, color=0xFFFFFF, font=FONT_UNICODE_24, parent=None)
#label_Time = M5TextBox(0, 20, "Time:", lcd.FONT_Default, 0xFFFFFF, rotate=0)
label_Time.set_hidden(False)
label_Latitude = M5Label('Latitude:', x=10, y=50, color=0xe8b35a, font=FONT_MONT_26, parent=None)
#label_Latitude = M5TextBox(20, 40, "Latitude:", lcd.FONT_Default, 0xe8b35a, rotate=0)
label_Latitude.set_hidden(False)

label_Longitude = M5Label('Longitude:', x=6, y=90, color=0xe0f0e5, font=FONT_MONT_26, parent=None)
#label_Longitude = M5TextBox(6, 90, "Longitude:", lcd.FONT_DejaVu18, 0xeb40e5, rotate=0)
label_Longitude.set_hidden(False)
label_Altitude = M5Label('Altitude:                m', x=10, y=125, color=0xeb4025, font=FONT_MONT_22, parent=None)

#label_Quality = M5TextBox(10, 180, "Quality:", lcd.FONT_Default, 0x3eed9e, rotate=0)
#label_Quality = M5Label('Qos:', x=10, y=180, color=0x3eed9e, font=FONT_MONT_18, parent=None)
label_Distance = M5Label('Dis:', x=10, y=180, color=0x3eed9e, font=FONT_MONT_18, parent=None)
#label_Quality.set_hidden(False)

#label_Num = M5TextBox(10, 220, "Numbers:", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
label_Num = M5Label('Sata.Nr:', x=10, y=200, color=0x57fa6d, font=FONT_MONT_18, parent=None)
label_Num.set_hidden(False)

label_Speed =  M5Label('Speed:                km/h', x=30, y=150, color=0x3e2f9e, font=FONT_MONT_26, parent=None)

label_TimeValue = M5TextBox(80, 30, "", lcd.FONT_DejaVu24, 0xede7a3, rotate=0)
label_LatitudeValue = M5TextBox(132, 60, "", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
label_LongitudeValue = M5TextBox(160, 100, "", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)
#label_QualityValue = M5TextBox(72, 185, "", lcd.FONT_DejaVu18, 0xF00F0F, rotate=0)
label_DistanceValue = M5TextBox(72, 185, "", lcd.FONT_DejaVu18, 0xF00F0F, rotate=0)
label_NumbersValue = M5TextBox(100, 210, "", lcd.FONT_DejaVu18, 0xFFFFFF, rotate=0)#FONT_Comic
label_SpeedValue=M5TextBox(158, 155, "", lcd.FONT_DejaVu24, 0xede7a3, rotate=0)#FONT_Comic
label_SpeedMax=M5TextBox(168, 175, "", lcd.FONT_DejaVu18, 0xede7a3, rotate=0)#FONT_Comic
label_AltitudeValue=M5TextBox(146, 130, "", lcd.FONT_DejaVu18, 0xFFF2FF, rotate=0)
label_Altitude_MAX_Value=M5Label('', x=230, y=124, color=0xeb70f2, font=FONT_MONT_14, parent=None)
label_Altitude_MIN_Value=M5Label('', x=230, y=138, color=0x62f2f6, font=FONT_MONT_14, parent=None)
label_Akku =  M5TextBox(220, 215, "Akku:", lcd.FONT_DejaVu18, 0xFFFF00, rotate=0)
label_Akku_mA =  M5TextBox(220, 195, "mA:", lcd.FONT_DejaVu18, 0xFFAF00, rotate=0)
wdt = WDT(timeout=15000)

distance = 0
LP_coord = 30.41416,120.2995 #lat, Longitude
coord_pre = LP_coord
coord_tmp = LP_coord

london_coord = 51.5073219,  -0.1276474
berlin_coord = 52.5170365,  13.3888599
cities = {
    'berlin': (52.5170365,  13.3888599),
    'vienna': (48.2083537,  16.3725042),
    'sydney': (-33.8548157, 151.2164539),
    'madrid': (40.4167047,  -3.7035825) 
}


#display max min Alt. , distance info
def buttonA_wasPressed():
  # global params
  global uart1,Altitude_max,Altitude_min,Distance_sofar,Time_var,label_Altitude_MAX_Value
  print('>>BTN_A pressed!')
  label_Altitude_MAX_Value.set_text('Max:'+str(Altitude_max)+'m')
  label_Altitude_MIN_Value.set_text('Min:'+str(Altitude_min)+'m')
  #print('>>screen brightness changed to'+str(screen_brightness))
  pass
btnA.wasPressed(buttonA_wasPressed)


#LCD BG light control
def buttonB_wasPressed():
  # global params
  global screen_brightness,screen_brightness_max,screen_brightness_min,screen,uart1
  print('>>BTN_B pressed!')
  screen_brightness = screen_brightness+20
  if (screen_brightness> screen_brightness_max):
      screen_brightness = screen_brightness_min
  screen.set_screen_brightness(screen_brightness)
  print('>>screen brightness changed to'+str(screen_brightness))
  pass
btnB.wasPressed(buttonB_wasPressed)

#clear speed max value
def buttonC_wasPressed():
  # global params
  global Speed_max,Speed_ave,error_cnt,uart1,label_SpeedMax
  Speed_max = 0
  label_SpeedMax.setText('Max:'+str(Speed_max))
  print('>>BTN_C pressed, Max speed cleared')
  pass
btnC.wasPressed(buttonC_wasPressed)


def haversine(coord1, coord2):
    R = 6372800  # Earth radius in meters
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    phi1, phi2 = math.radians(lat1), math.radians(lat2) 
    dphi       = math.radians(lat2 - lat1)
    dlambda    = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2)**2 + \
        math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    
    return 2*R*math.atan2(math.sqrt(a), math.sqrt(1 - a))


def callback_timer3(_arg):
  global Num_satalite, Quality_pos, Lon_var, Lat_var, Time_var, Speed_var, Alt_var,Tmr_OVF_cnt,Akku_V,Akku_C,error_cnt,uart1,Speed_max,Quality_var
  global GUI_time_refresh_Tmr_threshold,Altitude_max,Altitude_min,Distance_sofar,Tmr_alive
  global london_coord,berlin_coord,distance,sys_cnt,coord_pre,coord_cur
  Tmr_OVF_cnt = Tmr_OVF_cnt+1
  wdt.feed()
  sys_cnt = sys_cnt+1
  tck_start = time.ticks_ms()
  #print('tck_Anf.:'+str(tck_start))
  if(0==Tmr_alive):
      try:
          #if (Num_satalite>1): #has issues!
          #    rgb.setColorAll(0x00ef10)
          #else:
              #rgb.setColorAll(0x333300)
          Tmr_alive = 1
          rgb.setColorFrom(7, 8, 0x33ff33)#Left   
          #Time_var = gps_0.gps_time
          #print ('Speed:'+str(gps_0.speed_kph))
          Speed_var = gps_0.speed_kph
          #print ('Speed:'+str(gps_0.speed_kph))
          if (Speed_max<float(Speed_var)):
              Speed_max = float(Speed_var)
          #print('tck_parse_ms:'+str(time.ticks_ms()-tck_start)) #about 5ms
          #label_TimeValue.setText(str(Time_var))
          label_SpeedValue.setText(str(Speed_var))
          if (0==Time_GUI_update_src):
            label_TimeValue.setText(str(rtc.datetime()[4])+':'+str(rtc.datetime()[5])+'-'+str(rtc.datetime()[6]))#cost more than GNSS time get
          elif(0==(Tmr_OVF_cnt%GUI_time_refresh_Tmr_threshold)):
              rgb.setColorFrom(2, 3, 0xa3ff03)#Left   
              Time_var = gps_0.gps_time
              #print("GNSS Time:"+str(Time_var))#40ms
              label_TimeValue.setText(str(Time_var))
          
          
          if(0==Tmr_OVF_cnt%Tmr_threshold):
            #wdt.feed()
            print('>>:Update GUI now!')
            #Tmr_OVF_cnt = 0
            tck_gui = time.ticks_ms()
            #print('tck_start:'+str(time.ticks_ms()))
            Akku_V = power.getBatVoltage()
            Akku_C = power.getBatCurrent()
            label_Akku.setText(str(Akku_V)+' v')
            label_Akku_mA.setText(str(Akku_C)+'mA')
            Num_satalite = gps_0.satellite_num
            Quality_pos = gps_0.pos_quality
            Alt_var = gps_0.altitude
            Lon_var = gps_0.longitude_decimal
            Lat_var = gps_0.latitude_decimal
            Quality_var = int(Num_satalite)
            if (Quality_var>=3): #has issues!
              rgb.setColorAll(0x00ef10)
            else:
              rgb.setColorAll(0x333300)
            #print('-update label-')
            coord_cur = Lat_var,Lon_var
            distance_tmp = haversine(coord_cur, coord_pre)
            if (distance_tmp< 1000):
              distance = distance+distance_tmp
            coord_pre = Lat_var,Lon_var
            
            label_DistanceValue.setText(str(f'{distance:.1f}'))
            label_NumbersValue.setText(str(Num_satalite))
            #label_QualityValue.setText(str(Quality_pos))
            label_LatitudeValue.setText(str(Lat_var))
            label_LongitudeValue.setText(str(Lon_var))
            label_AltitudeValue.setText(str(Alt_var))
            label_SpeedMax.setText('Max'+str(Speed_max))
            #math.atan(x)
            print('GUI_loop_ms:'+str(time.ticks_ms()-tck_gui))
            print('GNSS time:'+str(Time_var))
            print('--Latitude:'+str(Lat_var))
            print('--Longitude:'+str(Lon_var))
            print('--Altitude:'+str(Alt_var))
            print('>>:Max Speed:'+str(Speed_max)+'km/h')
            print('>>:Distance:'+str(distance))
            print('>>:coord_cur:'+str(coord_cur))
            #print(rtc.printRTCtime())
            #print('--A:'+str(float(Alt_var)))
            Altitude_max = max((Altitude_max),float(Alt_var)) #int has issues for negative values?
            Altitude_min = min((Altitude_min),float(Alt_var))
            print('>>:Max Alt:'+str(Altitude_max)+'m')
            print('>>:Min Alt:'+str(Altitude_min)+'m')
            print('--Num_satalite:'+str(Num_satalite))
            print('Akku Voltage:'+str(Akku_V))
            print('Akku Current:'+str(Akku_C))
            #time cost about 220ms
            #print('tck_end:'+time.ticks_ms())
            gc.collect()
          rgb.setColorAll(0x000000)
      except:
          print('>>:GNSS read/parse error!'+str(error_cnt))
          print('>>:Check module status and position!')
          error_cnt = error_cnt+1
          rgb.setColorAll(0xff1100)
          #power.setBusPowerMode(1)
          if(0==error_cnt%error_rest_threshold):
            print('#>:Too many errors occured, reset GNSS module now!')
            power.setBusPowerMode(1)#disable Mbus 5V power
            wait_ms(200)
            power.setBusPowerMode(0)#Enable Mbus 5V power
          if(error_cnt>(2*error_rest_threshold)):
            #reset sys
            print('#>:Too much error occured, should rest now!')
            #machine.reset()
            
          pass
      wdt.feed()
      Tmr_alive = 0
      #print('tck_E:'+str(time.ticks_ms()))#small loop about 60 to 65 ms/80ms
      print('#>:TMR loop time_ms:'+str(time.ticks_ms()-tck_start))#small loop about 60 to 65 ms, 2 lables updates, large loop 500-600ms
  pass


gps_0.uart_port_id(2)
gps_0.set_time_zone(8)
wait_ms(1000)#allow UI to rendering before timer is called!
timerSch.timer.init(period=1000, mode=timerSch.timer.PERIODIC, callback=callback_timer3)
Tmr_alive =0
print('>>:Touch BtnA to display max min Alt. and distance info')
print('>>:Touch BtnB to change display brightness')
print('>>:Touch BtnC to clear speed max value')
distance = haversine(london_coord, berlin_coord) #test only
print('>>:Distance from London to Berlin:'+str(distance))
distance =0
while True:
  wdt.feed()
  wait_ms(2)
#wdt = WDT(timeout=22000)
#wdt.feed()
#end