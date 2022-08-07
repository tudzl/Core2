from m5stack import *
from m5stack_ui import *
from uiflow import *
import imu
import time
#core2 IMU test by Zell, V1.0 2022.8.07
screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xFFFFFF)


loop_run = None
X_acc = None
Y_acc = None
Z_acc = None

imu0 = imu.IMU()

label0 = M5Label('label_X', x=40, y=40, color=0x000, font=FONT_MONT_14, parent=None)
label1 = M5Label('label_Y', x=40, y=72, color=0x000, font=FONT_MONT_14, parent=None)
label2 = M5Label('label_Z', x=40, y=104, color=0x000, font=FONT_MONT_14, parent=None)
label3 = M5Label('label3', x=40, y=128, color=0x000, font=FONT_MONT_14, parent=None)
label4 = M5Label('label4', x=40, y=158, color=0x000, font=FONT_MONT_14, parent=None)
label5 = M5Label('label5', x=190, y=128, color=0x000, font=FONT_MONT_14, parent=None)
label6 = M5Label('label6', x=190, y=158, color=0x000, font=FONT_MONT_14, parent=None)
label7 = M5Label('label7', x=190, y=180, color=0x000, font=FONT_MONT_14, parent=None)
label_title = M5Label('CORE2 IMU test', x=41, y=7, color=0x000, font=FONT_MONT_14, parent=None)

from numbers import Number




loop_run = 1
while loop_run:
  X_acc = imu0.acceleration[0]
  Y_acc = imu0.acceleration[1]
  Z_acc = imu0.acceleration[2]
  label0.set_text(str(X_acc))
  label1.set_text(str(Y_acc))
  label2.set_text(str(Z_acc))
  label3.set_text(str(imu0.ypr[1]))
  label4.set_text(str(imu0.ypr[2]))
  label5.set_text(str(imu0.gyro[0]))
  label6.set_text(str(imu0.gyro[1]))
  label7.set_text(str(imu0.gyro[2]))
  loop_run = (loop_run if isinstance(loop_run, Number) else 0) + 1
  wait_ms(100)
