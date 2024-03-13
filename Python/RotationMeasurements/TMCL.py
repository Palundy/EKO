import serial
import time

class TMCL:

    # Rotation constants
    FULL_ROTATION = 51200 # Microsteps
    HALF_ROTATION = 25600 # Microsteps
    QUARTER_ROTATION = 12800 # Microsteps
    CLOCKWISE = 1
    COUNTER_CLOCKWISE = -1
    GEAR_RATIO = -5


    # Reply statuses
    REPLY_STATUS_SUCCESS = 100
    REPLY_STATUS_COMMAND_LOADED = 101
    REPLY_STATUS_WRONG_CHECKSUM = 1
    REPLY_STATUS_INVALID_COMMAND = 2
    REPLY_STATUS_WRONG_TYPE = 3
    REPLY_STATUS_INVALID_VALUE = 4
    REPLY_STATUS_EEPROM_LOCKED = 5
    REPLY_STATUS_COMMAND_NOT_AVAILABLE = 6

    statuses = {
        REPLY_STATUS_SUCCESS: "Successfully executed, no error",
        REPLY_STATUS_COMMAND_LOADED: "Command loaded into TMCL program EEPROM",
        REPLY_STATUS_WRONG_CHECKSUM: "Wrong checksum",
        REPLY_STATUS_INVALID_COMMAND: "Invalid command",
        REPLY_STATUS_WRONG_TYPE: "Wrong type",
        REPLY_STATUS_INVALID_VALUE: "Invalid value",
        REPLY_STATUS_EEPROM_LOCKED: "Configuration EEPROM locked",
        REPLY_STATUS_COMMAND_NOT_AVAILABLE: "Command not available"
    }

    # Commands
    COMMAND_ROTATE_RIGHT = 1
    COMMAND_ROTATE_LEFT = 2
    COMMAND_MOTOR_STOP = 3
    COMMAND_MOVE_TO_POSITION = 4
    COMMAND_SET_AXIS_PARAMETER = 5
    COMMAND_GET_AXIS_PARAMETER = 6
    COMMAND_REFERENCE_SEARCH = 13

    # Axis Parameter Type
    AXIS_PARAMETER_TARGET_POSITION = 0
    AXIS_PARAMETER_ACTUAL_POSITION = 1
    AXIS_PARAMETER_TARGET_SPEED = 2
    AXIS_PARAMETER_TARGET_ACTUAL_SPEED = 3
    AXIS_PARAMETER_TARGET_MAXIMUM_POSITIONING_SPEED = 4
    AXIS_PARAMETER_TARGET_MAXIMUM_ACCELERATION = 5

    # Types
    TYPE_ABSOLUTE = 0
    TYPE_RELATIVE = 1


    conn = None
    reply = None

    def __init__(self, port, baudrate = 9600, timeout = 1, write_timeout = 1):
        """
        Initializes a serial connection and stores
        this as a class variable.
        """

        print("Initializing serial connection.")
        try:
            self.conn = serial.Serial(port, baudrate, timeout = timeout, write_timeout = write_timeout)

        except Exception as e:
            print(f"Failed to initialize serial connection. ({e})")
            self.conn = None


    def send_command(self, command_number: int, value: int, type_number: int, module_address: int = 1, motor_number: int = 0):
        

        # Generate the command
        command = self.generate_command(command_number, value, type_number, module_address, motor_number)
        
        # Write the command to the serial connection
        try:
            self.reply = None
            self.conn.write(command)
            time.sleep(0.5)

            self.reply = self.conn.readline()
            return self

        except Exception as e:
            self.reply = None
            return self


    def generate_command(self, command_number: int, value: int, type_number: int, module_address: int = 1, motor_number: int = 0)-> bytearray:
        """
        Generates a command byte array for a TMCL-compatible motor controller.

        This function constructs a binary command consisting of a module address,
        command number, type number, motor or bank number, a 4-byte value, and a checksum.
        The checksum is the lower 8 bits of the sum of all command bytes.

        Args:
            command_number (int): The command number (byte) to identify the TMCL command.
            value (int): The value associated with the TMCL command, expressed as a 4-byte integer.
            type_number (int): The type number (byte) of the TMCL command.
            module_address (int, optional): The address of the module. Defaults to 1.
            motor_number (int, optional): The motor or bank number the command is directed to. Defaults to 0.

        Returns:
            bytearray: A bytearray containing the complete command, including the checksum byte.
        """
            
        # Convert the value to a 4-byte array
        value_bytes = int(value).to_bytes(4, byteorder="big", signed=True)

        # Construct the command (without the checksum)
        command = bytearray([
            module_address,
            command_number,
            type_number,
            motor_number
        ]) + value_bytes

        # Calculate the checksum
        checksum = sum(command) & 0xFF

        # Append the checksum to the byte array
        command.append(checksum)
        return command
    

    def parse_reply(self)-> list:
        """
        Parse a reply bytearray from a module following a specific TMCL reply format.

        The function interprets the given reply bytearray according to the TMCL protocol,
        extracting the reply address, module address, status, command number, value, and checksum.
        The value is a 4-byte integer with the most significant byte first.

        Returns:
        list: A list of integers where each element corresponds to a part of the reply.
            The list contains the following elements in order:
            - reply address (1 byte)
            - module address (1 byte)
            - status (1 byte)
            - command number (1 byte)
            - value (4 bytes, most significant byte first)
            - checksum (1 byte)
        """

        if self.reply == None:
            return False

        # Convert the byte array into an array of integers
        reply_address = self.reply[0]
        module_address = self.reply[1]
        status = self.reply[2]
        command_number = self.reply[3]
        value = int.from_bytes(self.reply[4:8], byteorder='big')
        # checksum = self.reply[8]

        # Create an array with the converted values
        return [reply_address, module_address, status, command_number, value, 0]


    def reply_status(self)-> int:
        """
        Returns the reply status code from a reply bytearray.

        Returns:
        int: The parsed status code.
        """

        if self.reply == None:
            return False

        _, _, status, _, _, _ = self.parse_reply()
        return status
    

    def reply_value(self)-> int:
        """
        Returns the reply value from a reply bytearray.

        Returns:
        int: The parsed value.
        """

        if self.reply == None:
            return False

        _, _, _, _, value, _ = self.parse_reply()
        return value
    

    def ok(self) -> bool:
        """
        Returns whether the last reply is ok or not.

        Returns:
            bool: A bool representing ok or not ok.
        """

        if self.reply == None:
            return False
        
        return self.reply_status() >= TMCL.REPLY_STATUS_SUCCESS
    

    def relative_rotation(self, step_amount: int):
        """
        Wrapper function to send the command
        to rotate the stepper motor by a relative amount.
        The function will block the rest of the script
        until the given position is reached.

        Args:
            step_amount (int): The amount of microsteps.

        Returns:
            Self@TMCL: This instance of the TMCL class.
        """

        # Retrieve the current position of the motor
        begin_pos = self.actual_position()

        # Send the command to move the position
        # by the relative amount
        action = self.send_command(
            TMCL.COMMAND_MOVE_TO_POSITION,
            step_amount,
            TMCL.TYPE_RELATIVE
        ).ok()


        if action:
            while self.is_moving(begin_pos, step_amount):
                # Wait until the position is at the right spot
                time.sleep(0.05)
        return self        

    

    def absolute_rotation(self, position: int):
        """
        Wrapper function to send the command
        to rotate the stepper motor to an absolute position.

        Args:
            position (int): The absolute position.

        Returns:
            Self@TMCL: This instance of the TMCL class.
        """

        # Retrieve the current position of the motor
        begin_pos = self.actual_position()

        # Send the command to move the
        # position to the given absolute position
        action = self.send_command(
            TMCL.COMMAND_MOVE_TO_POSITION,
            position,
            TMCL.TYPE_ABSOLUTE
        ).ok()

        if action:
            while self.is_moving(begin_pos, position - begin_pos):
                # Wait until the position is at the right spot
                time.sleep(0.05)
        return self
    

    def actual_position(self) -> int:
        """
        Wrapper function to send the command
        to get the actual position of the motor.

        Returns:
            int: The actual position.
        """

        if self.send_command(
            TMCL.COMMAND_GET_AXIS_PARAMETER,
            0,
            TMCL.AXIS_PARAMETER_ACTUAL_POSITION
        ).ok():
            return self.reply_value()
        return None
    

    def is_moving(self, begin_pos, step_amount):
        """
        Function to check whether the motor
        has reach the given position.
        This will be calculated by using the amount of
        steps and the begin position
        """
        if self.reply == None:
            return False
        
        end_pos = self.actual_position()
        return abs(end_pos - begin_pos) < abs(step_amount)