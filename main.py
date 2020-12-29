#!/usr/bin/python


from __future__ import division
#import time
import threading
import time
import sys
import obd
import pygame

background_image = pygame.image.load("toyota_logo1.png")

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
odometr = 0.0
odometr_add = 0.0
AirFuelRatio = 14.70
FuelDensityGramsPerLiter = 750.0
sp = 0.0
average_speed_trip = 0.0
time_trip = 0
LPH = 0.0

CONTROL_MODULE_VOLTAGE = 0.0
GET_MAF = 0.0
STOP_ACCEL = 1
STOP_PRINT = 1
STOP_GET = 1
GET_RPM = 0
GET_SPEED = 0.0
GET_LOAD = 0.0
GET_SHORT_L = 0.0
GET_LONG_L = 0.0
GET_TEMP = 0
GET_FUEL_STATUS = ""


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
    global GET_AFR, GET_FUEL_LEVEL, GET_SPEED_EXACTLY, GET_FUEL_STATUS, GET_TEMP, GET_RPM, GET_SPEED, GET_LOAD, \
        GET_LOAD_ABS, GET_THROTTLE, GET_THROTTLE_ABS, GET_SHORT_L, GET_LONG_L, GET_TIMING, GET_KNOCK, GET_MAF, CONTROL_MODULE_VOLTAGE
    while STOP_GET:
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_RPM = response.value.magnitude

        cmd = obd.commands.MAF # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            # GET_MAF = str_int(str(response.value))
            GET_MAF = response.value.magnitude

        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SPEED_EXACTLY = response.value
            # GET_SPEED = str_int(str(response.value))
            GET_SPEED = response.value.magnitude

        cmd = obd.commands.SHORT_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            # GET_SHORT_L = str_int(str(response.value), 1)
            GET_SHORT_L = response.value.magnitude

        cmd = obd.commands.LONG_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            # GET_LONG_L = str_int(str(response.value), 1)
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
        print_text_topleft(0, 400, GET_FUEL_STATUS, 30, fill=(255, 255, 55))


def print_screen(screen_number):
    if screen_number is 0:

        # Print screen title
        print_text_midtop(400, 0, "TRIP INFO", 30, fill=(42, 157, 1))

        # Print speed
        # print_text_topright(90, 40, str(GET_SPEED), 40, fill=(2, 135, 178))
        print_text_topright(140, 40, "{:.0f}".format(GET_SPEED), 40, fill=(2, 135, 178))
        print_text_topleft(150, 40, "km/h", 40, fill=(2, 135, 178))

        # Print L/h or instant L/100km in motion
        if sp > 0:
            print_text_topright(140, 85, "{:.1f}".format(LP100_inst), 40, fill=(2, 135, 178))
            print_text_topleft(150, 85, "L/100", 40, fill=(2, 135, 178))
        else:
            print_text_topright(140, 85, "{:.1f}".format(LPH), 40, fill=(2, 135, 178))
            print_text_topleft(150, 85, "L/h", 40, fill=(2, 135, 178))

        # Print trip L/100
        if odometr > 0.1: # отображать расход на 100 км только после 100 метров пробега
            lp100_to_print = "{:.1f}".format(LP100)  # display Lp100km value after 0.1 km trip
        else:
            lp100_to_print = "-.-"
        print_text_topright(140, 125, lp100_to_print, 40, fill=(2, 135, 178))
        print_text_topleft(150, 125, "L/100", 40, fill=(2, 135, 178))

        # Print trip km
        print_text_topright(140, 165, "{:.1f}".format(odometr), 40, fill=(2, 135, 178))
        print_text_topleft(150, 165, "km", 40, fill=(2, 135, 178))

        ### right side ###

        # print RPM
        print_text_topleft(500, 40, "rpm", 40, fill=(2, 135, 178))
        print_text_topright(490, 40, "{:.0f}".format(GET_RPM), 40, fill=(2, 135, 178))

        # print volts
        print_text_topleft(500, 85, "km/h av speed", 40, fill=(2, 135, 178))
        print_text_topright(490, 85, "{:.1f}".format(average_speed_trip), 40, fill=(2, 135, 178))

        # print coolant temp
        print_text_topleft(500, 125, "C", 40, fill=(2, 135, 178))
        print_text_topright(490, 125, "{:.0f}".format(GET_TEMP), 40, fill=(2, 135, 178))

        # print trip fuel litters
        print_text_topleft(500, 165, "L", 40, fill=(2, 135, 178))
        print_text_topright(490, 165, "{:.1f}".format(benz_potracheno), 40, fill=(2, 135, 178))

        ### sensors data ###

        # Print screen title
        print_text_midtop(400, 210, "SENSORS", 30, fill=(42, 157, 1))

        # Print long term fuel trim
        print_text_topright(140, 250, "{:+.1f}".format(GET_LONG_L), 40, fill=(2, 135, 178))
        print_text_topleft(150, 250, "% LTFT", 40, fill=(2, 135, 178))

        # Print MAF
        print_text_topright(140, 290, "{:.2f}".format(GET_MAF), 40, fill=(2, 135, 178))
        print_text_topleft(150, 290, "g/cm^3", 40, fill=(2, 135, 178))

        # Print trip L/100
        print_text_topright(140, 330, "{:.1f}".format(LP100), 40, fill=(2, 135, 178))
        print_text_topleft(150, 330, "L/100", 40, fill=(2, 135, 178))

        # Print trip km
        print_text_topright(140, 370, "{:.1f}".format(odometr), 40, fill=(2, 135, 178))
        print_text_topleft(150, 370, "km", 40, fill=(2, 135, 178))

        ### right side ###

        # print RPM
        print_text_topleft(500, 250, "% STFT", 40, fill=(2, 135, 178))
        print_text_topright(490, 250, "{:+.1f}".format(GET_SHORT_L), 40, fill=(2, 135, 178))

        # print volts
        print_text_topleft(500, 290, "V", 40, fill=(2, 135, 178))
        print_text_topright(490, 290, "{:.1f}".format(CONTROL_MODULE_VOLTAGE), 40, fill=(2, 135, 178))

        # print coolant temp
        print_text_topleft(500, 330, "C", 40, fill=(2, 135, 178))
        print_text_topright(490, 330, "{:.0f}".format(GET_TEMP), 40, fill=(2, 135, 178))

        # print fuel status
        print_text_topleft(500, 370, "fuel status", 40, fill=(2, 135, 178))
        print_text_topright(490, 370, str(fuel_status), 40, fill=(2, 135, 178))


def quit():
    global STOP_GET, STOP_PRINT, STOP_ACCEL
    STOP_GET = 0
    STOP_PRINT = 0
    STOP_ACCEL = 0


pygame.init()
clock = pygame.time.Clock()
# screen = pygame.display.set_mode((800, 480))
screen = pygame.display.set_mode((800, 500))
# pygame.display.toggle_fullscreen()
done = False
pygame.mouse.set_visible(False)

# connection = obd.OBD("/dev/ttyUSB0")  # auto-connects to USB or RF port
connection = obd.OBD("COM10") # config for Windows OS


Thread_getValues = threading.Thread(target=get_values)
Thread_getValues.daemon = False
Thread_getValues.start()

while not done:
    rpm_var = GET_RPM
    if rpm_var > engine_on_rpm:

        sp = GET_SPEED  # получить скорость
        MAF = GET_MAF  # get Air Flow Rate (MAF)
        long_term_val = GET_LONG_L
        short_term_val = GET_SHORT_L

        if GET_FUEL_STATUS == 'Closed loop, using oxygen sensor feedback to determine fuel mix':
            fuel_status = 2
        else:
            fuel_status = 4

        if fuel_status == 2:  # { // если замкнутая обратная связь  - Closed Loop
            ls_term_val = (100.0 + long_term_val + short_term_val) / 100.0 # коэффициент корректировки расхода по ShortTerm и LongTerm

        else:
            ls_term_val = (100.0 + long_term_val) / 100.0 # коэффициент корректировки расхода по LongTerm

        FuelFlowGramsPerSecond = (MAF / AirFuelRatio) * ls_term_val  # Получаем расход грамм бензина в секунду в
        # соотношении 14,7 воздуха/к 1 литра бензина, корректировка ls_term_val
        FuelFlowLitersPerSecond = FuelFlowGramsPerSecond / FuelDensityGramsPerLiter  # Переводим граммы бензина в литры
        LPH = FuelFlowLitersPerSecond * 3600.0  # Ковертирование литров в час

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

        if sp > 0:
            odometr_add = (((sp * 1000.0) / 3600.0) * time1) / 1000.0  # ???
            odometr = odometr + odometr_add  # обший пробег в км

        benz_add = FuelFlowLitersPerSecond * time1
        benz_potracheno = benz_potracheno + benz_add  # общий расход в литрах

        if odometr > 0 and time_trip > 0:
            average_speed_trip = odometr / (time_trip / 3600.0)
            LP100_inst = (benz_add / odometr_add) * 100.0  # instant fuel consumption

    if odometr > 0:
        LP100 = (benz_potracheno / odometr) * 100.0  # расход бензина на 100 км (в литрах) за поездку

    # manage events to quit the application
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            done = True
            quit()
        if event.type == pygame.QUIT:
            done = True
            quit()

    screen.fill((0, 35, 0))
    #screen.blit(background_image, (0, 0))
    print_screen(0)  # display values on screen 0

    pygame.display.flip()
    #pygame.display.update()
    clock.tick(60)
pygame.init()
sys.exit(0)
