import network
import ESP8266WebServer                
import wemotor
from machine import I2C,Pin

motor = wemotor.Motor()

# 左轉
def left():
    motor.move(0,50)

# 右轉
def right():
    motor.move(50,0)

# 處理 /Race 指令的函式
def handleCmd(socket, args):            
    # 檢查是否有 output 參數
    if 'output' in args:                
        if args['output'] == 'L':   # 若 output 參數值為 'L'
            left()                  # 左轉
        elif args['output'] == 'R': # 若 output 參數值為 'R'
            right()                 # 右轉
        ESP8266WebServer.ok(socket, "200", "OK")   
    else:
        ESP8266WebServer.err(socket, "400", "ERR") 
   

LED = Pin(2,Pin.OUT,value=1)  

sta = network.WLAN(network.STA_IF)         
sta.active(True)                           
sta.connect('無線網路名稱', '無線網路密碼') 

while not sta.isconnected():           
    pass

LED.value(0)               

ESP8266WebServer.begin(80)                   
ESP8266WebServer.onPath("/Race",handleCmd)        
print("伺服器位址：" + sta.ifconfig()[0])    

ap = network.WLAN(network.AP_IF) 
ap.active(True)
ap.config(essid='LAB10-'+str(sta.ifconfig()[0]))  

while True:
    ESP8266WebServer.handleClient()       
    motor.avoidTimeout()                  