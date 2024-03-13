from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import serial

import time
from TMCL import TMCL


# Initialize a sensor on port COM5
addresses_used = []

# Connect with first sensor
sensor_0 = MS("COM4", 3, addresses_used)
while (sensor_0.is_ready == False):
    time.sleep(1)
addresses_used.append(sensor_0.modbus_address)



n_steps = 0

overwrite = False
overwrite_steps = 0
overwrite_steps_amount = 1

step_size = int(TMCL.FULL_ROTATION * TMCL.GEAR_RATIO * TMCL.CLOCKWISE / 32)


# Open the .csv file
timenow = int(time.time())  
filename = f"measurement_quick_scan_{timenow}.csv"

with open(filename, "w+", newline="") as file:
    writer = csv.writer(file)
    

    
    # Connect with the driver
    with serial.Serial("COM3", baudrate=9600, timeout=1) as s:

        while (abs(n_steps) < abs(TMCL.FULL_ROTATION * TMCL.GEAR_RATIO) and overwrite == False) or (overwrite and overwrite_steps <= overwrite_steps_amount):
            


            # Read out the pyranometer
            irr = sensor_0.compensated_irradiance()

            # Retrieve the current position
            posCmd = TMCL.generateCommand(
                TMCL.COMMAND_GET_AXIS_PARAMETER,
                0,
                TMCL.AXIS_PARAMETER_ACTUAL_POSITION
            )
            s.write(posCmd)
            time.sleep(.5)

            pos = TMCL.returnReplyValue(s.readline())
            this_time = time.time()

            # Log the data
            data = [pos, n_steps, irr, this_time]
            writer.writerow(data)
            print(data)

            # Optional: Flush the file to ensure data is written.
            file.flush()



            stepCmd = TMCL.generateCommand(
                TMCL.COMMAND_MOVE_TO_POSITION,
                step_size,
                TMCL.TYPE_RELATIVE
            )

            # Update the position of the sensor
            pos_updated = False
            while pos_updated == False:
                try:
                    s.write(stepCmd)
                    sReply = s.readline()
                    if sReply:
                        # Update the position ticker
                        n_steps += step_size
                        overwrite_steps += 1
                    
                    pos_updated = True
                    break
                except Exception as e:
                    continue
                
        time.sleep(2)
        # Reset to begin position
        stepCmd = TMCL.generateCommand(
            TMCL.COMMAND_MOVE_TO_POSITION,
            TMCL.FULL_ROTATION * TMCL.GEAR_RATIO * TMCL.COUNTER_CLOCKWISE,
            TMCL.TYPE_RELATIVE
        )
        s.write(stepCmd)
    
    file.flush()
