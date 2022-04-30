"""
micropython driver that control the relay power. This driver is slave to a master 
controler that sends a 1 or a 0 to turn the relay powe on or off. 
 
"""
import network
from esp import espnow
from machine import Pin

# Activates a WLAN interface to send and recieve
w0 = network.WLAN(network.STA_IF)
w0.active(True)

# Initializes Esp now protocol
e = espnow.ESPNow()
e.init()

master = b'\x94\x3c\xc6\x6d\x17\x48'   # MAC address of master's wifi interface
e.add_peer(master) # Add master as a wifi interface peer

# Microcontroller pin setup 
p = Pin(14,Pin.OUT)
p.value(0)

while True:

    host, msg = e.irecv() # Recieve data from master (host)
    
    if msg == None:  # msg == None if timeout in irecv()
        print('Did not receive anything')

    if msg: 
        command = int(msg.decode("utf-8")) # Convert bitarray into interger
    
        # Sends command to the ralay to turn it on and off
        if command == 1:                   
            p.value(1) 
       
        elif command == 0:
            p.value(0) 
    
