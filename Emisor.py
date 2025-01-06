import network
from machine import Pin
import espnow
import utime


sta = network.WLAN(network.STA_IF)
sta.active(True)
sta.disconnect()


EN = espnow.ESPNow()
EN.active(True)

mac_emisor= b'Direccion Mac del ESP receptor'
EN.add_peer(mac_emisor)

button_pin = Pin(23, Pin.IN, Pin.PULL_UP)


last_button_state=1
debounce_delay=50

while True:
    
    current_button_state =button_pin.value()

    if current_button_state!=last_button_state:
        if current_button_state == 0:
            message = b'ledOn'
            print(f"Sending command : {message}")
            EN.send(message)
        else:
            message = b'ledOff'
            print(f"Sending command : {message}")
            EN.send(message)
           
    last_button_state = current_button_state
