#!/usr/bin/python


from __future__ import division
#import time
import threading
import time
import sys
import obd
import pygame

# uncomment for using background image
# background_image = pygame.image.load("toyota_logo4.jpg")

fuel_status = 4
engine_on_rpm = 400
time_start = 0
time1 = 0
time_new = 0
time_old = 0
time_old_gurnal = 0
benz_potracheno = 0
LP100 = 0.0
LP100_inst = 0.0
odometer = 0.0
odometer_add = 0.0
AirFuelRatio = 14.70
FuelDensityGramsPerLiter = 750.0
average_speed_trip = 0.0
time_trip = 0
LPH = 0.0

CONTROL_MODULE_VOLTAGE = 0.0
GET_MAF = 0.0
GET_RPM = 0
GET_SPEED = 0.0
GET_LOAD = 0.0
GET_SHORT_L = 0.0
GET_LONG_L = 0.0
GET_TEMP = 0
GET_FUEL_STATUS = ""

# variables for stopping application
STOP_ACCEL = 1
STOP_PRINT = 1
STOP_GET = 1


def print_text_topleft(x, y, text, size, fill):
    # font = pygame.font.Font('font/ubuntu/UbuntuMono-B.ttf', size)
    font = pygame.font.Font('font/ds_digital/DS-DIGIB.TTF', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.topleft = (x, y)
    screen.blit(puttext, textRect)


def print_text_topright(x, y, text, size, fill):
    # font = pygame.font.Font('font/ubuntu/UbuntuMono-B.ttf', size)
    font = pygame.font.Font('font/ds_digital/DS-DIGIB.TTF', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.topright = (x, y)
    screen.blit(puttext, textRect)


def print_text_midtop(x, y, text, size, fill):
    # font = pygame.font.Font('font/ubuntu/UbuntuMono-B.ttf', size)
    font = pygame.font.Font('font/ds_digital/DS-DIGIB.TTF', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.midtop = (x, y)
    screen.blit(puttext, textRect)


def get_values():
    global GET_FUEL_STATUS, GET_TEMP, GET_RPM, GET_SPEED, GET_LOAD, GET_SHORT_L, GET_LONG_L, GET_MAF, \
        CONTROL_MODULE_VOLTAGE

    while STOP_GET:
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_RPM = response.value.magnitude

        cmd = obd.commands.MAF # select an OBD command (sensor)
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

        cmd = obd.commands.ABSOLUTE_LOAD  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LOAD_ABS = response.value.magnitude

        cmd = obd.commands.COOLANT_TEMP  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_TEMP = response.value.magnitude

        cmd = obd.commands.FUEL_STATUS  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_FUEL_STATUS = response.value[0]

        cmd = obd.commands.CONTROL_MODULE_VOLTAGE
        response = connection.query(cmd)
        if response.value is not None:
            CONTROL_MODULE_VOLTAGE = response.value.magnitude


def print_fuel_status_string():
    if GET_FUEL_STATUS is not None:
        print_text_topleft(0, 500, GET_FUEL_STATUS, 30, fill=(255, 255, 55))


def print_screen(screen_number):
    if screen_number is 0:

        # Print screen title
        print_text_topleft(150, 0, "trip odometer", 30, fill=(42, 157, 1))
        print_text_topleft(500, 0, "odometer", 30, fill=(42, 157, 1))

        # Print av speed
        print_text_topright(140, 30, "{:.1f}".format(average_speed_trip), 40, fill=(2, 135, 178))
        print_text_topleft(150, 30, "km/h av", 40, fill=(2, 135, 178))

        # Print L/h or instant L/100km in motion
        if GET_SPEED > 0:
            print_text_topright(140, 75, "{:.1f}".format(LP100_inst), 40, fill=(2, 135, 178))
            print_text_topleft(150, 75, "L/100", 40, fill=(2, 135, 178))
        else:
            print_text_topright(140, 75, "{:.1f}".format(LPH), 40, fill=(2, 135, 178))
            print_text_topleft(150, 75, "L/h", 40, fill=(2, 135, 178))

        # Print trip L/100
        if odometer > 0.1:
            lp100_to_print = "{:.1f}".format(LP100)  # display Lp100km value after 0.1 km trip
        else:
            lp100_to_print = "-.-"
        print_text_topright(140, 115, lp100_to_print, 40, fill=(2, 135, 178))
        print_text_topleft(150, 115, "l/100", 40, fill=(2, 135, 178))

        # Print trip km
        print_text_topright(140, 155, "{:.1f}".format(odometer), 40, fill=(2, 135, 178))
        print_text_topleft(150, 155, "km", 40, fill=(2, 135, 178))

        # Print trip L
        print_text_topright(140, 195, "{:.2f}".format(benz_potracheno), 40, fill=(2, 135, 178))
        print_text_topleft(150, 195, "l", 40, fill=(2, 135, 178))

        ### right side ###

        # print RPM
        print_text_topleft(500, 30, "rpm", 40, fill=(2, 135, 178))
        print_text_topright(490, 30, "{:.0f}".format(GET_RPM), 40, fill=(2, 135, 178))

        # print volts
        print_text_topleft(500, 75, "km/h av speed", 40, fill=(2, 135, 178))
        print_text_topright(490, 75, "{:.1f}".format(average_speed_trip), 40, fill=(2, 135, 178))

        # print coolant temp
        print_text_topleft(500, 115, "value", 40, fill=(2, 135, 178))
        print_text_topright(490, 115, "{:.0f}".format(GET_TEMP), 40, fill=(2, 135, 178))

        # print trip fuel litters
        print_text_topleft(500, 155, "L", 40, fill=(2, 135, 178))
        print_text_topright(490, 155, "{:.2f}".format(benz_potracheno), 40, fill=(2, 135, 178))

        # print trip fuel litters
        print_text_topleft(500, 195, "L", 40, fill=(2, 135, 178))
        print_text_topright(490, 195, "{:.2f}".format(benz_potracheno), 40, fill=(2, 135, 178))

        ### sensors data ###

        # Print screen title
        print_text_midtop(400, 235, "SENSORS", 30, fill=(42, 157, 1))

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

        ### right side ###

        # print RPM
        print_text_topleft(500, 265, "% STFT", 40, fill=(2, 135, 178))
        print_text_topright(490, 265, "{:+.1f}".format(GET_SHORT_L), 40, fill=(2, 135, 178))

        # print volts
        print_text_topleft(500, 305, "V", 40, fill=(2, 135, 178))
        print_text_topright(490, 305, "{:.1f}".format(CONTROL_MODULE_VOLTAGE), 40, fill=(2, 135, 178))

        # print coolant temp
        print_text_topleft(500, 345, "C", 40, fill=(2, 135, 178))
        print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), 40, fill=(2, 135, 178))

        # print rpm
        print_text_topleft(500, 385, "RPM", 40, fill=(2, 135, 178))
        print_text_topright(490, 385, "{:.0f}".format(GET_RPM), 40, fill=(2, 135, 178))


def quit():
    global STOP_GET, STOP_PRINT, STOP_ACCEL
    STOP_GET = 0
    STOP_PRINT = 0
    STOP_ACCEL = 0


pygame.init()
clock = pygame.time.Clock()
# screen = pygame.display.set_mode((800, 480))
screen = pygame.display.set_mode((800, 540))
# pygame.display.toggle_fullscreen()
done = False
pygame.mouse.set_visible(False)

# connection = obd.OBD("/dev/ttyUSB0")  # auto-connects to USB or RF port
connection = obd.OBD("COM10") # config for Windows OS


Thread_getValues = threading.Thread(target=get_values)
Thread_getValues.daemon = False
Thread_getValues.start()

while not done:

    if GET_RPM > engine_on_rpm:
        FuelFlowLitersPerSecond = 0.0
        odometer_add = 0.0
        if GET_LOAD > 3:
            if GET_FUEL_STATUS == 'Closed loop, using oxygen sensor feedback to determine fuel mix':
                fuel_status = 2
            else:
                fuel_status = 4

            if fuel_status == 2:  # { // если замкнутая обратная связь  - Closed Loop
                ls_term_val = (100.0 + GET_LONG_L + GET_SHORT_L) / 100.0 # коэффициент корректировки расхода по ShortTerm и LongTerm
            else:
                ls_term_val = (100.0 + GET_LONG_L) / 100.0 # коэффициент корректировки расхода по LongTerm

            FuelFlowGramsPerSecond = (GET_MAF / AirFuelRatio) * ls_term_val  # calculate gram of petrol per second
            # соотношении 14,7 воздуха/к 1 литра бензина, корректировка ls_term_val
            FuelFlowLitersPerSecond = FuelFlowGramsPerSecond / FuelDensityGramsPerLiter  # grams of petrol to litters
            LPH = FuelFlowLitersPerSecond * 3600.0  # Litter per second to litter per hour

        # speed and odometr calculations
        if time_start == 0:
            time_start = time.time()

        time_trip = time.time() - time_start

        if time_old == 0:
            time_old = time.time()  # выполнится один раз при появлении оборотов

        time_new = time.time()   # время со старта программы в мс
        time1 = time_new - time_old  # * tcorrect  #// прошло время с последнего расчета скорости, расхода  - в сек

        if time1 > 10:
            time1 = 0

        time_old = time_new  # записать новое время для сравнения в следующем цикле



        benz_add = FuelFlowLitersPerSecond * time1
        benz_potracheno = benz_potracheno + benz_add  # общий расход в литрах

        if GET_SPEED > 0:
            odometer_add = (((GET_SPEED * 1000.0) / 3600.0) * time1) / 1000.0  # ???
            odometer = odometer + odometer_add  # обший пробег в км
            if odometer_add > 0:
                LP100_inst = (benz_add / odometer_add) * 100.0  # instant fuel consumption

        if odometer > 0 and time_trip > 0:
            average_speed_trip = odometer / (time_trip / 3600.0)
            #LP100_inst = (benz_add / odometer_add) * 100.0  # instant fuel consumption
    else:
        if GET_SPEED == 0:
            time_start = 0
            time_trip = 0
            odometer = 0
            benz_potracheno = 0

    if odometer > 0:
        LP100 = (benz_potracheno / odometer) * 100.0  # расход бензина на 100 км (в литрах) за поездку

    # manage events to quit the application
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            done = True
            quit()
        if event.type == pygame.QUIT:
            done = True
            quit()

    screen.fill((0, 20, 0))
    # uncomment for using background image
    # screen.blit(background_image, (0, 0))
    print_screen(0)  # display values on screen 0
    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(60)  # set fps for the app
pygame.init()
sys.exit(0)
