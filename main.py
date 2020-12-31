#!/usr/bin/python


from __future__ import division
# import time
import os
import threading
import time
import sys
import obd
import pygame
import csv
import platform

# uncomment for using background image
# background_image = pygame.image.load("toyota_logo4.jpg")

fuel_status = 4
engine_on_rpm = 400
time_start = 0
time1 = 0
time_new = 0
time_old = 0
#time_old_gurnal = 0
benz_potracheno_trip = 0
LP100_trip = 0.0
LP100_inst = 0.0
odometer_trip = 0.0
odometer_add = 0.0
AirFuelRatio = 14.70
FuelDensityGramsPerLiter = 750.0
average_speed_trip = 0.0
time_trip = 0
LPH = 0.0
LP100_full = 0.0
odometer_full = 0.0
benz_potracheno_full = 0.0
volts_alert = 12.6
temp_alert = 100.0
# font = 'font/ds_digital/DS-DIGIB.TTF'
font_file = 'font/ubuntu/UbuntuMono-B.ttf'
log_file = 'log.csv'
time_old_gurnal = 0
odometer_add_gurnal = 0.0
benz_add_gurnal = 0.0
time_add_gurnal = 0.0
time_full = 0.0
average_speed_full = 0.0
odometer_eeprom = 0.0
benz_eeprom = 0.0
time_eeprom = 0.0

i = 0


#CONTROL_MODULE_VOLTAGE = 0.0
GET_MAF = 0.0
GET_RPM = 0
GET_SPEED = 0.0
GET_LOAD = 0.0
GET_SHORT_L = 0.0
GET_LONG_L = 0.0
GET_TEMP = 0
GET_FUEL_STATUS = ""
ELM_VOLTAGE = 0.0

# variables for stopping application
STOP_ACCEL = 1
STOP_PRINT = 1
STOP_GET = 1


def print_text_topleft(x, y, text, size, fill):
    font = pygame.font.Font(font_file, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(puttext, text_rect)


def print_text_topright(x, y, text, size, fill):
    # font = pygame.font.Font('font/ubuntu/UbuntuMono-B.ttf', size)
    font = pygame.font.Font(font_file, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.topright = (x, y)
    screen.blit(puttext, text_rect)


def print_text_midtop(x, y, text, size, fill):
    # font = pygame.font.Font('font/ubuntu/UbuntuMono-B.ttf', size)
    font = pygame.font.Font(font_file, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(puttext, text_rect)


def get_values():
    global GET_FUEL_STATUS, GET_TEMP, GET_RPM, GET_SPEED, GET_LOAD, GET_SHORT_L, GET_LONG_L, GET_MAF, \
        CONTROL_MODULE_VOLTAGE, ELM_VOLTAGE

    while STOP_GET:
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_RPM = response.value.magnitude

        cmd = obd.commands.MAF  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_MAF = response.value.magnitude

        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SPEED = response.value.magnitude

        cmd = obd.commands.SHORT_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SHORT_L = response.value.magnitude

        cmd = obd.commands.LONG_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LONG_L = response.value.magnitude

        cmd = obd.commands.ENGINE_LOAD  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LOAD = response.value.magnitude

        cmd = obd.commands.COOLANT_TEMP  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_TEMP = response.value.magnitude

        cmd = obd.commands.FUEL_STATUS  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_FUEL_STATUS = response.value[0]

        cmd = obd.commands.ELM_VOLTAGE
        response = connection.query(cmd)
        if response.value is not None:
            ELM_VOLTAGE = response.value.magnitude


def print_fuel_status_string():
    if GET_FUEL_STATUS is not None:
        print_text_topleft(0, 500, GET_FUEL_STATUS, 30, fill=(255, 255, 55))


def print_screen(screen_number):
    if screen_number is 0:

        # Print screen title
        print_text_midtop(150, 0, "trip odometer", 30, fill=(42, 157, 1))
        print_text_midtop(500, 0, "odometer", 30, fill=(42, 157, 1))

        # Print L/h or instant L/100km in motion
        if GET_SPEED > 0:
            print_text_topright(140, 30, "{:.1f}".format(LP100_inst), 40, fill=(2, 135, 178))
            print_text_topleft(150, 30, "L/100", 40, fill=(2, 135, 178))
        else:
            print_text_topright(140, 30, "{:.1f}".format(LPH), 40, fill=(2, 135, 178))
            print_text_topleft(150, 30, "L/h", 40, fill=(2, 135, 178))

        # Print av speed trip
        print_text_topright(140, 75, "{:.1f}".format(average_speed_trip), 40, fill=(2, 135, 178))
        print_text_topleft(150, 75, "km/h av", 40, fill=(2, 135, 178))

        # Print trip L/100
        if odometer_trip > 0.1:
            lp100_to_print = "{:.1f}".format(LP100_trip)  # display Lp100km value after 0.1 km trip
        else:
            lp100_to_print = "-.-"
        print_text_topright(140, 115, lp100_to_print, 40, fill=(2, 135, 178))
        print_text_topleft(150, 115, "l/100", 40, fill=(2, 135, 178))

        # Print trip km
        print_text_topright(140, 155, "{:.1f}".format(odometer_trip), 40, fill=(2, 135, 178))
        print_text_topleft(150, 155, "km", 40, fill=(2, 135, 178))

        # Print trip L
        print_text_topright(140, 195, "{:.2f}".format(benz_potracheno_trip), 40, fill=(2, 135, 178))
        print_text_topleft(150, 195, "l", 40, fill=(2, 135, 178))

        # right side first row

        # print RPM
        print_text_topleft(500, 30, "rpm", 40, fill=(2, 135, 178))
        print_text_topright(490, 30, "{:.0f}".format(GET_RPM), 40, fill=(2, 135, 178))

        # print av speed full
        print_text_topleft(500, 75, "km/h av", 40, fill=(2, 135, 178))
        print_text_topright(490, 75, "{:.1f}".format(average_speed_full), 40, fill=(2, 135, 178))

        # print av L/100 full
        print_text_topleft(500, 115, "l/100 av", 40, fill=(2, 135, 178))
        print_text_topright(490, 115, "{:.1f}".format(LP100_full), 40, fill=(2, 135, 178))

        # print odometer full
        print_text_topleft(500, 155, "km", 40, fill=(2, 135, 178))
        print_text_topright(490, 155, "{:.2f}".format(odometer_full), 40, fill=(2, 135, 178))

        # print fuel litters full
        print_text_topleft(500, 195, "L", 40, fill=(2, 135, 178))
        print_text_topright(490, 195, "{:.2f}".format(benz_potracheno_full), 40, fill=(2, 135, 178))

        # sensors data - second row

        # Print screen title
        print_text_midtop(343, 235, "SENSORS", 30, fill=(42, 157, 1))

        # Print long term fuel trim
        print_text_topright(140, 265, "{:+.1f}".format(GET_LONG_L), 40, fill=(2, 135, 178))
        print_text_topleft(150, 265, "% LTFT", 40, fill=(2, 135, 178))

        # Print MAF
        print_text_topright(140, 305, "{:.2f}".format(GET_MAF), 40, fill=(2, 135, 178))
        print_text_topleft(150, 305, "g/cm^3 MAF", 40, fill=(2, 135, 178))

        # Print trip L/100
        print_text_topright(140, 345, "{:.1f}".format(GET_LOAD), 40, fill=(2, 135, 178))
        print_text_topleft(150, 345, "% ENG LOAD", 40, fill=(2, 135, 178))

        # Print speed
        print_text_topright(140, 385, "{:.0f}".format(GET_SPEED), 40, fill=(2, 135, 178))
        print_text_topleft(150, 385, "km/h", 40, fill=(2, 135, 178))

        # right side second row

        # print RPM
        print_text_topleft(500, 265, "% STFT", 40, fill=(2, 135, 178))
        print_text_topright(490, 265, "{:+.1f}".format(GET_SHORT_L), 40, fill=(2, 135, 178))

        # print volts
        if ELM_VOLTAGE < volts_alert:
            print_text_topleft(500, 305, "V", 40, fill=(235, 7, 49))
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), 40, fill=(235, 7, 49))
        else:
            print_text_topleft(500, 305, "V", 40, fill=(2, 135, 178))
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), 40, fill=(2, 135, 178))

        # print coolant temp
        degree_sign = u"\N{DEGREE SIGN}"
        if GET_TEMP > temp_alert:
            print_text_topleft(500, 345, degree_sign + "C", 40, fill=(235, 7, 49))
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), 40, fill=(235, 7, 49))
        else:
            print_text_topleft(500, 345, '\u00b0' + "C", 40, fill=(2, 135, 178))
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), 40, fill=(2, 135, 178))

        # print rpm
        # disabled for debug. DND
        #print_text_topleft(500, 385, "RPM", 40, fill=(2, 135, 178))
        #print_text_topright(490, 385, "{:.0f}".format(GET_RPM), 40, fill=(2, 135, 178))
        print_text_topleft(500, 385, "Write", 40, fill=(2, 135, 178))
        print_text_topright(490, 385, "{:.0f}".format(i), 40, fill=(2, 135, 178))


def csv_read():
    # 0 - odometer
    # 1 - fuel
    # 2 - time
    with open(log_file, 'r', newline='') as f:
        data = csv.reader(f, delimiter=',')
        data_return = list(data)
        return data_return[0]


def csv_write(odometer_eeprom, benz_eeprom, time_eeprom):
    with open(log_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([odometer_eeprom, benz_eeprom, time_eeprom])


def quit_app():
    global STOP_GET, STOP_PRINT, STOP_ACCEL
    STOP_GET = 0
    STOP_PRINT = 0
    STOP_ACCEL = 0


pygame.init()
clock = pygame.time.Clock()
# screen = pygame.display.set_mode((800, 480))
screen = pygame.display.set_mode((685, 455))

if not platform.system().startswith("Windows"):
    pygame.display.toggle_fullscreen()

done = False
pygame.mouse.set_visible(False)

if platform.system().startswith("Windows"):
    connection = obd.OBD("COM10")  # config for Windows OS
else:
    connection = obd.OBD()
    # connection = obd.OBD("/dev/ttyUSB0")  # auto-connects to USB or RF port

Thread_getValues = threading.Thread(target=get_values)
Thread_getValues.daemon = False
Thread_getValues.start()

# checking is log file available or not. creating new one if not
if not os.path.isfile(log_file):
    file = open(log_file, "w+")
    writer = csv.writer(file)
    writer.writerow(["0.0", "0.0", "0.0"])
    file.close()

while not done:

    if GET_RPM > engine_on_rpm:
        FuelFlowLitersPerSecond = 0.0
        odometer_add = 0.0
        if GET_LOAD > 3:
            if GET_FUEL_STATUS == 'Closed loop, using oxygen sensor feedback to determine fuel mix':
                fuel_status = 2
            else:
                fuel_status = 4

            if fuel_status == 2:  # if Closed Loop
                ls_term_val = (100.0 + GET_LONG_L + GET_SHORT_L) / 100.0  # fuel correction by ShortTerm and LongTerm
            else:  # if open loop
                ls_term_val = (100.0 + GET_LONG_L) / 100.0  # fuel correction trim by LongTerm

            FuelFlowGramsPerSecond = (GET_MAF / AirFuelRatio) * ls_term_val  # calculate gram of petrol per second
            # 14,7 air to 1 litter of gas, ls_term_val
            FuelFlowLitersPerSecond = FuelFlowGramsPerSecond / FuelDensityGramsPerLiter  # grams of petrol to litters
            LPH = FuelFlowLitersPerSecond * 3600.0  # Litter per second to litter per hour

        # speed and odometer calculations
        if time_start == 0:
            time_start = time.time()

        time_trip = time.time() - time_start

        if time_old == 0:
            time_old = time.time()  # do once after starting the app

        time_new = time.time()   # time from starting the app
        time1 = time_new - time_old  # * tcorrect  # time after the last speed calculating

        if time1 > 10:
            time1 = 0

        time_old = time_new  # write new time for comparing in new cycle

        benz_add = FuelFlowLitersPerSecond * time1
        benz_potracheno_trip = benz_potracheno_trip + benz_add  # fuel consumption for trip

        if GET_SPEED > 0:
            odometer_add = (((GET_SPEED * 1000.0) / 3600.0) * time1) / 1000.0  # calculate distance der time1
            odometer_trip = odometer_trip + odometer_add  # odometer value per trip
            if odometer_add > 0:
                LP100_inst = (benz_add / odometer_add) * 100.0  # instant fuel consumption

        if odometer_trip > 0 and time_trip > 0:
            average_speed_trip = odometer_trip / (time_trip / 3600.0)

        # Writing data to log file on drive
        if ((GET_SPEED > 1) and (GET_SPEED < 10) and ((time_new - time_old_gurnal) > 30)) or \
                ((GET_SPEED <= 1) and ((time_new - time_old_gurnal) > 10)) or \
                ((time_new - time_old_gurnal) > 300):
            # if True:
            # read data from log file
            log_data = csv_read()
            odometer_eeprom = float(log_data[0]) + odometer_add_gurnal + odometer_add
            benz_eeprom = float(log_data[1]) + benz_add_gurnal + benz_add
            time_eeprom = float(log_data[2]) + time_add_gurnal + time1
            # Vrite new data in log file
            csv_write(odometer_eeprom, benz_eeprom, time_eeprom)
            print("time_eeprom = " + str(time_eeprom))
            # Write temp counter of writes to storage
            i += 1

            #calculations for avarage values
            odometer_full = odometer_eeprom
            benz_potracheno_full = benz_eeprom
            time_full = time_eeprom
            if odometer_full > 0:
                LP100_full = (benz_potracheno_full / odometer_full) * 100.0
            if time_full >0:
                average_speed_full = odometer_full / (time_full / 3600.0)

            odometer_add_gurnal = 0
            benz_add_gurnal = 0
            time_add_gurnal = 0
            time_old_gurnal = time_new

        else:
            odometer_add_gurnal = odometer_add_gurnal + odometer_add
            benz_add_gurnal = benz_add_gurnal + benz_add
            time_add_gurnal += time1

            odometer_full = odometer_eeprom + odometer_add_gurnal
            benz_potracheno_full = benz_eeprom + benz_add_gurnal
            time_full = time_eeprom + time_add_gurnal
            if odometer_full > 0:
                LP100_full = (benz_potracheno_full / odometer_full) * 100.0
            if time_full > 0:
                average_speed_full = odometer_full / (time_full / 3600.0)

    else:
        if GET_SPEED == 0:
            time_start = 0
            time_trip = 0
            odometer_trip = 0
            benz_potracheno_trip = 0

    if odometer_trip > 0:
        LP100_trip = (benz_potracheno_trip / odometer_trip) * 100.0  # Fuel consumption L/100km


    # manage events to quit the application
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            done = True
            quit_app()
        if event.type == pygame.QUIT:
            done = True
            quit_app()

    screen.fill((0, 20, 0))
    # uncomment for using background image
    # screen.blit(background_image, (0, 0))
    print_screen(0)  # display values on screen 0
    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # set fps for the app
pygame.init()
sys.exit(0)
