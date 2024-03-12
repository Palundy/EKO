from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import serial

import time
from TMCL import TMCL

# MAX DISTANCE 310mm
max_distance = 310
step_size = 5

# OFFSETS
# x_offset = 35mm
# y_offset = 40mm


# Generating the prefix for the command to turn 1mm
mm_rotation = int(TMCL.FULL_ROTATION / 4)
mmStep = TMCL.CLOCKWISE * mm_rotation




# Initialize a sensor on port COM5
addresses_used = []

# Connect with first sensor
sensor_0 = MS("COM4", 3, addresses_used)
while (sensor_0.is_ready == False):
    time.sleep(1)
addresses_used.append(sensor_0.modbus_address)



x = 27
Overwrite = False

# Open the .csv file
filename = f"measurement_height_scan_x{x}.csv"

with open(filename, "w", newline="") as file:
    writer = csv.writer(file)

    current_distance = 0
    turn_direction = -1 # Clockwise   
        
    
    # Connect with the driver
    with serial.Serial("COM3", baudrate=9600, timeout=1) as s:

        while (abs(current_distance) <= 300) and Overwrite == False:

            # Read out the pyranometer
            irr = sensor_0.compensated_irradiance()

            # Retrieve the current position
            posCmd = TMCL.generateCommand(
                TMCL.COMMAND_GET_AXIS_PARAMETER,
                0,
                TMCL.AXIS_PARAMETER_ACTUAL_POSITION
            )
            s.write(posCmd)
            time.sleep(0.2)


            # Log the data
            data = [x, abs(current_distance), irr, 0]
            writer.writerow(data)
            print(data)

            # Optional: Flush the file to ensure data is written.
            file.flush()



            stepCmd = TMCL.generateCommand(
                TMCL.COMMAND_MOVE_TO_POSITION,
                mmStep * step_size * turn_direction,
                TMCL.TYPE_RELATIVE
            )

            # Update the position of the sensor
            s.write(stepCmd)
            time.sleep(1.1)
            sReply = s.readline()
            if sReply:
                # Update the position ticker
                current_distance += step_size * turn_direction                

                


        # Return to the starting position
        print("Returning to home")
        stepCmd = TMCL.generateCommand(
            TMCL.COMMAND_MOVE_TO_POSITION,
            mmStep * 303 * 1,
            TMCL.TYPE_RELATIVE
        )
        s.write(stepCmd)

        # stepCmd = TMCL.generateCommand(
        #     TMCL.COMMAND_SET_AXIS_PARAMETER,
        #     2047,
        #     TMCL.AXIS_PARAMETER_TARGET_MAXIMUM_POSITIONING_SPEED
        # )
        # s.write(stepCmd)


    file.flush()
