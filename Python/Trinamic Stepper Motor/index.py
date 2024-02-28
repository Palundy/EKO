import serial
import time
from TMCL import *

port = "COM3"
baud_rate = 9600

"""
The PD-2-1611 has 256 microsteps per step.
And 200 steps per revolution.
Thus: 51200 microsteps per revolution.
"""



try:
    with serial.Serial(port, baudrate=baud_rate, timeout=1) as s:

        # Generating the command to retrieve the actual position of the motor
        posCmd = TMCL.generateCommand(
            TMCL.COMMAND_GET_AXIS_PARAMETER,
            0,
            TMCL.AXIS_PARAMETER_ACTUAL_POSITION
        )

        # Generating the command to turn 180° clockwise
        cwSteps = TMCL.CLOCKWISE * TMCL.HALF_ROTATION * TMCL.GEAR_RATIO # Amount of steps for 180° clockwise rotation of the harmonic drive axis
        cwCmd = TMCL.generateCommand(
            TMCL.COMMAND_MOVE_TO_POSITION,
            cwSteps,
            TMCL.TYPE_RELATIVE
        )

        # Generating the command to turn 180° counter-clockwise
        ccwSteps = TMCL.COUNTER_CLOCKWISE * TMCL.HALF_ROTATION * TMCL.GEAR_RATIO # Amount of steps for 180° counter-clockwise rotation of the harmonic drive axis
        ccwCmd = TMCL.generateCommand(
            TMCL.COMMAND_MOVE_TO_POSITION,
            ccwSteps,
            TMCL.TYPE_RELATIVE
        )



        # Retrieve the starting position of the axis
        startingPos = None
        s.write(posCmd)
        sReply = s.readline()
        if sReply:
            startingPos = TMCL.returnReplyValue(sReply)
            print("The starting position is: ", startingPos)



        # Turn clockwise
        intermediatePos = startingPos
        s.write(cwCmd)
        sReply = s.readline()
        
        if sReply:
            # Wait until the position of the motor is valid
            while abs(intermediatePos - startingPos) < abs(cwSteps):
                # Retrieve the position of the axis
                print("In loop")
                s.write(posCmd)
                sReply = s.readline()
                intermediatePos = TMCL.returnReplyValue(sReply)
            print("Succesfully turned 180° clockwise")

        
        # Turn counter-clockwise
        endPos = intermediatePos
        s.write(ccwCmd)
        sReply = s.readline()
        if sReply:
            # Wait until the position of the motor is valid
            while abs(endPos - intermediatePos) < abs(ccwSteps):
                # Retrieve the position of the axis
                print("In loop")
                s.write(posCmd)
                sReply = s.readline()
                endPos = TMCL.returnReplyValue(sReply)
            print("Succesfully turned 180° counter-clockwise")
    
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")