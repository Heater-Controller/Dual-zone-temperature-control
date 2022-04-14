import time 
from machine import Timer 
from control_test import *
from time import sleep 

# Values that needs to come from learning algorithm and user 
t1 = 8
t2 = 10 
t3= 15  
tdss = 76

# Initial calculations to get time values 
temp_value = recieve_temp_data()

#Check that all sensors are working 
while sensor_value_check(temp_value) == "False":    
    temp_value = recieve_temp_data()
    
tT = calcuate_tT(t1, t2, t3)
tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])
#tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  
tind = calculate_tind(tdss, tss1)
tTotal = calculate_tTotal(tind, tT)
 
#Initialize tTotal timer interupt to achieve desired temperature 
#tTotal_timer = Timer(4)
#tTotal_timer.init(mode = Timer.ONE_SHOT, period = tTotal * 1000, callback = tTotal_timer_callback)

#Initialize tTotal timer interupt to achieve desired temperature 
tTotal_timer = Timer(4)
tTotal_timer.init(mode = Timer.PERIODIC, period = 30 * 60000, callback = data_gathering_callback)


# Begin the control 
#relay_status = "off"
#send_relay_signal(relay_status, relays)    

while True:
    

    temp_value = recieve_temp_data()
    tss1 = calculate_tss(temp_value[0], temp_value[1], temp_value[2])
    #tss2 = calculate_tss(temp_value[3], temp_value[4], temp_value[5])  
    temp_control_check = check_temp(tdss, tss1, control_signal)
    
    """
    if temp_control_check == "no":
         
        relay_status = "off"
        send_relay_signal(relay_status, relays)
        
    elif temp_control_check == "yes":
        
        relay_status == "on"
        send_relay_signal(relay_status, relays)

        time.sleep(tT) # wait for the temperature to increase by 1 with tT
        
        relay_status == "off"
        send_relay_signal(relay_status, relays)     
    """
    send_relay_signal_test(len(data), relays)
    
    print("Temperature value: " + str(temp_value))
    print("Tss1 value: " + str(tss1))
    #print("Tss2 value: " + str(tss2))
        
