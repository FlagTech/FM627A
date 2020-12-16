import wemotor
import time

motor = wemotor.Motor()

while True:
    # 等速前進
    motor.constantSpeed('forward',0.02,0.02)