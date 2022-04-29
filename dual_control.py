"""
    Main driver that controls and maintain the temperature of a dual spot. 
    The program begins by prompting the user to enter the desired temperature of the two desired,
    then begins the learning phase by calibrating the triangle of heaters to find which 3 triangles has
    the biggest impact on the special spot. Finally, The program enters the control mode in the infinite 
    loop where it attemps to keep both temperature as close to the desired temperature as possible 
    by controlling when heaters are ON or OFF. 
"""

from control import *

#Check that all sensors are sending data 
temp_value = recieve_temp_data()
while sensor_value_check(temp_value) == "False":    
    temp_value = recieve_temp_data()

#Calculate the current temperatures
tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])
tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])

# Values that comes from the user 
tdss1 = int(input("Enter the desired temperature of special spot 1: "))
tdss2 = int(input("Enter the desired temperature of special spot 2: "))

# Ensure the entered desired temperature is greater than the current temperature
while tdss1 < tss1:

    tdss1 = int(input("The current temperatuure is higher than the desired temperature on this spot." + 
                      "\nPlease re-enter the desired temperature of the special spot 1: "))
    temp_value = recieve_temp_data()
    tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])
    
# Ensure the entered desired temperature is greater than the current temperature
while tdss2 < tss2:

    tdss2 = int(input("The current temperature is higher than the desired temperature on this spot." +
                      "\nPlease re-enter the desired temperature of the special spot 2: "))
    temp_value = recieve_temp_data()
    tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])

# determine the heater triangles
triangle1 = [1,2,4]
triangle2 = [3,4,2]
current_status = [0,0,0,0,0]

#Begin the control 
relay_status = "on"
temp_control_check1 = "Desired temperature not reached"
temp_control_check2 = "Desired temperature not reached"

# Leaves the heaters on until the desired temperature is reached
while tdss1 != tss1 and tdss2 != tss2:
    
    current_status = send_relay_signal(relay_status, current_status, triangle1)    
    temp_value = recieve_temp_data()
    tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  
    print("Temp in desired spot 1 = " + str(tdss1) + " - Tss1 value: " + str(tss1) +  " => " + temp_control_check1)
    print("Temp in desired spot 2 = " + str(tdss2) + " - Tss2 value: " + str(tss2) +  " => " + temp_control_check2)

while True:
    
    #Monitoring change of temperature throughout the control
    temp_value = recieve_temp_data()
    tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  

    # perform a temperature check to determinne which range we are in. 
    # Above, bellow or withim the desired temperature range 
    temp_control_check1 = check_temp(tdss1, tss1)
    temp_control_check2 = check_temp(tdss2, tss2)

    #Send a hard turn off signal to the relay informing that we are 
    # above and that all heaters needs to be turned off
    if temp_control_check1 == "above":
         
        relay_status = "hard_turn_off"
        current_status = send_relay_signal(relay_status, current_status, triangle1)    
    
    #Send a soft turn on signal to the relay informing that we are 
    # above and that all heaters needs to be turned on      
    elif temp_control_check1 == "below":
        
        relay_status = "soft_turn_on"
        current_status = send_relay_signal(relay_status, current_status, triangle1)    

    #Send a no signal to the relay informing that we are in range
    elif temp_control_check1 == "within":

        relay_status = "no_signal"
        current_status = send_relay_signal(relay_status, current_status, triangle1)    

    #Send a hard turn off signal to the relay informing that we are 
    # above and that all heaters needs to be turned off
    if temp_control_check2 == "above":
         
        relay_status = "hard_turn_off"
        current_status = send_relay_signal(relay_status, current_status, triangle2)    
    
    #Send a soft turn on signal to the relay informing that we are 
    # above and that all heaters needs to be turned on      
    elif temp_control_check2 == "below":
        
        relay_status = "soft_turn_on"
        current_status = send_relay_signal(relay_status, current_status, triangle2)    
       
    #Send a no signal to the relay informing that we are in range
    elif temp_control_check2 == "Within":
        
        relay_status = "no_signal"
        current_status = send_relay_signal(relay_status, current_status, triangle2)    

    print("Temperature value: " + str(temp_value))
    print("Temp in desired spot 1 = " + str(tdss1) + " - Tss1 value: " + str(tss1) +  " => " + 
        temp_control_check1 + ", Signal = " + relay_status + ", Hard turn off = " + str(current_status[4]))
    print("Temp in desired spot 2 = " + str(tdss2) + " - Tss2 value: " + str(tss2) +  " => " + 
        temp_control_check2 + ", Signal = " + relay_status + ", Hard turn off = " + str(current_status[4]))

        
        

