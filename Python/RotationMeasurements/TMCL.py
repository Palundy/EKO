class TMCL:

    # Rotation constants
    FULL_ROTATION = 51200 # Microsteps
    HALF_ROTATION = 25600 # Microsteps
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


    def generateCommand(command_number: int, value: int, type_number: int, module_address: int = 1, motor_number: int = 0)-> bytearray:
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
        value_bytes = value.to_bytes(4, byteorder="big", signed=True)

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
    

    def parseReply(reply: bytearray)-> list:
        """
        Parse a reply bytearray from a module following a specific TMCL reply format.

        The function interprets the given reply bytearray according to the TMCL protocol,
        extracting the reply address, module address, status, command number, value, and checksum.
        The value is a 4-byte integer with the most significant byte first.

        Parameters:
        reply (bytearray): The byte array to be parsed. It should be exactly 9 bytes long,
                        corresponding to the expected format of the reply.

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

        # Convert the byte array into an array of integers
        reply_address = reply[0]
        module_address = reply[1]
        status = reply[2]
        command_number = reply[3]
        value = int.from_bytes(reply[4:8], byteorder='big')
        checksum = reply[8]

        # Create an array with the converted values
        return [reply_address, module_address, status, command_number, value, checksum]


    def returnReplyStatus(reply: bytearray)-> int:
        """
        Returns the reply status code from a reply bytearray.

        Parameters:
        reply (bytearray): The byte array to be parsed. It should be exactly 9 bytes long,
                        corresponding to the expected format of the reply.

        Returns:
        int: The parsed status code.
        """

        _, _, status, _, _, _ = TMCL.parseReply(reply)
        return status
    

    def returnReplyValue(reply: bytearray)-> int:
        """
        Returns the reply status code from a reply bytearray.

        Parameters:
        reply (bytearray): The byte array to be parsed. It should be exactly 9 bytes long,
                        corresponding to the expected format of the reply.

        Returns:
        int: The parsed value.
        """

        _, _, _, _, value, _ = TMCL.parseReply(reply)
        return value