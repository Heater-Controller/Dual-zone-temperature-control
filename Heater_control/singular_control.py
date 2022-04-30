"""
    Main driver that controls temperature on a single spot. 
    The program begins by prompting the user to enter a desired temperature,
    then begins the learning phase by calibrating the triangle of heaters to find which 3 triangles has
    the biggest impact on the special spot. Finally, The program enters the control mode in the infinite 
    loop where it attemps to keep the current temperature as close to the desired temperature as possible 
    by controlling when heaters are ON or OFF. 
"""

from control import *

#Check that all sensors are sending data 
temp_value = recieve_temp_data()
while sensor_value_check(temp_value) == "False":    
    temp_value = recieve_temp_data()

#Calculate the current temperature
tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])

# Values that comes from the user 
tdss = int(input("Enter the desired temperature of special spot: "))

# Ensure the entered desired temperature is greater than the current temperature
while tdss < tss:

    tdss = int(input("The current temperatuure is higher than the desired temperature.\nPlease re-enter the desired temperature of the special spot: "))
    temp_value = recieve_temp_data()
    tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])

# determine the heater triangle 
triangle = [1,2,4]
current_status = [0,0,0,0,0]
 
# Begin the control 
relay_status = "on"
current_status = send_relay_signal(relay_status, current_status, triangle)    
temp_control_check = "Desired temperature not reached"

# Leaves the heaters on until the desired temperature is reached
while tdss != tss:

    temp_value = recieve_temp_data()
    tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    print("Temp in desired spot 1 = " + str(tdss) + " - Tss value: " + str(tss) +  "=> " + temp_control_check)

while True:
    
    #Monitoring change of temperature throughout the control
    temp_value = recieve_temp_data()
    tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    temp_control_check = check_temp(tdss, tss)
    
    #Send a no signal to the relay informing that we are in range
    if temp_control_check == "within":

        relay_status = "no_signal"
        current_status = send_relay_signal(relay_status, current_status, triangle)
    
    #Send a hard turn off signal to the relay informing that we are 
    # above and that all heaters needs to be turned off
    elif temp_control_check == "above":
         
        relay_status = "hard_turn_off"
        current_status = send_relay_signal(relay_status, current_status, triangle)    

    #Send a soft turn on signal to the relay informing that we are 
    # above and that all heaters needs to be turned on   
    elif temp_control_check == "below":
        
        relay_status = "soft_turn_on"
        current_status = send_relay_signal(relay_status, current_status, triangle)    

    print("Temperature value: " + str(temp_value))
    print("Temp in desired spot 1 = " + str(tdss) + " - Tss value: " + str(tss) +  " => " + 
    temp_control_check + ", Signal = " + relay_status + ", Hard turn off = " + str(current_status[4]))

