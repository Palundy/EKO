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

# Initialize connection with the test sensor
test_sensor = MS("COM8", 2, used_addresses)
while (test_sensor.is_ready == False):
    time.sleep(1)
used_addresses.append(test_sensor.modbus_address)



# Set the amount of measurements
amount_of_measurements = 150
waiting_time = 60


# Open the .csv file
current_time = int(time.time())
filename = f"calibration_data_{current_time}.csv"
with open(filename, "w+", newline="") as file:

    # Open the writer
    writer = csv.writer(file)

    # Retrieve the starting position for additional check
    begin_pos = motor.actual_position()
    print(f"Begin pos: {begin_pos}")


    # Calculate the step size
    half = TMCL.HALF_ROTATION * TMCL.GEAR_RATIO
    quarter = TMCL.QUARTER_ROTATION * TMCL.GEAR_RATIO

    # Create the array with steps and irradiance data
    steps = np.array([0, quarter, -half, half, -quarter])
    irr = np.full((len(steps) - 1, 2, amount_of_measurements), 0)


    for i in range(len(steps)):

        
        # Rotate first
        step = steps[i]
        print(f"Rotating: {step} microsteps")
        motor.relative_rotation(step)

        # Check whether measurements should be taken this cycle
        if i == len(steps) - 1:
            print("Reached home position!")
            continue

        # Wait for the sensors to adjust to the environment
        if (i != 0):
            print(f"Waiting {waiting_time}s for the sensors to adjust")
            time.sleep(waiting_time)

        # Capture the current position
        current_pos = motor.actual_position()

        # Start measuring
        print(f"Start taking the measurements")
        for j in range(amount_of_measurements):

            # Retrieve the irradiances
            # of both the reference and test sensor
            comp_irr_ref = ref_sensor.compensated_irradiance()
            comp_irr_test = test_sensor.compensated_irradiance()

            # Capture the current time 
            #   this is explicity done after the sensor readouts
            #   because they can be blocking
            current_time = time.time()

            # Add values to array
            irr[i][0][j] = comp_irr_ref
            irr[i][1][j] = comp_irr_test
            print(f"Measurement {j + 1}: R({comp_irr_ref}), T({comp_irr_test}) W/m²")

            # Write the data into the .csv file
            data = [
                i, current_time, current_pos, 
                comp_irr_ref, comp_irr_test,
            ]
            writer.writerow(data)
            file.flush()
        

    # Flush the file once more
    file.flush()

    # Retrieve the final position
    end_pos = motor.actual_position()
    print(f"Beginning position was: {begin_pos}, and the final position is: {end_pos}")

