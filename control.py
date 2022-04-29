"""
    micropython module that contains functions and initialization required for the main control program.
    The program initialize the WLAN communication interface, the espnow protocole and set up all the 
    microcontroller addresses needed for the wireless communication of the system.  
"""

import network
from esp import espnow
import math

# Activates a WLAN interface to send and recieve
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
relays = {'1' : b'\x94\x3c\xc6\x6d\x15\x40', '2' : b'\x94\x3c\xc6\x6d\x29\xd4', 
          '3' : b'\x94\x3c\xc6\x6d\x14\x74', '4' : b'\x94\x3c\xc6\x6d\x29\xec'}

#Variable used to save read temperature
temp_value = [0,0,0,0,0,0]


"""
Description: 
    Function that adds components to master's communication protocol
Parameters:
    comp_list: List of relay and temperature sensor microcontroller mac addresses
Returns:
    N/A
Throws:
    N/A
"""
def add_peer(comp_list):
    
    for peers in comp_list:
        e.add_peer(comp_list[peers])


# Adding temperature sensors and relays to master's communication protocol
add_peer(temp_sensors)
add_peer(relays)

"""
Description: 
    Fucntion that calcuate tss, which is the measured temperature at a special spot
Parameters:
    temp1, temp2, temp3: 3 temperatrures from the temperature sensors surrounding a special spot
Returns:
    tss_to_fareingth: returns the calculatred tss value in fareneight
Throws:
    N/A
"""
def calculate_tss(temp1, temp2, temp3):
    
    tss = (temp1 + temp2 + temp3)/3
    tss_to_fareingth = cel_to_fah(tss) # Convert the calculated tss into fareneight 
    return tss_to_fareingth


"""
Description: 
    Function gives sensors specific names on the basis of their converted integer addresses
    int_values have been calculated according to the value returned by the sensor microcontroler 
    slaves when sending data to the master microcontroller. The sensors are then named accordingly.
Parameters:
    int_val: sensor host bitarray calcultated in integer
Returns:
    temp_sensor_name: returns the name of a sensor in a more readabe manner
Throws:
    N/A
"""
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


"""
Description: 
    Function that assign a sent temperature to the particular sensor number (in index number)  
    That sent it. This allows us to keep track of a particular sensor and the data it sent 
Parameters:
    sensor_name, sensor_data: sensor data along with the name of the sensor that sent it
Returns:
    temp_value: returns an array containning sensor values 
Throws:
    N/A
"""
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


"""
Description: 
    Function that checks for the temperature range and return the state of the 
    current temperature vs the desired temperature of a special spot. 
Parameters:
   tdss, tss: The desired temperature and the current temperature 
Returns:
    Function returns the state of the current temperature 
Throws:
    N/A
"""
def check_temp(tdss, tss):
    
    if (tdss - tss) >= 1: 
    #means the temperature is below treashhold
        return "below"
     
    elif (tss - tdss) >= 1:
    #means the temperature is above treashhold
        return "above"
    
    elif (tss - tdss) < 1 and (tdss - tss) < 1:
    #means the temperature is above treashhold
        return "within"
    
    else: 
        return "Desired temperature not reached"


"""
Description: 
    Function to recieve data from temperature sensors and save them in accordance to
    The temperature sensor that sent it 
Parameters:
   N/A
Returns:
    temp_value_list: returns a list of updated temperature data whenever new data is recieved 
Throws:
    ValueError: Ensures that a sensor bitarray value has been sent before the conversion to integer happens
"""
def recieve_temp_data():
   
    host, msg = e.irecv()  # Recieve data from sensors  
    
    if msg: # msg == None if timeout in irecv()
        
        host_conv_val = int.from_bytes(host, "big") # Converts bitarray host name to int value 
        sensor_name = name_sensor(host_conv_val) # Converts int host name to a string 
        
        try:
            sensor_data = int(msg.decode("utf-8"))/10000 # Converts bitarray sensor value to an integer
        except ValueError:
            pass
        
        temp_value_list = get_temp(sensor_name, sensor_data)
        print(sensor_name + ": " + str(sensor_data))
        
        return temp_value_list


"""
Description: 
    Function that sends a relay signal to the slave relay microcontroller to turn them ON or OFF. 
    The signal is the sent to an acknolegment function that resends the relay signal 100 until the 
    signal is received by the relay. 
Parameters:
   relay_status, current_status, triangle: The status we want the relay to be, the current status of 
                                           the heaters, and the heater triangle passing the relay status  
Returns:
    current_status: Returns the current status of the heaters  
Throws:
    N/A
"""    
def send_relay_signal(relay_status, current_status, triangle):
    
    acknowledgements = [] # Keeps track of which relays acknowledged they received a signal 
    
    if relay_status == "on": 

        acknowledgements.append(    e.send(relays['1'], str(1), True)    ) 
        acknowledgements.append(    e.send(relays['2'], str(1), True)    )
        acknowledgements.append(    e.send(relays['3'], str(1), True)    )
        acknowledgements.append(    e.send(relays['4'], str(1), True)    )
        
        acknowledgement_check( acknowledgements, relays, ['1', '2', '3', '4'], 
        [str(1), str(1), str(1), str(1)] ) # acknowledgment and retransmission protocol 
        
        current_status = [1, 1, 1, 1, 0]
        
    elif relay_status == "off": 
         
        acknowledgements.append(    e.send(relays['1'], str(0), True)    )
        acknowledgements.append(    e.send(relays['2'], str(0), True)    )
        acknowledgements.append(    e.send(relays['3'], str(0), True)    )
        acknowledgements.append(    e.send(relays['4'], str(0), True)    )
        
        acknowledgement_check( acknowledgements, relays, ['1', '2', '3', '4'], [str(0), str(0), str(0), str(0)] )
        
        current_status = [0, 0, 0, 0, 0]
 
    elif relay_status == "soft_turn_on":
        
        if current_status[4] == 1: #Means hard turn_on is active
            
            acknowledgements.append(    e.send(relays[str(triangle[0])], str(1), True)    )
            acknowledgements.append(True) # *** Theoretically we do not need it but need to test first
            acknowledgements.append(True)
            acknowledgements.append(True)
            
            acknowledgement_check( acknowledgements, relays, [ str(triangle[0]), '2', '3', '4'], [str(1), str(0), str(0), str(0)] )
            # *** Theoretically can be this but need to test first  
            #acknowledgement_check( acknowledgements, relays, [ str(triangle[0])], [str(1)] )
                                        
            current_status[(triangle[0] - 1)] = 1

        else:
            
            for value in triangle:
                
                acknowledgements.append(    e.send(relays[str(value)], str(1), True)    ) 
                current_status[(value - 1)] = 1
            
            acknowledgements.append(True)     
            acknowledgement_check( acknowledgements, relays, [ str(value), str(value), str(value), '4'], [str(1), str(1), str(1), str(0)] )
    
    elif relay_status == "soft_turn_off":
        
        acknowledgements.append(    e.send(relays[str(triangle[0])], str(0), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)
        acknowledgements.append(True)
        
        acknowledgement_check( acknowledgements, relays, [ str(triangle[0]), '2', '3', '4' ], [str(0), str(0), str(0), str(0)] )
        
        current_status[(triangle[0] - 1)] = 0
                
    elif relay_status == "hard_turn_off":
        
        for value in triangle:
            
            acknowledgements.append(    e.send(relays[str(value)], str(0), True)    )
            current_status[(value - 1)] = 0
        
        current_status[4] = 1
        acknowledgements.append(True) 
        acknowledgement_check( acknowledgements, relays, [ str(triangle[0]), '2', '3', '4' ], [str(0), str(0), str(0), str(0)] )
    
    elif relay_status == "no_signal":
        current_status[4] = 0
    
    return current_status


"""
Description: 
    Function that convert the celcius degree into fareneight
Parameters:
   tc: Temperature in celcius
Returns:
    tf: Temperature converted to fareneight
Throws:
    N/A
"""
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


"""
Description: 
    Fucnction that ensure we get all the sensor value before calculation
Parameters:
    temp_value: Array that contain all temperature
Returns:
    N/A
Throws:
    N/A
"""
def sensor_value_check(temp_value):
    
    check = "True" 
    for value in temp_value:
        
         if value == 0:
             
            check = "False"
            break
    
    return check


"""
Description: 
    Fucnction that checks if the data was sent succesfully
    Can make this into a for loop later -> once it works well
Parameters:
    _acknowledgements: Acknowledgment status to relays
    relays: microcontroller relay list 
    _relay_number: index of the relays 
    _commands: list of commands of relays 
Returns:
    Function returns the state of the current temperature 
Throws:
    N/A
"""
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
       

"""
Description: 
    Function that sends signal to relays to turn them ON 1 at the time.       
Parameters:
    heater: Determines which heater is ON or OFF
Returns:
    N/A
Throws:
    N/A
"""
def learning(heater):
        
    acknowledgements = [] # Keeps track of which relays acknowledged they received a signal 
    
    if heater == 0:
        
        acknowledgements.append(    e.send(relays['1'], str(0), True)    )
        acknowledgements.append(    e.send(relays['2'], str(0), True)    )
        acknowledgements.append(    e.send(relays['3'], str(0), True)    )
        acknowledgements.append(    e.send(relays['4'], str(0), True)    )
        acknowledgement_check( acknowledgements, relays, [ '1', '2', '3', '4' ], [str(0), str(0), str(0), str(0)] )
        
    elif heater == 1:
        acknowledgements.append(    e.send(relays['1'], str(1), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)
        acknowledgements.append(True)
        
        acknowledgement_check( acknowledgements, relays, ['1', '2', '3', '4'], [str(1), str(0), str(0), str(0)] )
       
        
    elif heater == 2:
        acknowledgements.append(    e.send(relays['2'], str(1), True)    )
        acknowledgements.append(    e.send(relays['1'], str(0), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)      
        acknowledgement_check( acknowledgements, relays, [ '2', '1', '3', '4' ], [str(1), str(0), str(0), str(0)] )
        
    elif heater == 3:
        acknowledgements.append(    e.send(relays['3'], str(1), True)    )
        acknowledgements.append(    e.send(relays['2'], str(0), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)  
        acknowledgement_check( acknowledgements, relays, [ '3', '2', '1', '4' ], [str(1), str(0), str(0), str(0)] )
        
    elif heater == 4:
        
        acknowledgements.append(    e.send(relays['4'], str(1), True)    )
        acknowledgements.append(    e.send(relays['3'], str(0), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)  
        acknowledgement_check( acknowledgements, relays, [ '4', '3', '1', '2' ], [str(1), str(0), str(0), str(0)] )
        
    elif heater == 5:
        
        acknowledgements.append(    e.send(relays['4'], str(0), True)    )
        acknowledgements.append(True)
        acknowledgements.append(True)
        acknowledgements.append(True)  
        acknowledgement_check( acknowledgements, relays, [ '4', '3', '1', '2' ], [str(0), str(0), str(0), str(0)] )
    
    elif heater == 6:
        
        acknowledgements.append(    e.send(relays['1'], str(1), True)    )
        acknowledgements.append(    e.send(relays['2'], str(1), True)    )
        acknowledgements.append(    e.send(relays['3'], str(1), True)    )
        acknowledgements.append(    e.send(relays['4'], str(1), True)    ) 
        acknowledgement_check( acknowledgements, relays, [ '1', '2', '3', '4' ], [str(1), str(1), str(1), str(1)] )