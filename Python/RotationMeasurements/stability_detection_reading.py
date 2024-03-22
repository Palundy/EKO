from MS import MS
from TMCL import TMCL
import numpy as np
import time
import csv



# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS("COM4", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)


# Set the amount of minutes
amount_of_minutes = 3

# Open the .csv file
begin_time = time.time()
current_time = int(time.time())

# Open the file
filename = f"stability_detection_{current_time}.csv"
with open(filename, "w+", newline="") as file:

    while current_time - begin_time < 60 * amount_of_minutes:

        # Open the writer
        writer = csv.writer(file)


        # Retrieve the irradiances
        # of both the reference and test sensor
        comp_irr_ref = ref_sensor.compensated_irradiance()
        print(comp_irr_ref, current_time)

        # Capture the current time 
        #   this is explicity done after the sensor readouts
        #   because they have blocking behaviour
        current_time = time.time()


        # Write the data into the .csv file
        data = [current_time, comp_irr_ref]
        writer.writerow(data)
        file.flush()

