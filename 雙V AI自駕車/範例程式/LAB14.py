import network
import ESP8266WebServer                 
import wemotor
from machine import I2C,Pin
import time

motor = wemotor.Motor()         

def handleCmd(socket, args):         

    if 'output' in args:                 
        if args['output'] == 'L':    
            motor.move(0,40)         # 左轉
            time.sleep(1.5)
            motor.move(0,0)
            
        elif args['output'] == 'R':  
            motor.move(40,0)         # 右轉
            time.sleep(1.5)
            motor.move(0,0)
            
        elif args['output'] == 'F':
            motor.move(40,40)        # 直走
            time.sleep(1.5)
            motor.move(0,0)

        ESP8266WebServer.ok(socket, "200", "OK")   
    else:
        ESP8266WebServer.err(socket, "400", "ERR") 

LED = Pin(2,Pin.OUT,value=1)  

sta = network.WLAN(network.STA_IF)
sta.active(True)   
sta.connect('無線網路名稱', '無線網路密碼')     
while(not sta.isconnected()):
    pass

LED.value(0)                

ESP8266WebServer.begin(80)                      
ESP8266WebServer.onPath("/Race",handleCmd)      
print("伺服器位址：" + sta.ifconfig()[0])        

ap = network.WLAN(network.AP_IF) 
ap.active(True)
ap.config(essid='LAB14-'+str(sta.ifconfig()[0]))  

while True:
    ESP8266WebServer.handleClient()       
    motor.avoidTimeout()                  