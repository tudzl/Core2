from m5stack import *
from m5ui import *
from uiflow import *
remoteInit()

setScreenColor(0x111111)




led_flag = None
text_input = None
Akku_soc = None
spk_flag = None



label_txt_input = M5TextBox(8, 219, "label0", lcd.FONT_Default, 0x58dd68, rotate=0)




def _remote_LED_ON_OFF(led_flag):
  global text_input, Akku_soc, spk_flag 
  if led_flag == 1:
    rgb.setColorFrom(6, 10, 0xff9900)
    rgb.setColor(3, 0xcc33cc)
    rgb.setColor(5, 0x993399)
    rgb.setColorFrom(1, 5, 0x33cc00)
    rgb.setColor(6, 0xcc0000)
    rgb.setColor(10, 0xcc0000)
  else:
    rgb.setColorAll(0x000000)

def _remote_Bright(led_flag):
  global text_input, Akku_soc, spk_flag 
  rgb.setBrightness(led_flag)

def _remote_InputName(text_input):
  global Akku_soc, led_flag, spk_flag 
  text_input = text_input
  label_txt_input.setText(str(text_input))

def _remote_M5_Akku(Akku_soc):
  global text_input, led_flag, spk_flag 
  Akku_soc = power.getBatteryLevel()
  pass
def _remote_SPK_test(spk_flag):
  global text_input, Akku_soc, led_flag 
  Akku_soc = power.getBatteryLevel()
  spk_flag = 1
  speaker.sing(220, 1)


lcd.qrcode('http://flow-remote.m5stack.com/?remote=1264019049256321024', 72, 32, 176)
spk_flag = 0
label_txt_input.setText('Hello,wait for input')

# Describe this function...

# Describe this function...

# Describe this function...

# Describe this function...

# Describe this function...
