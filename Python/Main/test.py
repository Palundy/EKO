from Classes.MS import MS
from Classes.TMCL import TMCL
from Classes.ICF02 import ICF02
import numpy as np
import time
import csv

from Classes.Series.MS80S import MS80S


# Initialize connection with motor
motor = TMCL("COM3")

# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS(MS80S ,"COM4", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)

# Initialize connection with the test sensor
test_sensor = MS(MS80S, "COM4", 2, used_addresses)
while (test_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(test_sensor.modbus_address)


ICF02.quick_profile_scan(ref_sensor, motor)