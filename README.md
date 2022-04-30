# Dual-zone temperature control

**Project Description** : Code of a prototype that de-risk the dual zone temperature in the same room engineering challenge.

**How to Install and Run the Project** : 

![Hardware](https://github.com/JuanDavidGA/Dual_zone_temperature_control/blob/main/Hardware%20level.jpg)

Hardware consists of: 
*  11 ESP microcontrollers
*  6 temperature sensors
*  4 relays
*  4 heaters

![topology](https://github.com/JuanDavidGA/Dual_zone_temperature_control/blob/main/Topology.jpg)

It is important to stick to the setup: 
*  3 temperature sensors surrounding each special spot 
*  1 heater per wall

![redzone](https://github.com/JuanDavidGA/Dual_zone_temperature_control/blob/main/Red%20zone.png)

Important notes:  
*  Zone can be any size 
*  Special spot can not be located in the red zone

**How to Use the Project** :
<ol><li>Down load the ESPnow bin file on every ESP</li><li>Upload heater control code to the main/server ESP</li><li>Upload sensor_node code in the 6 EPS temperature nodes</li><li>Upload realy_node code in the 4 EPS relay nodes</li><li> 
    
## Useful References
**References for the Temperature Sensor:**
    
    Connections and Code -> https://randomnerdtutorials.com/micropython-ds18b20-esp32-esp8266/ 
    
    More code -> https://RandomNerdTutorials.com 
    
    Sensor Datasheet -> https://cdn-shop.adafruit.com/datasheets/DS18B20.pdf 
    
**Useful Code Snippets for the Temperature Sensor:**
    
    # Creates a ds18x20 object called temp_sensor on the sensor_pin defined earlier
    temp_sensor = ds18x20.DS18X20(onewire.OneWire(sensor_pin))
    
    # Scans for the DS18B20 sensors and saves the address found... returns a list with the address
    DS18B20_address = temp_sensor.scan()
        
    # Needed everytime we want to read the temp
    temp_sensor.convert_temp() 
    time.sleep_ms(750) # Delay of 750 ms to give enough time to convert the temperature
        
    # Return the temperature in Celcius
    temp_sensor.read_temp(DS18B20_address[0]) 

**References for the SD Card Module:**
    
    os for controlling the filesystem -> https://docs.micropython.org/en/latest/esp8266/tutorial/filesystem.html
    
    sd library with micropython -> https://learn.adafruit.com/micropython-hardware-sd-cards/micropython
    
    file read, write, etc -> https://www.pythontutorial.net/python-basics/python-write-text-file/
    
    hardware connections -> https://learn.adafruit.com/micropython-hardware-sd-cards/micropython?view=all

**Useful Code Snippets for the SD Card Module:**
    
    spi = machine.SPI(1, sck=machine.Pin(14), mosi=machine.Pin(13), miso=machine.Pin(12))
    #sck in the ESP is CLK on the SD Card Module
    #mosi or Pin(13) in the ESP is DI on the SD Card Module 
    #miso or Pin(12) in the ESP is DO on the SD Card Module  
    #GPIO Pin(18) is cs on the SD Card Module
        
    # Makes an SD card object  
    sdcard = sdcard.SDCard(spi, cs)
    # Makes the SD card the new root filesystem 
    vfs = os.VfsFat(sdcard)
    os.mount(vfs, "/sd")
