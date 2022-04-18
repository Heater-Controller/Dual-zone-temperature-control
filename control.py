## This module contains functions required for the control algorithm 

import network
from esp import espnow


#Adding components to master's communication protocol
def add_peer(comp_list):
    
    for peers in comp_list:
        e.add_peer(comp_list[peers])

global relay_status
global control_signal

# A WLAN interface must be active to send()/recv()
w0 = network.WLAN(network.STA_IF)
w0.active(True)

# ESP protocol initalization
e = espnow.ESPNow()
e.init()

# MAC addresses of temperature sensors' wifi interfaces
temp_sensors = { 'temp_sensor_1' : b'\x94\x3c\xc6\x6d\x17\x70', 'temp_sensor_2' : b'\x94\x3c\xc6\x6d\x1b\x68',
                 'temp_sensor_3' : b'\x94\x3c\xc6\x6d\x27\x14', 'temp_sensor_4' : b'\x94\x3c\xc6\x6d\x15\xfc',
                 'temp_sensor_5' : b'\x94\x3c\xc6\x6d\x27\x7c', 'temp_sensor_6' : b'\x94\x3c\xc6\x6d\x1f\x1c'}

# MAC addresses of relays' wifi interfaces
relays = {'relay_1' : b'\x94\x3c\xc6\x6d\x15\x40', 'relay_2' : b'\x94\x3c\xc6\x6d\x29\xd4', 
          'relay_3' : b'\x94\x3c\xc6\x6d\x14\x74', 'relay_4' : b'\x94\x3c\xc6\x6d\x29\xec'}

# Adding temperature sensors and relays to master's communication protocol
add_peer(temp_sensors)
add_peer(relays)
# Fucntion that calcuate tss, which is the measured temperature at a special spot
def calculate_tss(temp1, temp2, temp3):
    
    tss = (temp1 + temp2 + temp3)/3
    return tss


# Fucntion that calcuate tind, which is the amount by which temperature has to
# increase to reach desired value
def calculate_tind(tdss, tss):
    
    tind = tdss - tss
    return tind


# Fucntion that calcuate tT, which is the superpossed time it takes the heater to 
# increase the temperature of a special spot by 1
def calcuate_tT(t1, t2, t3):
    
    tT = (t1 * t2 * t3) / ((t1 * t2) + (t2 * t3) + (t1 *t3))
    return tT


 # Fucntion that calcuate tTotal, which is the total time required to reach a special
 # spot desired temperature
def calculate_tTotal(tind, tT):
    
    tTotal = tind * tT
    return tTotal


# Function gives sensors specific names on the basis of their converted integer addresses
def name_sensor(int_val):
    
    if (int_val == 162988747986800):
        temp_sensor_name = "sensor 1"

    if (int_val == 162988747987816):
        temp_sensor_name = "sensor 2"
        
    if (int_val == 162988747990804):
        temp_sensor_name = "sensor 3"
    
    """
    if (int_val == ):
        temp_sensor_name = "sensor 4"
        
    if (int_val == ):
        temp_sensor_name = "sensor 5"
        
    if (int_val == ):
        temp_sensor_name = "sensor 6"
    """
    return temp_sensor_name   

## Function that assign a sent temperature to the particular sensor number that sent it 
def get_temp(sensor_name, sensor_data):
    
    temp_value = [0,0,0,0,0,0]
    
    if sensor_name == 'sensor 1':
        temp_value[0] = sensor_data
    
    if sensor_name == 'sensor 2':
        temp_value[1] = sensor_data
        
    if sensor_name == 'sensor 3':
        temp_value[2] = sensor_data
        
    if sensor_name == 'sensor 4':
        temp_value[3] = sensor_data
        
    if sensor_name == 'sensor 5':
        temp_value[4] = sensor_data
        
    if sensor_name == 'sensor 6':
        temp_value[5] = sensor_data
    
    return temp_value

# Function to abstract relay names 
def get_relay(dict):
    return dict.keys()


def check_temp(tdss, tss, control_signal):
    
    if (tdss - tss) > 1 and control_signal == "on":
        return "yes"
    
    elif (tss - tdss) > 1 and control_signal == "on":
        return "no"
    
    else: 
        return "control off"
  
    
# Function To recive data from temperature sensors and save them in accordance to
# The temperature sensor that sent it 
def recieve_temp_data():
   
    host, msg = e.irecv()   
    
    if msg: # msg == None if timeout in irecv()
        
        host_conv_val = int.from_bytes(host, "big")
        sensor_name = name_sensor(host_conv_val)
        
        try:
            sensor_data = int(msg.decode("utf-8"))/100000
        except ValueError:
            pass
        
        temp_value = get_temp(sensor_name, sensor_data)
        print(sensor_name + ": " + int(sensor_data))
        
        return temp_value
         
# Function to send relay signal with the use of the relay status      
def send_relay_signal(status, relays):
    
    if status == "on": 

        e.send(relays['relay_1'], str(1), True)
        e.send(relays['relay_1'], str(1), True)
        e.send(relays['relay_1'], str(1), True)
    
    elif status == "off": 
         
        e.send(relays['relay_1'], str(0), True) 
        e.send(relays['relay_2'], str(0), True)
        e.send(relays['relay_3'], str(0), True)
        
# Function that sets the relay status to off when tTotal is done
def tTotal_timer_callback(t):  
     
    relay_status = "off"   
    control_signal = "on"
    send_relay_signal(relay_status, relays)
    

def cel_to_fah(tc):
    tf = (9/5) * tc + 32
    tfs = str("%.2f" % tf)
    t1 = int(tfs[3])
    t2 = int(tfs[4])
    if (t1 >= 7 and t2 >= 5):
        tf = math.ceil(tf)
    else:
        tf = math.floor(tf)
    return tf

