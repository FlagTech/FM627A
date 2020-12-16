import wemotor
import time

motor = wemotor.Motor()

motor.move(20,80)  # 左轉     
time.sleep(1)
motor.move(80,20)  # 右轉
time.sleep(1)
motor.move(0,0)    # 停止