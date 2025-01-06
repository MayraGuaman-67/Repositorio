import network
import espnow
import machine
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from machine import Pin, SoftI2C
from time import sleep

S = network.WLAN(network.STA_IF)
S.active(True)
S.disconnect()

E = espnow.ESPNow()
E.active(True)

I2C_ADDR = 0x27
totalRows = 4
totalColums = 20

i2c = SoftI2C(scl=Pin(22), sda=Pin(21),freq=4000000)
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColums)

lcd.clear()
lcd.move_to(0,1)
lcd.putstr("Lcd On.")
    

while True:
    host, msg = E.recv() 
    if msg:  
        if msg == b'ledOn':
            print("lcd prendida")
            lcd.clear()
            lcd.putstr("") #Nombre 1
            lcd.move_to(0,1)
            for i in range(11):
                lcd.putstr(str(i))
                lcd.move_to(1,1)
                sleep(0.3)
                if i == 10:
                    lcd.move_to(0,3)
                    lcd.putstr("") #Nombre 2
                    sleep(2)
                    
        elif msg == b'ledOff':
            print("led apagado")
            lcd.clear()
            lcd.putstr("Lcd On.")
            lcd.move_to(0,1)
        else:
            print(f"Mensaje desconocido {msg}") 
