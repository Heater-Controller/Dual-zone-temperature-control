## This module contains functions required for the control algorithm 

import network
from esp import espnow
import math


global current_status
current_status = [0,0,0,0,0]
temp_value = [0,0,0,0,0,0]


#Adding components to master's communication protocol
def add_peer(comp_list):
    
    for peers in comp_list:
        e.add_peer(comp_list[peers])


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
    
    temp_sensor_name = ""
    if (int_val == 162988747986800):
        temp_sensor_name = "sensor 1"

    if (int_val == 162988747987816):
        temp_sensor_name = "sensor 2"
        
    if (int_val == 162988747990804):
        temp_sensor_name = "sensor 3"
    
    if (int_val == 162988747986428):
        temp_sensor_name = "sensor 4"
        
    if (int_val == 162988747990908):
        temp_sensor_name = "sensor 5"
        
    if (int_val == 162988747988764):
        temp_sensor_name = "sensor 6"

    return temp_sensor_name   


## Function that assign a sent temperature to the particular sensor number that sent it 
def get_temp(sensor_name, sensor_data):
        
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


def check_temp(tdss, tss):
    
    if (tdss - tss) >= 1: 
    #means the temperature is below treashhold
        return "Below"
     
    elif (tss - tdss) >= 1:
    #means the temperature is above treashhold
        return "Above"
    
    elif (tss - tdss) < 1 and (tdss - tss) < 1:
    #means the temperature is above treashhold
        return "Within"
    
    else: 
        return "Desired temperature not reached"
  

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
        
        temp_value_list = get_temp(sensor_name, sensor_data)
        print(sensor_name + ": " + int(sensor_data))
        
        return temp_value_list
         
    
# Function to send relay signal with the use of the relay status      
def send_relay_signal(status, relays, triangle):
    
    acknowledgements = [] # Keeps track of which relays acknowledged they received a signal 
    
    if status == "on": 

        acknowledgements.append(    e.send(relays['1'], str(1), True)    ) # True if the message was received ... False if it was not received
        acknowledgements.append(    e.send(relays['2'], str(1), True)    )
        acknowledgements.append(    e.send(relays['3'], str(1), True)    )
        acknowledgements.append(    e.send(relays['4'], str(1), True)    )
        
        acknowledgement_check( acknowledgements, relays, ['1', '2', '3', '4'], [str(1), str(1), str(1), str(1)] ) # acknowledgment and retransmission protocol 
        
        current_status = [1, 1, 1, 1, 0]
        
    elif status == "off": 
         
        acknowledgements.append(    e.send(relays['1'], str(0), True)    )
        acknowledgements.append(    e.send(relays['2'], str(0), True)    )
        acknowledgements.append(    e.send(relays['3'], str(0), True)    )
        acknowledgements.append(    e.send(relays['4'], str(0), True)    )
        
        acknowledgement_check( acknowledgements, relays, ['1', '2', '3', '4'], [str(0), str(0), str(0), str(0)] )
        
        current_status = [0, 0, 0, 0, 0]
 
    elif status == "soft_turn_on":
        
        if current_status[4] == 1: #Means hard turn_on is active
            
            acknowledgements.append(    e.send(relays[str(triangle[0])], str(1), True)    )
            acknowledgements.append(True) # *** Theoretically we do not need it but need to test first
            acknowledgements.append(True)
            acknowledgements.append(True)
            
            acknowledgement_check( acknowledgements, relays, [ str(triangle[0]), '2', '3', '4'], [str(1), str(0), str(0), str(0)] )
            # *** Theoretically can be this but need to test first  
            #acknowledgement_check( acknowledgements, relays, [ str(triangle[0])], [str(1)] )
                                        
            current_status[triangle[0] - 1] = 1

        else:
            
            for value in triangle:
                
                acknowledgements.append(    e.send(relays[str(value)], str(1), True)    ) 
                acknowledgements.append(    e.send(relays[str(value)], str(1), True)    )
                acknowledgements.append(    e.send(relays[str(value)], str(1), True)    )
                acknowledgements.append(True)
                
                acknowledgement_check( acknowledgements, relays, [ str(value), str(value), str(value), '4'], [str(1), str(1), str(1), str(0)] )
                # *** Theoretically can be this but need to test first  
                #acknowledgement_check( acknowledgements, relays, [ str(value), str(value), str(value)], [str(1), str(1), str(1)] )
                current_status[value - 1] = [1]

    
    elif status == "soft_turn_off":
        
        acknowledgements.append(    e.send(relays[str(triangle[0])], str(0), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)
        acknowledgements.append(True)
        
        acknowledgement_check( acknowledgements, relays, [ str(triangle[0]), '2', '3', '4' ], [str(0), str(0), str(0), str(0)] )
        
        current_status[triangle[0] - 1] = 0
                
    elif status == "hard_turn_off":
        
        for value in triangle:
            
            acknowledgements.append(    e.send(relays[str(value)], str(0), True)    )
            acknowledgements.append(    e.send(relays[str(value)], str(0), True)    )
            acknowledgements.append(    e.send(relays[str(value)], str(0), True)    )
            acknowledgements.append(True)
            
            acknowledgement_check( acknowledgements, relays, [ str(triangle[0]), '2', '3', '4' ], [str(0), str(0), str(0), str(0)] )
            
            current_status[value - 1] = [0]
        
        current_status[4] = 1
    
    elif status == "no_signal":
        current_status[4] = 0
     
     
# Function that sets the relay status to off when tTotal is done
#def tTotal_timer_callback(t):  
     
#    relay_status = "off"   
#    send_relay_signal(relay_status, relays)
    

# Function that we call when we finally reach tdss
def begin_control(relay_status):  
    send_relay_signal(relay_status, relays, [1,2,3])    


#Function that convert the celcius degree into fareneight
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


# Fucnction that make sure we gett all the sensor value before calculation
def sensor_value_check(temp_value):
    
    check = "True" 
    for value in temp_value:
        
         if value == 0:
             
            check = "False"
            break
    
    return check


# Fucnction that checks if the data was sent succesfully
# Can make this into a for loop later -> once it works well
def acknowledgement_check(_acknowledgements, relays, _relay_number, _commands):
    
    if _acknowledgements[0] == False: # Relay 1 acknowledgement was false -> the Relay did not receive the command
        print('-> Relay ' + str(_relay_number[0]) + ' did not receive anything')
        print('   The ESP will try to send 100 times before giving up if the relay does not acknowledge it received the ON/OFF command')
        
        ack = False
        count_acknowledgement_tries = 100
        
        while count_acknowledgement_tries > 1:
            ack = e.send(relays[_relay_number[0]], _commands[0], True)
            count_acknowledgement_tries -= 1
            
            if ack == True:
                e.send(relays[_relay_number[0]], _commands[0], True)
                break    
        
    if _acknowledgements[1] == False: # Relay 2 acknowledgement
        print('-> Relay ' + str(_relay_number[1]) + ' did not receive anything')
        print('   The ESP will try to send 100 times before giving up if the relay does not acknowledge it received the ON/OFF command')
        
        ack = False
        count_acknowledgement_tries = 100
        
        while count_acknowledgement_tries > 1:
            ack = e.send(relays[_relay_number[1]], _commands[1], True)
            count_acknowledgement_tries -= 1
            
            if ack == True:
                e.send(relays[_relay_number[1]], _commands[1], True)
                break
            
    if _acknowledgements[2] == False: # Relay 3 acknowledgement
        print('-> Relay ' + str(_relay_number[2]) + ' did not receive anything')
        print('   The ESP will try to send 100 times before giving up if the relay does not acknowledge it received the ON/OFF command')
        
        ack = False
        count_acknowledgement_tries = 100
        
        while count_acknowledgement_tries > 1:
            ack = e.send(relays[_relay_number[2]], _commands[2], True)
            count_acknowledgement_tries -= 1
           
            if ack == True:
                e.send(relays[_relay_number[2]], _commands[2], True)
                break
            
    if _acknowledgements[3] == False: # Relay 4 acknowledgement
        print('-> Relay ' + str(_relay_number[3]) + ' did not receive anything')
        print('   The ESP will try to send 100 times before giving up if the relay does not acknowledge it received the ON/OFF command')
        
        ack = False
        count_acknowledgement_tries = 100

        while count_acknowledgement_tries > 1:
            ack = e.send(relays[_relay_number[3]], _commands[3], True)
            count_acknowledgement_tries -= 1
            
            if ack == True:
                e.send(relays[_relay_number[3]], _commands[3], True)
                break
        
    return
