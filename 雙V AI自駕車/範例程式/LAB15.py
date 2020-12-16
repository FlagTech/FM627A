import network
import ESP8266WebServer                 
import wemotor
from machine import I2C,Pin
import time

result = ''     # 網頁接收到的值
move = False    # 車子是否開始動

turn_time = 0   # 開始轉彎的時間

motor = wemotor.Motor()

# 處理 /Race 指令的函式
def handleCmd(socket, args):            
    global result, turn_time
    
    # 檢查是否有 output 參數
    if 'output' in args:                
        result = args['output']
        turn_time = time.ticks_ms()
        ESP8266WebServer.ok(socket, "200", "OK")   
    else:
        ESP8266WebServer.err(socket, "400", "ERR") 

LED=Pin(2,Pin.OUT,value=1)  

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
ap.config(essid='LAB15-'+str(sta.ifconfig()[0]))  

while True:
    ESP8266WebServer.handleClient()            
    motor.avoidTimeout()                       
    # 如果接收到 A 且車子還沒開始動
    if(result == 'A' and move == False):
        move = True   # 開始移動
        
    if(move == True):
        motor.constantSpeed('forward',0.02,0.02)
        
        # 如果接收到 L
        if result == 'L':
            # 如果還沒轉 1 秒
            while (time.ticks_ms() - turn_time) <= 1000:
                # 定速左轉
                motor.constantSpeed('left',0.02,0.02)
                
            motor.move(0,0)
            time.sleep(0.8)           
        # 如果接收到 R   
        elif result == 'R':
            # 如果還沒轉 1 秒
            while (time.ticks_ms() - turn_time) <= 1000:
                # 定速右轉
                motor.constantSpeed('right',0.02,0.02)
                
            motor.move(0,0)
            time.sleep(0.8)
        # 如果接收到 B    
        elif result == 'B':
            motor.move(0,0)     # 避免前傾
            time.sleep(0.8)
            turn_time = time.ticks_ms()
            # 如果還沒轉 1 秒
            while (time.ticks_ms() - turn_time) <= 1000:
                # 定速後退
                motor.constantSpeed('backward',0.02,0.02)
                
            motor.move(0,0)
            time.sleep(0.8)
        # 如果接收到 S    
        elif result == 'S':
            motor.constantSpeed('stop',0,0)
            move = False
        result = ''
