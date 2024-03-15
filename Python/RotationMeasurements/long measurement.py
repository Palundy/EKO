from MS import MS
from TMCL import TMCL
import numpy as np
import time
import csv



# Initialize connection with the reference sensor
used_addresses = []
ref_sensor = MS("COM8", 3, used_addresses)
while (ref_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(ref_sensor.modbus_address)

# Initialize connection with the test sensor
test_sensor = MS("COM8", 2, used_addresses)
while (test_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(test_sensor.modbus_address)



# Set the amount of measurements
amount_of_measurements = 150
waiting_time = 60


# Open the .csv file
begin_time = time.time()
current_time = int(time.time())
filename = f"long_measurement_{current_time}.csv"
with open(filename, "w+", newline="") as file:

    while current_time - begin_time < 60 * 20:

        # Open the writer
        writer = csv.writer(file)


        # Retrieve the irradiances
        # of both the reference and test sensor
        comp_irr_ref = ref_sensor.compensated_irradiance()
        comp_irr_test = test_sensor.compensated_irradiance()
        print(comp_irr_ref, comp_irr_test, current_time)

        # Capture the current time 
        #   this is explicity done after the sensor readouts
        #   because they can be blocking
        current_time = time.time()


        # Write the data into the .csv file
        data = [current_time, comp_irr_ref, comp_irr_test]
        writer.writerow(data)
        file.flush()

