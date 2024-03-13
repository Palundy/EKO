from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time
import csv
import serial
import threading

import time
from TMCL import TMCL

def log_sensor_data(sensor_0):


    print("Logging shiz")

    # Open the .csv file
    filename = f"measurement_quick_scan_15.csv"
    
    with open(filename, "w+", newline="") as file:
        while True:
            try:
                writer = csv.writer(file)        
                # Read out the pyranometer
                irr = sensor_0.compensated_irradiance()

                # Retrieve the current position
                posCmd = TMCL.generateCommand(
                    TMCL.COMMAND_GET_AXIS_PARAMETER,
                    0,
                    TMCL.AXIS_PARAMETER_ACTUAL_POSITION
                )
                s.write(posCmd)
                time.sleep(.25)

                pos = TMCL.returnReplyValue(s.readline())
                this_time = time.time()

                # Log the data
                data = [pos, n_steps, irr, this_time]
                writer.writerow(data)
                print(data)

                # Optional: Flush the file to ensure data is written.
                file.flush()
            except KeyboardInterrupt:
                file.flush()
                return
    
    



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

step_size = -1 * int(TMCL.FULL_ROTATION * TMCL.GEAR_RATIO)

    
# Connect with the driver
with serial.Serial("COM3", baudrate=9600, timeout=1) as s:

    # Start sensor reading thread
    thread_1 = threading.Thread(target=log_sensor_data, args=(sensor_0,))
    thread_1.start()
    time.sleep(2)


    stepCmd = TMCL.generateCommand(
        TMCL.COMMAND_MOVE_TO_POSITION,
        step_size,
        TMCL.TYPE_RELATIVE
    )

    # Update the position of the sensor
    s.write(stepCmd)
    sReply = s.readline()

                


