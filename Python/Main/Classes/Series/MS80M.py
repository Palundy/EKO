class MS80M:
    """
    An interface for providing constants
    for the MS-80M pyranometers
    by EKO Instruments.

    This class is used within the `MS` class.
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
    ADDRESS_MODEL = 8
    """Model number"""

    ADDRESS_COMPENSATED_IRRADIANCE = 21
    """Adjusted solar radiation intensity (W/m2)"""

    ADDRESS_SENSOR_TEMPERATURE = 23
    """Sensor temperature (°C)"""

    ADDRESS_X_AXIS_TILT_ANGLE = -1 
    """Not available on this model."""

    ADDRESS_Y_AXIS_TILT_ANGLE = -2
    """Not available on this model."""

    ADDRESS_RAW_IRRADIANCE = -3
    """Not available on this model."""
    
    ADDRESS_SENSOR_OUTPUT_VOLTAGE = -4
    """Not available on this model."""

    ADDRESS_INTERNAL_TEMPERATUE = -5
    """Not available on this model."""
    
    ADDRESS_INTERNAL_HUMIDITY = -6
    """Not available on this model."""

    ADDRESS_ALERTS_ABNORMAL_INTERNAL_HUMIDITY = -7
    """Not available on this model."""



    #   Register datatypes
    REGISTER_SPECIFICATIONS = {
        ADDRESS_MODEL: {
            "format": DATA_FORMAT_U16,
            "type": DATA_TYPE_INT,
            "register_amount": 5
        },
        ADDRESS_COMPENSATED_IRRADIANCE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_SENSOR_TEMPERATURE: {
            "format": DATA_FORMAT_F32,
            "type": DATA_TYPE_FLOAT,
            "register_amount": 2
        },
        ADDRESS_X_AXIS_TILT_ANGLE: None,
        ADDRESS_Y_AXIS_TILT_ANGLE: None,
        ADDRESS_RAW_IRRADIANCE: None,
        ADDRESS_SENSOR_OUTPUT_VOLTAGE: None,
        ADDRESS_INTERNAL_TEMPERATUE: None,
        ADDRESS_INTERNAL_HUMIDITY: None,
        ADDRESS_ALERTS_ABNORMAL_INTERNAL_HUMIDITY: None
    }
    """A dictionary containing the format and datatype of certain addresses.
    Examples:
    - `REGISTER_DATA_TYPES[ADDRESS_MODEL]["format"] => DATA_FORMAT_U16`
    - `REGISTER_DATA_TYPES[ADDRESS_MODEL]["type"] => DATA_TYPE_FLOAT`
    - `REGISTER_DATA_TYPES[ADDRESS_MODEL]["register_amount"] => 1`
    """

