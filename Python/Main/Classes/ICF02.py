from Classes.MS import MS
from Classes.TMCL import TMCL
import numpy as np
import time

class ICF02:

    def wait_until_irradiance_is_stable(sensor_object: MS, threshold: float = 1.5, attempts: int|None = 5, measurement_amount: int = 30):
        """
        Waits until the (compensated) irradiance sensor readings stabilize within a certain threshold.

        Parameters:
            threshold (float): The threshold value below which the derivative of irradiance signal is considered stable.
                                Default is `1.5 (W/m²)/s`.
            attempts (int | bool): The maximum number of attempts to check for stability. If set to `None`, the function
                                will run indefinitely until stability is reached. Default is `5`.
            measurement_amount (int): The number of measurements to take in each attempt. Default is `30`.

        Returns:
            bool: `True` if the sensor readings stabilize within the specified threshold, `False` otherwise.
        """

        print("Detecting whether sensor is stable.")

        # Initialise the arrays
        I = np.array([], dtype=float) # Irradiances
        t = np.array([], dtype=float) # Time (s)
        D = np.array([], dtype=float) # Derivatives


        # Retrieve the current time
        begin_time = time.time()

        # Count the amount of attempts 
        n_attempts = 0


        # Creating the conditional statement for the while-loop
        while_statement = n_attempts < attempts
        if attempts == None:
            while_statement = True


        while while_statement:

            # Count the amount of measurements
            n_measurements = 0
            while n_measurements < measurement_amount:

                # Retrieve the compensated irradiance
                comp_irr_ref = sensor_object.compensated_irradiance()
                # Capture the current time 
                #   this is explicity done after the sensor readouts
                #   because they have blocking behaviour
                current_time = time.time() - begin_time

                
                # Add the irradiance and the timestamp
                # to the array
                I = np.append(I, comp_irr_ref)
                t = np.append(t, current_time)
                n_measurements += 1        

            
            # Calculate the derivative of each point (excluding the first value)
            D = (I[1:] - I[:-1]) / (t[1:] - t[:-1])

            # Check whether the signal is stable
            consecutive_values = 0
            for k in range(len(D) - 1):
                if abs(D[k]) <= threshold:
                    consecutive_values += 1
                else:
                    consecutive_values = 0
                
                if consecutive_values == int(1/2 * measurement_amount):
                    print("The sensor is stable.")
                    return True
                
            # Update the attempt count
            n_attempts += 1

            # Updating the conditional statement for the while-loop
            while_statement = n_attempts < attempts
            if attempts == None:
                while_statement = True

            print("The sensor is not yet stable.")

        return False
    

    def quick_profile_scan(sensor_object: MS, motor_object: TMCL):
        """
        Performs a quick scan to determine where:
        - The optimal calibration position is
        - The shaded position is
        - How wide the shaded position is
        """

        # Define the discrete rotation segments
        n = 16

        # Initialise the position and irradiance arrays
        P = np.zeros(n)
        I = np.zeros(n)

        # Capture the starting position
        # begin_pos = motor_object.actual_position()

        # Set the rotation speed
        motor_object.set_actual_speed(1000)

        # Iterate over all discrete rotation segments
        for i in range(n):
            
            # Rotate a nth part of a full rotation
            motor_object.relative_rotation(TMCL.FULL_ROTATION * TMCL.CLOCKWISE* TMCL.GEAR_RATIO / n)
            
            # Retrieve the current position
            P[i] = motor_object.actual_position()

            # Capture the irradiance
            I[i] = sensor_object.compensated_irradiance()
            print(i, P[i], I[i])

        print(P)
        print(I)
