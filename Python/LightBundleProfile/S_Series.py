class S_Series:
    """
    An interface for providing constants
    for the S-type MS-series pyranometers
    by EKO Instruments.

    This class can be used within the `MS` class.
    """

    #   Data types
    DATA_TYPE_FLOAT = 0
    """Float data type"""

    DATA_TYPE_INT = 1
    """Integer data types"""



    #   Data formats
    DATA_FORMAT_U16 = 0 
    """Unsigned 16-bit integer"""

    DATA_FORMAT_S16 = 1
    """Signed 16-bit integer"""

    DATA_FORMAT_U32 = 2
    """Unsigned 32-bit integer"""

    DATA_FORMAT_S32 = 3
    """Signed 32-bit integer"""

    DATA_FORMAT_F32 = 4
    """IEEE754 32-bit floating point format """

    DATA_FORMAT_STR = 5 
    """ASCII characters string"""



    #   Register addresses
    ADDRESS_MODEL = 0
    """Model number of the transmitter. (MS-80S:0x0110)"""

    ADDRESS_COMPENSATED_IRRADIANCE = 2
    """Adjusted solar radiation intensity (W/m2)"""

    ADDRESS_PT100 = 8
    """Sensor temperature (°C)"""

    ADDRESS_X_AXIS_TILT_ANGLE = 14
    """X-axis component of the tilt angle (°)"""

    ADDRESS_Y_AXIS_TILT_ANGLE = 16
    """Y-axis component of the tilt angle (°)"""

    ADDRESS_RAW_IRRADIANCE = 18
    """Intensity of solar radiation before correction (W/m2)"""
    
    ADDRESS_SENSOR_OUTPUT_VOLTAGE = 20
    """Sensor output voltage (mV)"""

    ADDRESS_INTERNAL_TEMPERATUE = 22
    """Temperature measured by the internal temperature sensor (°C)"""
    
    ADDRESS_INTERNAL_HUMIDITY = 24
    """Relative humidity measured by the internal humidity sensor (% RH)"""

    ADDRESS_ALERTS_ABNORMAL_INTERNAL_HUMIDITY = 26
    """Alerts for abnormalities in the internal humidity of the pyranometer. Normal: *0, Abnormality occurs: 1"""



    #   Register datatypes
    REGISTER_SPECIFICATIONS = {
        ADDRESS_MODEL: {
            "format": DATA_FORMAT_U16,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 1
        },
        ADDRESS_COMPENSATED_IRRADIANCE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_PT100: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_X_AXIS_TILT_ANGLE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_Y_AXIS_TILT_ANGLE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_RAW_IRRADIANCE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_SENSOR_OUTPUT_VOLTAGE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_INTERNAL_TEMPERATUE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_INTERNAL_HUMIDITY: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_ALERTS_ABNORMAL_INTERNAL_HUMIDITY: {
            "format": DATA_FORMAT_U16,
            "type": DATA_TYPE_INT,
            "register_amount": 2
        }
    }
    """A dictionary containing the format and datatype of certain addresses.
    Examples:
    - `REGISTER_DATA_TYPES[ADDRESS_MODEL]["format"] => DATA_FORMAT_U16`
    - `REGISTER_DATA_TYPES[ADDRESS_MODEL]["type"] => DATA_TYPE_FLOAT`
    - `REGISTER_DATA_TYPES[ADDRESS_MODEL]["register_amount"] => 1`
    """

