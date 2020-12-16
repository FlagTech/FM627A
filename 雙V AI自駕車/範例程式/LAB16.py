import network
import ESP8266WebServer                
import wemotor
from machine import I2C,Pin
import time

motor = wemotor.Motor()                 

def handleCmd(socket, args):            
    
    adj = 0                         # 調整速度
    lSpeed = 0
    rSpeed = 0
    
    if 'output' in args:                 
        if args['output'] == 'L':   # 若 output 為 'L'
            lSpeed = 15
            rSpeed = 25 
        elif args['output'] == 'R': # 若 output 為 'R'
            lSpeed = 25
            rSpeed = 15
        elif args['output'] == 'BL':
            lSpeed = 0
            rSpeed = 25 
        elif args['output'] == 'BR':
            lSpeed = 25
            rSpeed = 0
        elif args['output'] == 'F':
            lSpeed = 25
            rSpeed = 25
        elif args['output'] == 'S':
            lSpeed = 0
            rSpeed = 0
        if(args['output'] != 'S'):
            lSpeed = lSpeed + adj
            rSpeed = rSpeed + adj
        
        if(lSpeed<0):
            lSpeed = 0
        if(rSpeed<0):
            rSpeed = 0
        if(lSpeed>100):
            lSpeed = 100
        if(rSpeed>100):
            rSpeed = 100
            
        motor.move(lSpeed,rSpeed)         
            
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
ap.config(essid='LAB16-'+str(sta.ifconfig()[0]))  

while True:
    ESP8266WebServer.handleClient()       
    motor.avoidTimeout()                 

