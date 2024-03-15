from MS import MS
from TMCL import TMCL
import numpy as np
import time
import csv


# Initialize connection with motor
motor = TMCL("COM3")

# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS("COM8", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)

# Retrieve the output voltage, the raw irr and comp. irr
ov = ref_sensor.output_voltage()
ri = ref_sensor.raw_irradiance()
ci = ref_sensor.compensated_irradiance()

print(ov, ri, ci)