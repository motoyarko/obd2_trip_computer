#!/usr/bin/python

# Thanks to:
# https://sohabr.net/habr/post/252207/
# https://www.drive2.ru/l/481530293824520264/

from __future__ import division
import os
import threading
import time
import sys
import obd
import pygame
import csv
import platform
from gpiozero import Button

if not platform.system().startswith("Windows"):
    button1 = Button(2)
    button2 = Button(3)
screen_counter = 0
screen_last = 1
fuel_status = False
engine_on_rpm = 200
time_start = 0
time1 = 0
time_new = 0
time_old = 0
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
# font_file = 'UbuntuMono-B.ttf'
font_file = 'Audiowide-Regular.ttf'
font_size_values = 35
log_file = 'log.csv'
background_image = pygame.image.load("logo5.jpg")
time_old_gurnal = 0
odometer_add_gurnal = 0.0
benz_add_gurnal = 0.0
time_add_gurnal = 0.0
time_full = 0.0
average_speed_full = 0.0
odometer_eeprom = 0.0
benz_eeprom = 0.0
time_eeprom = 0.0
default_text_color = (102, 102, 102)
# default_text_color = (230, 230, 230)
# default_text_color = (0, 0, 0)
alert_text_color = (235, 7, 49)
title_text_color = (204, 204, 204)
# title_text_color = (10, 10, 10)
# background_color = (0, 20, 0)
background_color = (42, 120, 10)

write_flash_counter = 0

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


def button_process():
    global screen_counter
    while STOP_GET:
        if button1.is_pressed:
            time.sleep(0.15)
            while button1.is_pressed:
                pass
            else:
                if screen_counter < screen_last:
                    screen_counter += 1
                else:
                    screen_counter = 0

        if button2.is_pressed:
            time.sleep(0.15)
            while button2.is_pressed:
                pass
            else:
                screen_counter = 11
                """
                if screen_counter < screen_last:
                   screen_counter += 11
                else:
                   screen_counter = 11
                """


def print_text_topleft(x, y, text, size, fill):
    font = pygame.font.Font(font_file, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(puttext, text_rect)


def print_text_topright(x, y, text, size, fill):
    font = pygame.font.Font(font_file, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.topright = (x, y)
    screen.blit(puttext, text_rect)


def print_text_midtop(x, y, text, size, fill):
    font = pygame.font.Font(font_file, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(puttext, text_rect)


def get_values():
    global GET_FUEL_STATUS, GET_TEMP, GET_RPM, GET_SPEED, GET_LOAD, GET_SHORT_L, GET_LONG_L, GET_MAF, ELM_VOLTAGE
    while STOP_GET:
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_RPM = response.value.magnitude
        else:
            GET_RPM = 0.0

        cmd = obd.commands.MAF  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_MAF = response.value.magnitude
        else:
            GET_MAF = 0.0

        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SPEED = response.value.magnitude
        else:
            GET_SPEED = 0.0

        cmd = obd.commands.SHORT_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SHORT_L = response.value.magnitude
        else:
            GET_SHORT_L = 0.0

        cmd = obd.commands.LONG_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LONG_L = response.value.magnitude
        else:
            GET_LONG_L = 0.0

        cmd = obd.commands.ENGINE_LOAD  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LOAD = response.value.magnitude
        else:
            GET_LOAD = 0.0

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
        print_text_midtop(150, 0, "trip odometer", 30, fill=title_text_color)
        print_text_midtop(500, 0, "odometer", 30, fill=title_text_color)

        # Print L/h or instant L/100km in motion
        if GET_SPEED > 0:
            print_text_topright(140, 30, "{:.1f}".format(LP100_inst), font_size_values, fill=default_text_color)
            print_text_topleft(150, 30, "L/100", font_size_values, fill=default_text_color)
        else:
            print_text_topright(140, 30, "{:.1f}".format(LPH), font_size_values, fill=default_text_color)
            print_text_topleft(150, 30, "L/h", font_size_values, fill=default_text_color)

        # Print av speed trip
        print_text_topright(140, 75, "{:.1f}".format(average_speed_trip), font_size_values, fill=default_text_color)
        print_text_topleft(150, 75, "km/h av", font_size_values, fill=default_text_color)

        # Print trip L/100
        if odometer_trip > 0.1:
            lp100_to_print = "{:.1f}".format(LP100_trip)  # display Lp100km value after 0.1 km trip
        else:
            lp100_to_print = "-.-"
        print_text_topright(140, 115, lp100_to_print, font_size_values, fill=default_text_color)
        print_text_topleft(150, 115, "l/100", font_size_values, fill=default_text_color)

        # Print trip km
        print_text_topright(140, 155, "{:.1f}".format(odometer_trip), font_size_values, fill=default_text_color)
        print_text_topleft(150, 155, "km", font_size_values, fill=default_text_color)

        # Print trip L
        print_text_topright(140, 195, "{:.1f}".format(benz_potracheno_trip), font_size_values, fill=default_text_color)
        print_text_topleft(150, 195, "l", font_size_values, fill=default_text_color)

        # right side first row

        # print RPM
        print_text_topleft(500, 30, "rpm", font_size_values, fill=default_text_color)
        print_text_topright(490, 30, "{:.0f}".format(GET_RPM), font_size_values, fill=default_text_color)

        # print av speed full
        print_text_topleft(500, 75, "km/h av", font_size_values, fill=default_text_color)
        print_text_topright(490, 75, "{:.1f}".format(average_speed_full), font_size_values, fill=default_text_color)

        # print av L/100 full
        print_text_topleft(500, 115, "l/100 av", font_size_values, fill=default_text_color)
        print_text_topright(490, 115, "{:.1f}".format(LP100_full), font_size_values, fill=default_text_color)

        # print odometer full
        print_text_topleft(500, 155, "km", font_size_values, fill=default_text_color)
        print_text_topright(490, 155, "{:.1f}".format(odometer_full), font_size_values, fill=default_text_color)

        # print fuel litters full
        print_text_topleft(500, 195, "L", font_size_values, fill=default_text_color)
        print_text_topright(490, 195, "{:.1f}".format(benz_potracheno_full), font_size_values, fill=default_text_color)

        # sensors data - second row

        # Print screen title
        print_text_midtop(105, 235, "sensors", 30, fill=title_text_color)

        # Print long term fuel trim
        print_text_topright(140, 265, "{:+.1f}".format(GET_LONG_L), font_size_values, fill=default_text_color)
        print_text_topleft(150, 265, "% LTFT", font_size_values, fill=default_text_color)

        # Print MAF
        print_text_topright(140, 305, "{:.1f}".format(GET_MAF), font_size_values, fill=default_text_color)
        print_text_topleft(150, 305, "g/cm^3 MAF", font_size_values, fill=default_text_color)

        # Print trip L/100
        print_text_topright(140, 345, "{:.1f}".format(GET_LOAD), font_size_values, fill=default_text_color)
        print_text_topleft(150, 345, "% ENG LOAD", font_size_values, fill=default_text_color)

        # Print speed
        print_text_topright(140, 385, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)
        print_text_topleft(150, 385, "km/h", font_size_values, fill=default_text_color)

        # right side second row

        # print RPM
        print_text_topleft(500, 265, "% STFT", font_size_values, fill=default_text_color)
        print_text_topright(490, 265, "{:+.1f}".format(GET_SHORT_L), font_size_values, fill=default_text_color)

        # print volts
        if ELM_VOLTAGE < volts_alert:
            print_text_topleft(500, 305, "V", font_size_values, fill=alert_text_color)
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=alert_text_color)
        else:
            print_text_topleft(500, 305, "V", font_size_values, fill=default_text_color)
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=default_text_color)

        # print coolant temp
        degree_sign = u"\N{DEGREE SIGN}"
        if GET_TEMP > temp_alert:
            print_text_topleft(500, 345, degree_sign + "C", font_size_values, fill=alert_text_color)
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=alert_text_color)
        else:
            print_text_topleft(500, 345, '\u00b0' + "C", font_size_values, fill=default_text_color)
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=default_text_color)

        print_text_topleft(500, 385, "Write", font_size_values, fill=default_text_color)
        print_text_topright(490, 385, "{:.0f}".format(write_flash_counter), font_size_values, fill=default_text_color)

    # ############################### SCREEN 1 #########################################################
    if screen_number is 1:
        screen.blit(background_image, (0, 0))  # ?
        # Print screen title
        print_text_midtop(250, 0, "Sensors", 30, fill=title_text_color)

        # Print long term fuel trim
        print_text_topright(140, 30, "{:+.1f}".format(GET_LONG_L), font_size_values, fill=default_text_color)
        print_text_topleft(150, 30, "% LTFT", font_size_values, fill=default_text_color)

        # Print MAF
        print_text_topright(140, 115, "{:.1f}".format(GET_MAF), font_size_values, fill=default_text_color)
        print_text_topleft(150, 115, "g/cm^3 MAF", font_size_values, fill=default_text_color)

        # Print speed
        print_text_topright(140, 155, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)
        print_text_topleft(150, 155, "km/h", font_size_values, fill=default_text_color)

        # print RPM
        print_text_topleft(500, 30, "rpm", font_size_values, fill=default_text_color)
        print_text_topright(490, 30, "{:.0f}".format(GET_RPM), font_size_values, fill=default_text_color)

        # print RPM
        print_text_topleft(500, 265, "% STFT", font_size_values, fill=default_text_color)
        print_text_topright(490, 265, "{:+.1f}".format(GET_SHORT_L), font_size_values, fill=default_text_color)

        # print volts
        if ELM_VOLTAGE < volts_alert:
            print_text_topleft(500, 305, "V", font_size_values, fill=alert_text_color)
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=alert_text_color)
        else:
            print_text_topleft(500, 305, "V", font_size_values, fill=default_text_color)
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=default_text_color)

        # print coolant temp
        degree_sign = u"\N{DEGREE SIGN}"
        if GET_TEMP > temp_alert:
            print_text_topleft(500, 345, degree_sign + "C", font_size_values, fill=alert_text_color)
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=alert_text_color)
        else:
            print_text_topleft(500, 345, '\u00b0' + "C", font_size_values, fill=default_text_color)
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=default_text_color)

        print_text_topleft(500, 385, "wr_count", font_size_values, fill=default_text_color)
        print_text_topright(490, 385, "{:.0f}".format(write_flash_counter), font_size_values, fill=default_text_color)

    if screen_number is 10:
        print_text_midtop(343, 100, "OBDII adapter disconnected", 40, fill=alert_text_color)
    if screen_number is 11:
        print_text_midtop(343, 100, "CONNECTING...", 50, fill=default_text_color)
        pygame.display.flip()


def csv_read():
    # 0 - odometer
    # 1 - fuel
    # 2 - time
    try:
        with open(log_file, 'r', newline='') as f:
            data = csv.reader(f, delimiter=',')
            data_return = list(data)
            return data_return[0]
    except Exception as e:
        # if file doesn't exist - display message and create file
        # return ["0.0", "0.0", "0.0"]
        print(e)
        # screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        print_text_midtop(343, 235, "Can't read from log file", 50, fill=alert_text_color)
        print_text_midtop(343, 290, "No such file or directory", 50, fill=alert_text_color)
        pygame.display.flip()
        create_log_file()
        pygame.time.wait(10000)
        return ["0.0", "0.0", "0.0"]


def csv_write(odometer, benz, time_all):
    try:
        with open(log_file, 'w', newline='') as f:
            write = csv.writer(f)
            write.writerow([odometer, benz, time_all])
    except Exception as e:
        # If can't write in log file - display message, and print it in terminal
        print(e)
        # screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        print_text_midtop(343, 235, "Can't write in log file", 50, fill=alert_text_color)
        pygame.display.flip()
        pygame.time.wait(10000)


def create_log_file():
    # creating log file
    try:
        file = open(log_file, "w+")
        writer = csv.writer(file)
        writer.writerow(["0.0", "0.0", "0.0"])
        file.close()
    except Exception as e:
        # If can't create log file - display message, and print it in terminal
        print(e)
        # screen.fill(background_color)
        screen.blit(background_image, (0, 0))
        print_text_midtop(343, 235, "Can't create the log file", 50, fill=alert_text_color)
        pygame.display.flip()
        pygame.time.wait(10000)


def quit_app():
    global STOP_GET, STOP_PRINT, STOP_ACCEL
    STOP_GET = 0
    STOP_PRINT = 0
    STOP_ACCEL = 0


def connect():
    if platform.system().startswith("Windows"):
        connection_obj = obd.OBD("COM10")  # config for Windows OS
        return connection_obj
    else:
        # connection_obj = obd.OBD("/dev/ttyUSB0")  # connect to specific port in linux
        connection_obj = obd.OBD()
        return connection_obj  # return connection object in main loop


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((690, 463))  # set the resolution of app window or full screen mode

if not platform.system().startswith("Windows"):
    pygame.display.toggle_fullscreen()  # start the app in full screen mode on any os except Windows

done = False  # set the while exit-value for main loop
pygame.mouse.set_visible(False)  # do not display mouse cursor
screen.blit(background_image, (0, 0))
print_screen(11)  # display the connection message
connection = connect()  # initialize obd connection

# initialize thread for reading data from ECU
Thread_getValues = threading.Thread(target=get_values)
Thread_getValues.daemon = False
Thread_getValues.start()

if not platform.system().startswith("Windows"):
    Thread_getValues = threading.Thread(target=button_process)
    Thread_getValues.daemon = False
    Thread_getValues.start()

# checking is log file available or not. creating new one if not
if not os.path.isfile(log_file):
    create_log_file()

# do once to display average speed, fuel consumption before the ignition is on
# start
log_data = csv_read()
odometer_full = float(log_data[0])
benz_potracheno_full = float(log_data[1])
time_full = float(log_data[2])

if odometer_full > 0.1:  # 0.1 because too high values are displayed after reset log file
    LP100_full = (benz_potracheno_full / odometer_full) * 100.0
if time_full > 0:
    average_speed_full = odometer_full / (time_full / 3600.0)

# screen.fill(background_color)
screen.blit(background_image, (0, 0))
print_screen(0)  # display values on screen 0
# end

# main loop
while not done:
    # button_process()
    # don't need to calculate values if no connection with adapter
    if connection.status() != "Car Connected":
        screen.blit(background_image, (0, 0))
        # screen.fill(background_color)  # fill out the screen with color
        print_screen(10)  # print message
        connection = connect()  # try to reconnect
    else:
        # if connection with elm327 adapter is available
        # main loop
        if GET_RPM > engine_on_rpm:
            FuelFlowLitersPerSecond = 0.0
            odometer_add = 0.0

            if time_start == 0:
                time_start = time.time()
            if time_old == 0:
                time_old = time.time()  # do once after starting the app

            if GET_LOAD > 3:
                # convert fuel system status to int
                if GET_FUEL_STATUS == 'Closed loop, using oxygen sensor feedback to determine fuel mix':
                    fuel_status = True
                else:
                    fuel_status = False

                if fuel_status:  # if Closed Loop
                    # fuel correction by ShortTerm and LongTerm
                    ls_term_val = (100.0 + GET_LONG_L + GET_SHORT_L) / 100.0
                else:  # if open loop
                    # fuel correction trim by LongTerm
                    ls_term_val = (100.0 + GET_LONG_L) / 100.0

                FuelFlowGramsPerSecond = (GET_MAF / AirFuelRatio) * ls_term_val  # calculate gram of petrol per second
                # 14,7 air to 1 litter of gas, ls_term_val
                FuelFlowLitersPerSecond = FuelFlowGramsPerSecond / FuelDensityGramsPerLiter  # grams of petrol to L
                LPH = FuelFlowLitersPerSecond * 3600.0  # Litter per second to litter per hour

            # speed and odometer calculations
            time_trip = time.time() - time_start
            time_new = time.time()  # time from starting the app
            time1 = time_new - time_old  # * tcorrect  # time after the last speed calculating

            # if time1 > 10:
            #    time1 = 0

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
            # every 60 seconds on speeds 1...10km/h
            # every 30 seconds on speeds <= 1km/h
            # every 30 minutes on speeds > 10km/h
            if ((GET_SPEED > 1) and (GET_SPEED < 10) and ((time_new - time_old_gurnal) > 60)) or \
                    ((GET_SPEED <= 1) and ((time_new - time_old_gurnal) > 30)) or \
                    ((time_new - time_old_gurnal) > 1800):
                # read data from log file
                log_data = csv_read()
                odometer_eeprom = float(log_data[0]) + odometer_add_gurnal + odometer_add
                benz_eeprom = float(log_data[1]) + benz_add_gurnal + benz_add
                time_eeprom = float(log_data[2]) + time_add_gurnal + time1
                # Write new data in log file
                csv_write(odometer_eeprom, benz_eeprom, time_eeprom)

                # debug code for investigate with count of writing operations
                write_flash_counter += 1

                # calculations for avarage values
                odometer_full = odometer_eeprom
                benz_potracheno_full = benz_eeprom
                time_full = time_eeprom
                if odometer_full > 0:
                    LP100_full = (benz_potracheno_full / odometer_full) * 100.0
                if time_full > 0:
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

        # screen.fill(background_color)
        # uncomment for using background image
        screen.blit(background_image, (0, 0))
        print_screen(screen_counter)  # display values on screen 0

    # manage events to quit the application
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            done = True
            quit_app()
        if event.type == pygame.QUIT:
            done = True
            quit_app()
        if event.type == pygame.KEYDOWN:  # changing screen
            if screen_counter < screen_last:
                screen_counter += 1
            else:
                screen_counter = 0

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # set fps for the app
pygame.init()
sys.exit(0)
