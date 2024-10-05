from m5stack import *
from m5stack_ui import *
from uiflow import *


screen = M5Screen()
screen.clean_screen()
screen.set_screen_bg_color(0xf3f9c2)
cnt=0
info=''
msg_line=''
GPU_Freq =0
ECPU_Freq =0
PCPU_Freq =0
Mem_Free = 0
auto_ack = 1

label0 = M5Label('core2_uart_demo V1.3', x=20, y=5, color=0x000, font=FONT_MONT_18, parent=None)
label1 = M5Label('RX:', x=2, y=60, color=0xf64d74, font=FONT_MONT_18, parent=None)
label2 = M5Label('TX:', x=2, y=180, color=0x4e8fdc, font=FONT_MONT_14, parent=None)
label3_GPU = M5Label('GPU:', x=2, y=90, color=0xee8f1c, font=FONT_MONT_14, parent=None)
label4_ECPU = M5Label('ECPU:', x=2, y=110, color=0x4e8f2c, font=FONT_MONT_14, parent=None)
label5_PCPU = M5Label('PCPU:', x=2, y=130, color=0xa61d14, font=FONT_MONT_14, parent=None)
label6_mem = M5Label('F_Mem:', x=2, y=150, color=0x000611, font=FONT_MONT_14, parent=None)

def buttonA_wasPressed():
  global uart1，label2,cnt,auto_ack
  msg='hello from M5'
  uart1.write('hello from M5'+str(cnt)+"\r\n")
  label2.set_text('TX:'+str(msg))
  auto_ack=1-auto_ack
  pass
btnA.wasPressed(buttonA_wasPressed)


uart1 = machine.UART(1, tx=1, rx=3)
uart1.init(115200, bits=8, parity=None, stop=1)
while True:
  if uart1.any():
    #info = (uart1.read()).decode()
    wait_ms(5)
    msg_line = (uart1.readline()).decode()
    info = msg_line
    buf= info.rsplit(",")
    cnt=cnt+1
    label1.set_text('RX:'+info)
    if (auto_ack):
      uart1.write('M5 received msg cnt:'+str(cnt)+"\r\n")
    lcd.print((info), 2, 32, 0xcc0000, rotate=0)
    try:
      label3_GPU.set_text('GPU:'+buf[0])
      label4_ECPU.set_text('ECPU:'+buf[1])
      label5_PCPU.set_text('PCPU:'+buf[2])
      label6_mem.set_text('F_Mem:'+buf[3])
    except Exception as e:
        print(e)
  wait_ms(2)