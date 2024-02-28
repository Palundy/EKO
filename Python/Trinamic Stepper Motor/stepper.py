import minimalmodbus

# Replace '/dev/ttyUSB0' with the port you identified
instrument = minimalmodbus.Instrument('COM3', 1)  # 1 is the slave address (default for many devices)

# Configure instrument
instrument.serial.baudrate = 9600  # Set baud rate
instrument.serial.bytesize = 8
instrument.serial.parity = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout = 1  # seconds

# Ensure you're using RTU mode
instrument.mode = minimalmodbus.MODE_RTU

# Example: Read from a register
# Replace 'register_address' with the address you want to read
# The second parameter is the number of decimals, third is the function code (3 for holding registers)
register_address = 
try:
    value = instrument.read_register(register_address, 0, 3)
    print(f"Register value: {value}")
except IOError:
    print("Failed to read from instrument")
