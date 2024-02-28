import minimalmodbus
import time
import matplotlib.pyplot as plt
import numpy as np


port = "COM5"
baud_rate = 19200
bytesize = 8
# parity = minimalmodbus.serial.PARITY_EVEN
parity = minimalmodbus.serial.PARITY_NONE
stopbits = 2
timeout = 1

modbus_address = 2

max_retries = 500
retry_delay = 1.5


x = np.arange(0, max_retries, 1)
y = np.zeros(max_retries, dtype=float)



plt.ion()
figure, ax = plt.subplots()
line, = ax.plot(x, y)
ax.autoscale(enable=True, axis='y', tight=None)

try:
    instrument = minimalmodbus.Instrument("COM5", modbus_address)
except Exception as e:
    print("An error has occured: ", e)
    


instrument.serial.baudrate = baud_rate
instrument.serial.bytesize = 8
instrument.serial.parity = parity
instrument.serial.stopbits = stopbits
instrument.serial.timeout = timeout


def read_sensor(register_address, max_retries, retry_delay):
    for attempt in range(max_retries):
        try:
            comp_irradiance = instrument.read_float(register_address, functioncode=3, number_of_registers=2)
            y[attempt:] = abs(comp_irradiance)
            
            # updating data values
            line.set_xdata(x)
            line.set_ydata(y)

            ax.relim()
            ax.autoscale_view()
        
            # drawing updated values
            figure.canvas.draw()
        
            # This will run the GUI event
            # loop until all UI events
            # currently waiting have been processed
            figure.canvas.flush_events()
        
        except IOError as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            time.sleep(retry_delay)  # Wait before retrying
    return None

# Attempt to read the sensor register with retries
read_sensor(2, max_retries, retry_delay)
print(y)