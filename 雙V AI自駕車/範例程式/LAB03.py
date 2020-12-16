# 匯入馬達模組
import wemotor
import time

# 建立馬達物件
motor= wemotor.Motor()

motor.move(40,40)   # 前進
time.sleep(1)       # 暫停 1 秒
motor.move(-40,-40) # 後退
time.sleep(1)       # 暫停 1 秒
motor.move(0,0) # 後退