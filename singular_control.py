import time 
from machine import Timer 
from control import *

# Values that comes from the user 
tdss = 76
triangle = [1,2,4]
current_status = [0,0,0,0,0]

# Initial calculations to get time values 
temp_value = recieve_temp_data()

#Check that all sensors are working 
while sensor_value_check(temp_value) == "False":    
    temp_value = recieve_temp_data()

#tT = calcuate_tT(t1, t2, t3)
tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
tind = calculate_tind(tdss, tss)
#tTotal = calculate_tTotal(tind, tT)
 
#Initialize tTotal timer interupt to achieve desired temperature 
#tTotal_timer = Timer(4)
#tT_timer = Timer(2)
#tTotal_timer.init(mode = Timer.ONE_SHOT, period = tTotal * 1000, callback = tTotal_timer_callback)

# Begin the control 
relay_status = "on"
current_status = send_relay_signal(relay_status, current_status, triangle)    
temp_control_check = "Desired temperature not reached"

#def tT_timer_callback(t):
    
#    relay_status = "hard_turn_off"
#    send_relay_signal(relay_status, triangle)

while tdss != tss:

    temp_value = recieve_temp_data()
    tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    print("Temp in desired spot 1 = " + str(tdss) + " - Tss value: " + str(tss) +  "=> " + temp_control_check)

   
while True:
    
    temp_value = recieve_temp_data()
    tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    temp_control_check = check_temp(tdss, tss)
    
    if temp_control_check == "within":

        relay_status = "no_signal"
        current_status = send_relay_signal(relay_status, current_status, triangle)
        
    elif temp_control_check == "above":
         
        relay_status = "hard_turn_off"
        current_status = send_relay_signal(relay_status, current_status, triangle)    

        
    elif temp_control_check == "below":
        
        relay_status = "soft_turn_on"
        current_status = send_relay_signal(relay_status, current_status, triangle)    


        # wait for the temperature to increase by 1 with tT 
        #tT_timer.init(mode = Timer.ONE_SHOT, period = tT * 60000, callback = tT_timer_callback)

    print("Temperature value: " + str(temp_value))
    print("Temp in desired spot 1 = " + str(tdss) + " - Tss value: " + str(tss) +  " => " + 
    temp_control_check + ", Signal = " + relay_status + ", Hard turn off = " + str(current_status[4]))

