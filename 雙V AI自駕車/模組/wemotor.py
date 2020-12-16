import ustruct
from machine import I2C, Pin
import time

i2c = I2C(scl=Pin(5),sda=Pin(4))    # freq=100000

A = const(0)   # Motor A
B = const(1)   # Motor B

BRAKE = const(0)
CCW = const(1)
CW = const(2)
STOP = const(3)
STANDBY = const(4)

leftSensor = Pin(12,Pin.IN)      # D6 左輪感測器
rightSensor = Pin(16,Pin.IN)     # D0 右輪感測器

flagL = 0   # 左輪狀態
flagR = 0   # 右輪狀態

valL = 0    # 左輪脈衝值
valR = 0    # 右輪脈衝值

speedL = 0  # 左輪速度
speedR = 0  # 右輪速度

class Motor:
    def __init__(self, address=0x30, freq=1000, standbyPin=None):
            
        self.i2c = i2c
        self.address = address
        self.standbyPin = standbyPin
        
        self.lNowSpeed = 0
        self.rNowSpeed = 0
        
        if standbyPin is not None:
            standbyPin.init(standbyPin.OUT, 0)

        self.setFreq(freq)

    def setMotor(self, dir, speed):         # setmotor(模式,轉速) 模式：1是後退、2是前進、3是停止 。轉速 0~100
        if self.standbyPin is not None:
            if dir == STANDBY:
                self.standbyPin.value(0)
                return
            else:
                self.standbyPin.value(1)

        _speed = int(speed * 100)

        if _speed > 10000:
            _speed = 10000

        if dir not in range(0,5):
           dir = 3

        s0 = _speed >> 8 & 0xff
        s1 = _speed & 0xff

        self.i2c.writeto(self.address, ustruct.pack(">4B", self.motor | 0x10, dir, s0, s1))
        
    def setFreq(self, freq):
        n0 = freq >> 16 & 0x0f
        n1 = freq >> 16 & 0xff
        n2 = freq & 0xffff

        self.i2c.writeto(self.address, ustruct.pack(">2BH", n0, n1, n2))
    
    def move(self, lSpeed, rSpeed):
        self.lNowSpeed = lSpeed
        self.rNowSpeed = rSpeed
        
        self.motor=A
        if(lSpeed>=0):
            self.setMotor(2,lSpeed)
        elif(lSpeed<0):
            self.setMotor(1,abs(lSpeed))
            
        self.motor=B    
        if(rSpeed>=0):
            self.setMotor(2,rSpeed)
        elif(rSpeed<0):
            self.setMotor(1,abs(rSpeed))
    
    # 等速前進
    def constantSpeed(self,mode, lRotating, rRotating):  #  lRotating、rRotating 0.02 有不錯的效果
        global flagL,flagR,valL,valR,speedL,speedR
        
        d_time = 20    # 單位時間(毫秒)
        
        last_time = now_time = time.ticks_ms()
        
        while (now_time-last_time<d_time):
            if(flagL == 0 and leftSensor.value() == 1):  # 左輪
                valL += 1
                flagL = 1
            if(flagL == 1 and leftSensor.value() == 0):
                valL += 1
                flagL = 0            
            if(flagR == 0 and rightSensor.value() == 1): # 右輪
                valR += 1
                flagR = 1
            if(flagR == 1 and rightSensor.value() == 0):
                valR += 1
                flagR = 0
                
            now_time = time.ticks_ms()  # 更新現在時間(毫秒)
        
        l = valL/d_time                 # 計算左輪單位速度
        r = valR/d_time                 # 計算右輪單位速度
      
        if(l<=lRotating):      
            speedL += 1
        if(l>=lRotating + 0.02):      
            speedL -= 1      
        if(r<=rRotating):      
            speedR += 1
        if(r>=rRotating + 0.02):      
            speedR -= 1
        
        if(speedL>100):
            speedL = 100
        if(speedL<0):
            speedL = 0      
        if(speedR>100):
            speedR = 100
        if(speedR<0):
            speedR = 0
            
        lDirection = 1   # -1為後退、1為前進、0為停止
        rDirection = 1   # -1為後退、1為前進、0為停止
        
        if(mode == 'forward'):
            lDirection = 1
            rDirection = 1
        elif(mode == 'backward'):
            lDirection = -1
            rDirection = -1                   
        elif(mode == 'stop'):
            lDirection = 0
            rDirection = 0
            speedL = 0
            speedR = 0
        elif(mode == 'left'):
            lDirection = -1
            rDirection = 1
        elif(mode == 'right'):
            lDirection = 1
            rDirection = -1
            
        self.move(lDirection*(speedL),rDirection*(speedR))    
        
        valL = 0
        valR = 0
        
    def avoidTimeout(self):
        self.move(self.lNowSpeed,self.rNowSpeed)