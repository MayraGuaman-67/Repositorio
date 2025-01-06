import network

wifi = network.WLAN(network.STA_IF)

wifi.active(True)

mac = wifi.config('mac')

# Imprimir la dirección MAC en formato hexadecimal
print(':'.join(['{:02x}'.format(b) for b in mac]))
