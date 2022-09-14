



# test get_values.py module
import obd
from get_values import GetValuesOBD


o = obd.OBD("COM2")
values_obd = GetValuesOBD(o)

for i in range(1000):
    print("rpm: " + str(values_obd.get_rpm()))
    print("coolant temp: " + str(values_obd.get_coolant_temp()))
    print("cvt temp: " + str(values_obd.get_cvt_temp()))
    print("elm voltage: " + str(values_obd.get_elm_voltage()))
    print("fuel status: " + str(values_obd.get_fuel_status()))
    print("load: " + str(values_obd.get_load()))
    print("long fuel trim: " + str(values_obd.get_long_l()))
    print("maf: " + str(values_obd.get_maf()))
    print("short fuel trim: " + str(values_obd.get_short_l()))
    print("speed: " + str(values_obd.get_speed()))






"""
# working with strings and OK paths

import os

print(os.path.expanduser('~/Music'))

max_characters_displayed_per_line = 40
song_title = "14 Christoph Doom Schneider - Doctor Christian Lorenz - Till Lindemann - Paul Landers - Richard Z. Kruspe - Oliver Riedel - Ohne Dich.mp3"

try:

    tmp_str_list = song_title.split()  # split on  strings

    # print first half of items in list on first line
    first_line = "".join(str(i) + " " for i in tmp_str_list[: len(tmp_str_list) // 2])
    if len(first_line) > max_characters_displayed_per_line:
        raise Exception("first half of song title is too long. print first max_characters_displayed_per_line")

    print_text_midtop(443, 100, first_line, 50, fill=alert_text_color)

    # print second half of items in list on second line
    second_line = "".join(str(i) + " " for i in tmp_str_list[len(tmp_str_list) // 2:])
    if len(second_line) > max_characters_displayed_per_line:
        second_line = second_line[:max_characters_displayed_per_line]
    print_text_midtop(443, 140, second_line, 50, fill=alert_text_color)

except Exception as e:
    # print(e)

    print(443, 140, song_title[:max_characters_displayed_per_line - 1])

#print(s[:5])
"""


"""

CVT temp test


from obd import OBDCommand, Unit
from obd.protocols import ECU
import obd


def decode(messages):
    # decoder for CVT temp messages
    d = messages[0].data  # only operate on a single message
    d = d[15] # Select single bit N
    N = d
    print("N: " + str(N)) # Real value of temp
    result = (0.000000002344 * (N ** 5)) + (-0.000001387 * (N ** 4)) + (0.0003193 * (N ** 3)) + (
            -0.03501 * (N ** 2)) + (2.302 * N) + (-36.6)  # Decode temp value
    return result


cvt_temp_command = OBDCommand(name="RPM",
                              desc="Engine RPM",
                              command=b"2103",
                              _bytes=0,
                              decoder=decode,
                              ecu=ECU.ALL,
                              fast=True,
                              header=b"7E1"
                              )

o = obd.OBD("COM6")
o.supported_commands.add(cvt_temp_command)

for i in range(5):
    cvt_temp = o.query(cvt_temp_command)
    print("CVT TEMP: " + str(cvt_temp))
    print("{:.0f}".format(float(str(cvt_temp))))
"""
