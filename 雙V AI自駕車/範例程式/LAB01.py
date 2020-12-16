# 從 machine 模組匯入 Pin 物件
from machine import Pin
# 匯入時間相關的 time 模組
import time

# 建立 2 號腳位的 Pin 物件, 設定為輸出腳位, 並命名為 led
led = Pin(2, Pin.OUT)

led.value(0)    # 設定為低電位, 點亮 LED 
time.sleep(3)   # 暫停 3 秒
led.value(1)    # 設定為高電位, 熄滅 LED