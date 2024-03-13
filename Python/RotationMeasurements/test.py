from MS import MS
from S_Series import S_Series as S
import matplotlib.pyplot as plt
import numpy as np
import time
from TMCL import TMCL

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
amount_of_measurements = 25
waiting_time = 15

# Lock the starting position at 1280000
# motor.set_actual_position(1280000)

# Retrieve the starting position for additional check
begin_pos = motor.actual_position()


# Calculate the step size
half = TMCL.HALF_ROTATION * TMCL.GEAR_RATIO
quarter = TMCL.QUARTER_ROTATION * TMCL.GEAR_RATIO

# Create the array with steps and irradiances
steps = np.array([quarter, -half, half, -quarter])
irr = np.full((len(steps) - 1, 2, amount_of_measurements), 0)

for i in range(len(steps)):
    
    # Rotate first
    step = steps[i]
    print(f"Rotating: {step} microsteps")
    motor.relative_rotation(step)

    # Check whether measurements should be taken this cycle
    if i == len(steps) - 1:
        continue

    # Wait for the sensors to adjust to the environment
    print(f"Waiting {waiting_time}s for the sensors to adjust")
    time.sleep(waiting_time)

    # Start measuring
    print(f"Start taking the measurements")
    for j in range(amount_of_measurements):

        # Retrieve the irradiances
        # of both the reference and test sensor
        ref_irr = ref_sensor.compensated_irradiance()
        test_irr = test_sensor.compensated_irradiance()

        # Add values to array
        irr[i][0][j] = ref_irr
        irr[i][1][j] = test_irr
        print(f"Measurement {j + 1}: R({ref_irr}), T({test_irr}) W/m²")
    

# Retrieve the final position
end_pos = motor.actual_position()
print(f"Beginning position was: {begin_pos}, and the final position is: {end_pos}")



# Calculate the standard deviation and mean of each measurement series
for i in range(len(irr)):
    
    # Mean
    mean_ref = np.mean(irr[i][0])
    mean_test = np.mean(irr[i][1])

    # Standard deviation
    std_ref = np.std(irr[i][0])
    std_test = np.std(irr[i][1])

    print("")
    print(f"Measurement {i+1}: REFERENCE: Mean: {mean_ref}, Sigma: {std_ref}")
    print(f"Measurement {i+1}: TEST: Mean: {mean_test}, Sigma: {std_test}")


