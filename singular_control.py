import time 
from machine import Timer 
from control_test import *

# Values that needs to come from learning algorithm and user 
t1 = 8
t2 = 10 
t3= 15  
tdss = 76
triangle = [1,2,4]

# Initial calculations to get time values 
temp_value = recieve_temp_data()

#Check that all sensors are working 
while sensor_value_check(temp_value) == "False":    
    temp_value = recieve_temp_data()

tT = calcuate_tT(t1, t2, t3)
tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
tind = calculate_tind(tdss, tss)
tTotal = calculate_tTotal(tind, tT)
 
#Initialize tTotal timer interupt to achieve desired temperature 
tTotal_timer = Timer(4)
tT_timer = Timer(2)
tTotal_timer.init(mode = Timer.ONE_SHOT, period = tTotal * 1000, callback = tTotal_timer_callback)

# Begin the control 
relay_status = "on"
send_relay_signal(relay_status, relays, triangle)    

def tT_timer_callback(t):
    
    relay_status = "hard_turn_off"
    send_relay_signal(relay_status, relays, triangle)
    
while True:
    
    temp_value = recieve_temp_data()
    tss = calculate_tss(temp_value[0], temp_value[1], temp_value[2])  
    temp_control_check = check_temp(tdss, tss, control_signal)
    
    if temp_control_check == "above":
         
        relay_status = "hard_turn_off"
        send_relay_signal(relay_status, relays, triangle)
        
    elif temp_control_check == "below":
        
        relay_status == "soft_turn_on"
        send_relay_signal(relay_status, relays, triangle)

        # wait for the temperature to increase by 1 with tT 
        tT_timer.init(mode = Timer.ONE_SHOT, period = tT * 60000, callback = tT_timer_callback)

    elif temp_control_check == "within":

        relay_status == "no_signal"
        send_relay_signal(relay_status, relays, triangle)
