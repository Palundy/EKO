from S_Series import S_Series as S
import minimalmodbus
import time

class MS:
    """
    Class for reading and writing the MS-series pyranometers from
    EKO Instruments.

    This class uses the `minimalmodbus` module for interfacing
    with the sensors.

    
    The MS-series pyranometers can have different communication specifications,
    which is why this class also has childclasses to initiatie for certain models.
    """
    


    sensor = None
    baudrate = 19200
    bytesize = 8
    parity = minimalmodbus.serial.PARITY_NONE
    stopbits = 2
    timeout = 1
    modbus_address = None
    is_ready = False

    time_last_read = None


    def __init__(self, port: str, modbus_address: int = -1, used_addresses: list = [])-> None:
        """
        Configures the connection with the pyranometer.

        Parameters:
            port (str):
                A string representing the port to use.
                Something like `"COM4"`.

            modbus_address (int) [optional]:
                An integer representing the modbuss address to connect to.
                This parameter is optional. The standard value is `-1`, which
                will enable an automatic search for the right modbus address.
                This is not advised when using multiple modbus sensors.

            used_addresses (list) [optional]:
                A list of addresses that are already used.
                This list can be seen as a blacklist.
                The parameter defaults to an empty blacklist.
        """

        if modbus_address == -1:
            print("Search for modbus address is initiated.")

            # The address will be iteratively
            # determined by trying to connect and reading out a value
            while modbus_address < 512:
                try:
                    # Try to connect with the sensor
                    modbus_address += 1
                    print(modbus_address)
                    time.sleep(0.1)

                    if modbus_address in used_addresses:
                        print(f"The current address ({modbus_address}) is already in use. Skipping this search iteration.")
                        self.sensor = None
                        continue

                    self.sensor = minimalmodbus.Instrument(port, modbus_address)
                    self.sensor.serial.baudrate = self.baudrate
                    self.sensor.serial.bytesize = self.bytesize
                    self.sensor.serial.parity = self.parity
                    self.sensor.serial.stopbits = self.stopbits
                    self.sensor.serial.timeout = self.timeout

                    # Try to read the voltage
                    output_voltage = self.output_voltage()
                    if (isinstance(output_voltage, float)):
                        # Succesfully connected
                        print(f"Succesfully connected with sensor. The modbus address is {modbus_address}")
                        self.modbus_address = modbus_address
                        self.is_ready = True
                        return
                    
                except Exception as e:
                    continue

        else:

            # Check whether the given address is already in use
            if modbus_address in used_addresses:
                print(f"This address is already used {modbus_address}")
                print(f"Couldn't connect with the sensor on modbus address {modbus_address}")
                return


            # Connect with the given modbus address
            try:
                # Configure the connection with the pyranometer
                self.sensor = minimalmodbus.Instrument(port, modbus_address)
                self.sensor.serial.baudrate = self.baudrate
                self.sensor.serial.bytesize = self.bytesize
                self.sensor.serial.parity = self.parity
                self.sensor.serial.stopbits = self.stopbits
                self.sensor.serial.timeout = self.timeout
                print(f"Succesfully connected with sensor. The modbus address is {modbus_address}")
                self.modbus_address = modbus_address
                self.is_ready = True
                return
                
            except Exception as e:
                print(f"Couldn't connect with the sensor on modbus address {modbus_address}")
                return

        

    def output_voltage(self)-> float:
        """Returns the sensor output voltage in mV"""
        return self.read_sensor(S.ADDRESS_SENSOR_OUTPUT_VOLTAGE)
    
    
    def compensated_irradiance(self)-> float:
        """Returns the adjusted solar radiation intensity in W/m²"""
        return self.read_sensor(S.ADDRESS_COMPENSATED_IRRADIANCE)
    

    def raw_irradiance(self)-> float:
        """Returns the intensity of solar radiation before correction in W/m²"""
        return self.read_sensor(S.ADDRESS_RAW_IRRADIANCE)
    

    def sensor_temperature(self)-> float:
        """Returns the temperature of the PT100-sensor in °C"""
        return self.read_sensor(S.ADDRESS_PT100)
    

    def internal_temperature(self)-> float:
        """Returns the temperature measured by the internal temperature sensor in °C"""
        return self.read_sensor(S.ADDRESS_INTERNAL_TEMPERATUE)
    

    def internal_humidity(self)-> float:
        """Returns the relative humidity by the the internal humidity sensor in %RH"""
        return self.read_sensor(S.ADDRESS_INTERNAL_HUMIDITY)
    
    
    def x_axis_tilt_angle(self)-> float:
        """Returns the X-axis component of the tilt angle in °"""
        return self.read_sensor(S.ADDRESS_X_AXIS_TILT_ANGLE)
    

    def y_axis_tilt_angle(self)-> float:
        """Returns the Y-axis component of the tilt angle in °"""
        return self.read_sensor(S.ADDRESS_Y_AXIS_TILT_ANGLE)
        
    
    def read_sensor(self, register_address: int)-> int|float|None:
        """
        Reads the sensor and returns the value.
        The value can be an `int` or `float` 
        depending on the register that is being read out.

        Use the series specific class constants to address
        a certain register.

        Parameters:
            `register_address` (`int`):
                The `ADDRESS` constant
                to determine which register to address.
                See the series specific class constants.

        Returns:
            An `int` or `float` depending on which register
            is being read. If the sensor could not be
            read out succesfully; `None` will be returned.
        """

        # Check whether the given `register` is
        # pointing to a valid address
        try:
            register_specification = S.REGISTER_SPECIFICATIONS[register_address]

        except Exception:
            print(f"Given register_address ({register_address}) is not valid.")

        
        # Check whether 0.2s has passed since the last reading of the sensor
        if self.time_last_read != None:
            time_elapsed = time.time() - self.time_last_read
            if (time_elapsed < 0.15):
                # Sleep for the remaining time
                time.sleep(0.15 - time_elapsed)

        # Read out the sensor
        try:
            sensor_value = None
            while sensor_value == None:
                sensor_value = self.sensor.read_float(register_address, 3, register_specification["register_amount"])

        except Exception as e:
            # Failed to read out the sensor
            #       call this function again
            return self.read_sensor(register_address)
        
        # Record the current time
        self.time_last_read = time.time()

        if register_specification["type"] == S.DATA_TYPE_INT:
            # Parse and then return as an integer
            return int(sensor_value)
        return sensor_value

