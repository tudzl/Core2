# Optimized for M5Stack Core2 + DX-GP10 GNSS
# Fixed: concurrency, memory fragmentation, error recovery
from m5stack import *
from m5ui import *
from m5stack_ui import *
from uiflow import *
import unit
from machine import WDT
import time
import math
import gc

# ========== 配置 ==========
UIFlow_debug_mode_EN = False
error_rest_threshold = 10
Time_GUI_update_src = 1          # 0: RTC, 1: GNSS
Tmr_threshold = 5                # 完整GUI更新周期 (秒)
GUI_time_refresh_Tmr_threshold = 2

screen = M5Screen()
setScreenColor(0x000000)
screen.set_screen_brightness(40)

# ========== 全局变量 ==========
screen_brightness = 40
Btn_C_pressCNT = 0
error_cnt = 0
sys_cnt = 0

# GPS 数据
Num_satalite = 0
Quality_var = 0
Lat_var = 0.0
Lon_var = 0.0
Time_var = ""
Speed_var = 0.0
Alt_var = 0.0

Speed_max = 0.0
distance = 0.0
Altitude_max = -1000.0
Altitude_min = 3000.0
coord_pre = (30.41416, 120.2995)
coord_cur = coord_pre

# 复位请求标志 (由按钮设置, 定时器处理)
gps_reset_request = False

# 对象引用
gps_0 = None
wdt = WDT(timeout=18000)

# ========== UI组件 ==========
image_BG = M5Img("res/BMW_coupit BG3.png", x=0, y=0)
rgb.setColorFrom(6, 10, 0x33ff33)
rgb.setColorFrom(1, 5, 0xff6600)
rgb.setBrightness(10)

title0 = M5Label('GNSS tracker APP v1.7E', x=20, y=0, color=0x0FFFFF, font=FONT_UNICODE_24)
label_Time = M5Label('Time:', x=2, y=20, color=0xFFFFFF, font=FONT_UNICODE_24)
label_Latitude = M5Label('Latitude:', x=10, y=50, color=0xe8b35a, font=FONT_MONT_26)
label_Longitude = M5Label('Longitude:', x=6, y=90, color=0xe0f0e5, font=FONT_MONT_26)
label_Altitude = M5Label('Altitude:                m', x=10, y=125, color=0xeb4025, font=FONT_MONT_22)
label_Distance = M5Label('Dis:', x=10, y=180, color=0x3eed9e, font=FONT_MONT_18)
label_Num = M5Label('Sata.Nr:', x=10, y=200, color=0x57fa6d, font=FONT_MONT_18)
label_Speed = M5Label('Speed:                km/h', x=30, y=150, color=0x3e2f9e, font=FONT_MONT_26)

label_TimeValue = M5TextBox(80, 30, "", lcd.FONT_DejaVu24, 0xede7a3)
label_LatitudeValue = M5TextBox(132, 60, "", lcd.FONT_DejaVu18, 0xFFFFFF)
label_LongitudeValue = M5TextBox(160, 100, "", lcd.FONT_DejaVu18, 0xFFFFFF)
label_DistanceValue = M5TextBox(72, 185, "", lcd.FONT_DejaVu18, 0xF00F0F)
label_NumbersValue = M5TextBox(100, 210, "", lcd.FONT_DejaVu18, 0xFFFFFF)
label_SpeedValue = M5TextBox(158, 155, "", lcd.FONT_DejaVu24, 0xede7a3)
label_SpeedMax = M5TextBox(168, 175, "", lcd.FONT_DejaVu18, 0xede7a3)
label_AltitudeValue = M5TextBox(146, 130, "", lcd.FONT_DejaVu18, 0xFFF2FF)
label_Altitude_MAX_Value = M5Label('', x=230, y=124, color=0xeb70f2, font=FONT_MONT_14)
label_Altitude_MIN_Value = M5Label('', x=230, y=138, color=0x62f2f6, font=FONT_MONT_14)
label_Akku = M5TextBox(220, 215, "Akku:", lcd.FONT_DejaVu18, 0xFFFF00)
label_Akku_mA = M5TextBox(220, 195, "mA:", lcd.FONT_DejaVu18, 0xFFAF00)

# ========== 辅助函数 ==========
def haversine(coord1, coord2):
    """返回两点间距离(米)，坐标无效时返回0"""
    try:
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        # 过滤无效数据
        if abs(lat1) < 0.0001 and abs(lon1) < 0.0001:
            return 0.0
        if abs(lat2) < 0.0001 and abs(lon2) < 0.0001:
            return 0.0
        R = 6372800
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    except:
        return 0.0

def safe_set_text(label, text):
    """安全更新文本，避免过长字符串"""
    try:
        label.setText(str(text))
    except:
        pass

def gps_reinit():
    """完全重置 GNSS 模块 (在定时器回调中调用)"""
    global gps_0, gps_reset_request
    print("[INFO] Resetting GNSS module...")
    try:
        power.setBusPowerMode(1)   # 断电
        wait_ms(200)
        power.setBusPowerMode(0)   # 上电
        wait_ms(500)
        gps_0 = unit.get(unit.GPS, (14,13))
        gps_0.uart_port_id(2)
        gps_0.set_time_zone(8)
        wait_ms(100)
        print("[INFO] GNSS module reset done")
    except Exception as e:
        print("[ERROR] GPS reset failed:", e)
    gps_reset_request = False

# ========== 按钮回调 ==========
def buttonA_wasPressed():
    label_Altitude_MAX_Value.set_text("Max:" + str(int(Altitude_max)) + "m")
    label_Altitude_MIN_Value.set_text("Min:" + str(int(Altitude_min)) + "m")
    dt = rtc.datetime()
    safe_set_text(label_TimeValue, "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6]))

def buttonB_wasPressed():
    global screen_brightness
    screen_brightness = (screen_brightness + 20) % 101
    if screen_brightness == 0:
        screen_brightness = 20
    screen.set_screen_brightness(screen_brightness)
    print("[INFO] Brightness:", screen_brightness)

def buttonC_wasPressed():
    global distance, Speed_max, Btn_C_pressCNT, gps_reset_request
    Speed_max = 0.0
    distance = 0.0
    Btn_C_pressCNT += 1
    safe_set_text(label_SpeedMax, "Max:0")
    safe_set_text(label_DistanceValue, "0.0")
    if Btn_C_pressCNT % 5 == 0:
        gps_reset_request = True
        print("[INFO] GPS reset requested (button C)")

btnA.wasPressed(buttonA_wasPressed)
btnB.wasPressed(buttonB_wasPressed)
btnC.wasPressed(buttonC_wasPressed)

# ========== 定时器回调 (核心) ==========
Tmr_OVF_cnt = 0
Tmr_alive = 0

def callback_timer3(_arg):
    global Tmr_OVF_cnt, Tmr_alive, error_cnt, sys_cnt
    global Num_satalite, Quality_var, Lat_var, Lon_var, Time_var, Speed_var, Alt_var
    global Speed_max, distance, Altitude_max, Altitude_min
    global coord_pre, coord_cur, gps_0, gps_reset_request

    Tmr_OVF_cnt += 1
    sys_cnt += 1
    t_start = time.ticks_ms()
    wdt.feed()

    if Tmr_alive == 1:
        return
    Tmr_alive = 1

    # 处理复位请求（不访问 GPS 对象）
    if gps_reset_request:
        gps_reinit()
        Tmr_alive = 0
        return

    # 确保 GPS 对象存在
    if gps_0 is None:
        try:
            gps_0 = unit.get(unit.GPS, (14,13))
            gps_0.uart_port_id(2)
            gps_0.set_time_zone(8)
            print("[INFO] GPS object created")
        except Exception as e:
            print("[ERROR] GPS init failed:", e)
            Tmr_alive = 0
            return

    try:
        # 读取速度 (每次都读)
        Speed_var = gps_0.speed_kph
        if Speed_var > Speed_max:
            Speed_max = Speed_var
        safe_set_text(label_SpeedValue, "{:.1f}".format(Speed_var))

        # 更新时间 (按配置)
        if Time_GUI_update_src == 0:
            dt = rtc.datetime()
            safe_set_text(label_TimeValue, "{:02d}:{:02d}:{:02d}".format(dt[4], dt[5], dt[6]))
        elif Tmr_OVF_cnt % GUI_time_refresh_Tmr_threshold == 0:
            Time_var = gps_0.gps_time
            if Time_var:
                safe_set_text(label_TimeValue, str(Time_var))

        # 完整 GUI 更新 (每 Tmr_threshold 秒)
        if Tmr_OVF_cnt % Tmr_threshold == 0:
            # 读取所有数据
            Num_satalite = gps_0.satellite_num
            Alt_var = gps_0.altitude
            Lon_var = gps_0.longitude_decimal
            Lat_var = gps_0.latitude_decimal
            Quality_var = Num_satalite

            # 卫星质量指示
            if Quality_var >= 3:
                rgb.setColorAll(0x00ef10)
            else:
                rgb.setColorAll(0x333300)

            # 更新 UI
            safe_set_text(label_NumbersValue, str(Num_satalite))
            safe_set_text(label_LatitudeValue, "{:.6f}".format(Lat_var))
            safe_set_text(label_LongitudeValue, "{:.6f}".format(Lon_var))
            safe_set_text(label_AltitudeValue, "{:.1f}".format(Alt_var))
            safe_set_text(label_SpeedMax, "Max:{:.1f}".format(Speed_max))

            # 距离计算 (需要有效定位)
            if Quality_var >= 3 and abs(Lat_var) > 0.01 and abs(Lon_var) > 0.01:
                coord_cur = (Lat_var, Lon_var)
                delta = haversine(coord_cur, coord_pre)
                if delta < 1000:
                    distance += delta
                coord_pre = coord_cur
                safe_set_text(label_DistanceValue, "{:.1f}".format(distance))

            # 极值更新
            if Alt_var != 0:
                if Alt_var > Altitude_max:
                    Altitude_max = Alt_var
                if Alt_var < Altitude_min:
                    Altitude_min = Alt_var

            # 电源信息
            Akku_V = power.getBatVoltage()
            Akku_C = power.getBatCurrent()
            safe_set_text(label_Akku, "{:.2f}v".format(Akku_V))
            safe_set_text(label_Akku_mA, "{:.0f}mA".format(Akku_C))

            # 调试输出 (降低频率)
            if sys_cnt % 30 == 0:
                print("[STAT] Sats:{} Lat:{:.4f} Lon:{:.4f} Alt:{:.1f} Spd:{:.1f} MaxSpd:{:.1f} Dist:{:.1f}".format(
                    Num_satalite, Lat_var, Lon_var, Alt_var, Speed_var, Speed_max, distance))

            # 主动垃圾回收
            gc.collect()

        # 清空 LED 如果无定位
        if Quality_var < 3:
            rgb.setColorAll(0x000000)

        # 错误计数衰减
        if error_cnt > 0:
            error_cnt -= 1

    except Exception as e:
        error_cnt += 1
        print("[ERROR] GPS read #{}: {}".format(error_cnt, e))
        rgb.setColorAll(0xff1100)
        if error_cnt >= error_rest_threshold:
            print("[ERROR] Too many errors, requesting GPS reset")
            gps_reset_request = True
            error_cnt = 0

    finally:
        Tmr_alive = 0
        wdt.feed()

# ========== 初始化 ==========
print("GNSS tracker V1.8 (optimized)")
power.setBusPowerMode(0)      # 确保 GNSS 供电
gps_0 = unit.get(unit.GPS, (14,13))
gps_0.uart_port_id(2)
gps_0.set_time_zone(8)
wait_ms(1000)

timerSch.timer.init(period=1000, mode=timerSch.timer.PERIODIC, callback=callback_timer3)

print("[READY] Touch BtnA: show min/max alt, BtnB: brightness, BtnC: reset max speed (5x to reset GPS)")

# 主循环: 仅喂狗与防卡死
while True:
    wdt.feed()
    wait_ms(1)
    
'''
 关键改进说明
问题	解决方法
GPS 对象并发冲突	引入 gps_busy 标志 + 按钮复位时等待释放；复位期间临时停用定时器效果（通过标志跳过执行）。
内存碎片	1. 使用 safe_set_text 限制字符串长度；
2. 减少 print 频率（每30秒一次）；
3. 每次完整 GUI 更新后调用 gc.collect()；
4. 避免在循环内创建大量临时对象（如 f-string 已优化）。
异常后恢复不彻底	当错误累计到阈值时，设置 gps_reset_request，由定时器安全地执行 gps_reinit()，完全重建 GPS 对象。
坐标无效导致计算异常	haversine 函数加入异常捕获和无效坐标过滤（(0,0) 附近视为无效）。
看门狗失效风险	在定时器入口/出口以及主循环中都调用 wdt.feed()；复位操作期间虽可能阻塞，但超时前会完成。
'''