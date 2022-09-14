"""
Done
"""

import obd
from obd import OBDCommand
from obd.protocols import ECU


def _decode_cvt(messages):
    """ decoder for CVT temp messages """
    d = messages[0].data  # only operate on a single message
    d = d[15]  # Select single bit N
    N = d
    print("N: " + str(N))  # Real value of temp
    result = (0.000000002344 * (N ** 5)) + (-0.000001387 * (N ** 4)) + (0.0003193 * (N ** 3)) + (
            -0.03501 * (N ** 2)) + (2.302 * N) + (-36.6)  # Decode temp value
    return result


"""cvt temp custom command for mitsubishi outlander xl"""
_cvt_temp_command = OBDCommand(name="RPM",
                               desc="Engine RPM",
                               command=b"2103",
                               _bytes=0,
                               decoder=_decode_cvt,
                               ecu=ECU.ALL,
                               fast=True,
                               header=b"7E1"
                               )


class GetValuesOBD:
    """
    class for getting obd values
    you need to send obd object during class initialization
    """
    def __init__(self, connection):
        self.connection = connection
        connection.supported_commands.add(_cvt_temp_command)  # adding cvt_temp_command to supported commands list

    def get_rpm(self):
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            rpm = response.value.magnitude
        else:
            rpm = 0.0

        return rpm

    def get_maf(self):
        cmd = obd.commands.MAF  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            maf = response.value.magnitude
        else:
            maf = 0.0
        return maf

    def get_speed(self):
        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            speed = response.value.magnitude
        else:
            speed = 0.0
        return speed

    def get_short_l(self):
        cmd = obd.commands.SHORT_FUEL_TRIM_1  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            short_l = response.value.magnitude
        else:
            short_l = 0.0
        return short_l

    def get_long_l(self):
        cmd = obd.commands.LONG_FUEL_TRIM_1  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            long_l = response.value.magnitude
        else:
            long_l = 0.0
        return long_l

    def get_load(self):
        cmd = obd.commands.ENGINE_LOAD  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            load = response.value.magnitude
        else:
            load = 0.0
        return load

    def get_coolant_temp(self):
        cmd = obd.commands.COOLANT_TEMP  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            coolant_temp = response.value.magnitude
        else:
            coolant_temp = 0.0
        return coolant_temp

    def get_fuel_status(self):
        cmd = obd.commands.FUEL_STATUS  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            fuel_status = response.value[0]
        else:
            fuel_status = "Err FUEL_STATUS"
        return fuel_status

    def get_elm_voltage(self):
        cmd = obd.commands.ELM_VOLTAGE  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            elm_voltage = response.value.magnitude
        else:
            elm_voltage = 0.0
        return elm_voltage

    def get_cvt_temp(self):
        cmd = _cvt_temp_command  # select an OBD command (sensor)
        response = self.connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            cvt_temp = response
        else:
            cvt_temp = 0.0
        return cvt_temp
