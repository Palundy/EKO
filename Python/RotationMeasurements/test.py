from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import serial

import time
from TMCL import TMCL

# Initialize connection with motor
motor = TMCL("COM3")

# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS("COM5", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)


# Initialize connection with the test sensor
test_sensor = MS("COM5", 3, used_addresses)
while (test_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(test_sensor.modbus_address)



# Set the amount of measurements
amount_of_measurements = 5

# Retrieve the starting position for added check
begin_pos = motor.actual_position()


# Calculate the step size
half_cw = TMCL.HALF_ROTATION * TMCL.GEAR_RATIO * TMCL.CLOCKWISE
quarter_ccw = TMCL.QUARTER_ROTATION * TMCL.GEAR_RATIO * TMCL.COUNTER_CLOCKWISE


# Rotate a quarter CLOCKWISE
motor.relative_rotation(quarter_ccw)
print("Turned a quarter clockwise")

print(f"Performing {amount_of_measurements} irradiance measurements:")
for i in range(amount_of_measurements):
    irradiance = sensor.compensated_irradiance()
    print(f"Measurement {i + 1}: {irradiance} W/m²")


print("Turning 180° for counter-measurements")
motor.relative_rotation(half_cw)
print("Turned to counter-measurements position")
        

print(f"Performing {amount_of_measurements} irradiance measurements:")
for i in range(amount_of_measurements):
    irradiance = sensor.compensated_irradiance()
    print(f"Measurement {i + 1}: {irradiance} W/m²")

print("Turning back to home position")
motor.relative_rotation(quarter_ccw)
print("Done!")


# Retrieving final position
end_pos = motor.actual_position()
print(f"Beginning position was: {begin_pos}, and the final position is: {end_pos}")


