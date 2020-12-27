#!/usr/bin/python


from __future__ import division
import time
import threading
import time
import sys
import obd
import pygame

time_new = 0
time_old = 0
time_old_gurnal = 0
odometr = 0
odometr_add = 0
benz_potracheno = 0

STOP_ACCEL = 1
STOP_PRINT = 1
STOP_GET = 1
GET_RPM = "0"
GET_SPEED = "0"
GET_SPEED_EXACTLY = 0.0
GET_LOAD = "0"
GET_LOAD_ABS = "0"
GET_THROTTLE = "0"
GET_THROTTLE_ABS = "0"
GET_SHORT_L = "0"
GET_LONG_L = "0"
GET_TIMING = "00.0"
GET_KNOCK = "00.0"
GET_TEMP = "0"
GET_FUEL_STATUS = " "
GET_FUEL_LEVEL = "0"
GET_AFR = "0"
GET_ACCEL = 0.0
TIME_START = 0.0
TIME_FINISH = 0.0
START_MEASURE = False
V0 = 0.0
V1 = 0.0
GET_DISTANCE = 0.0


def print_text(x, y, text, size, fill):
    font = pygame.font.SysFont("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", size)
    # font = pygame.font.Font('freesansbold.ttf', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.topleft = (x, y)
    screen.blit(puttext, textRect)


def print_text_topleft(x, y, text, size, fill):
    # font = pygame.font.SysFont("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", size)
    font = pygame.font.Font('UbuntuMono-B.ttf', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.topleft = (x, y)
    screen.blit(puttext, textRect)


def print_text_topright(x, y, text, size, fill):
    # font = pygame.font.SysFont("/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf", size)
    font = pygame.font.Font('UbuntuMono-B.ttf', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.topright = (x, y)
    screen.blit(puttext, textRect)


def print_text_midtop(x, y, text, size, fill):
    # font = pygame.font.SysFont("/ubuntu-font-family-0.83/UbuntuMono-B.ttf", size)
    # font = pygame.font.Font('freesansbold.ttf', size)
    font = pygame.font.Font('UbuntuMono-B.ttf', size)
    puttext = font.render(text, True, fill)
    textRect = puttext.get_rect()
    textRect.midtop = (x, y)
    screen.blit(puttext, textRect)


def str_int(str, digits=0):
    index = str.find(".")
    if index == -1:
        return str
    if index > 0:
        if digits > 0:
            return str[0:index + digits + 1]
        return str[0:index]
    return "0"


def get_values():
    global GET_AFR, GET_FUEL_LEVEL, GET_SPEED_EXACTLY, GET_FUEL_STATUS, GET_TEMP, GET_RPM, GET_SPEED, GET_LOAD, \
        GET_LOAD_ABS, GET_THROTTLE, GET_THROTTLE_ABS, GET_SHORT_L, GET_LONG_L, GET_TIMING, GET_KNOCK
    while STOP_GET:
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_RPM = str_int(str(response.value))

        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SPEED_EXACTLY = response.value
            GET_SPEED = str_int(str(response.value))

        cmd = obd.commands.TIMING_ADVANCE  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_TIMING = str_int(str(response.value), 1)

        # 2
        cmd = obd.commands.SHORT_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SHORT_L = str_int(str(response.value), 1)
        # -----------------------------------------------------------------------------------
        cmd = obd.commands.RELATIVE_THROTTLE_POS  # select an OBD command (sensor)
        # cmd = obd.commands.INTAKE_PRESSURE # select an OBD command (sensor)

        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_THROTTLE = str_int(str(response.value))
        # -----------------------------------------------------------------------------------
        # GET_THROTTLE=chDt.get()

        cmd = obd.commands.THROTTLE_POS  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_THROTTLE_ABS = str_int(str(response.value))
        # 3
        cmd = obd.commands.LONG_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LONG_L = str_int(str(response.value), 1)

        cmd = obd.commands.ENGINE_LOAD  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LOAD = str_int(str(response.value))

        cmd = obd.commands.ABSOLUTE_LOAD  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LOAD_ABS = str_int(str(response.value))
        # 4
        cmd = obd.commands.COOLANT_TEMP  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_TEMP = str_int(str(response.value))

        cmd = obd.commands.FUEL_STATUS  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_FUEL_STATUS = response.value


def print_rpm():
    # print GET_RPM,"++"
    print_text(25, 5, GET_RPM, 75, fill=(255, 55, 55))
    print_text(25, 50, "engine rpm", 30, fill=(255, 55, 55))


def print_speed():
    print_text(200, 5, GET_SPEED, 75, fill=(255, 0, 155))
    print_text(190, 50, "speed km/h", 30, fill=(255, 0, 155))


def print_timing():
    # print_text( (350, 5), GET_TIMING,  55, fill=(150,150,255))
    print_text(350, 5, GET_TIMING, 55, fill=(0, 81, 255))
    # print_text((340, 50), "timing adv. %",  30, fill=(150,150,255))


def print_knock():
    print_text(350, 40, GET_KNOCK, 55, fill=(255, 255, 255))
    # print_text((340, 50), "timing adv. %",  30, fill=(150,150,255))


# secont raw
def print_short_l():
    print_text(50, 80, GET_SHORT_L, 75, fill=(0, 255, 0))
    print_text(2, 130, "fuel trim short%", 30, fill=(0, 255, 0))


def print_throttle():
    print_text(200, 80, GET_THROTTLE, 75, fill=(150, 150, 255))
    print_text(190, 130, "throttle %", 30, fill=(150, 150, 255))


def print_throttle_abs():
    print_text(355, 80, GET_THROTTLE_ABS, 75, fill=(150, 150, 255))
    print_text(330, 130, "throttle abs %", 30, fill=(150, 150, 255))


# third row
def print_long_l():
    print_text(55, 160, GET_LONG_L, 75, fill=(0, 255, 0))
    print_text(5, 210, "fuel trim long%", 30, fill=(0, 255, 0))


def print_load():
    print_text(200, 155, GET_LOAD, 75, fill=(255, 255, 0))
    print_text(190, 210, "calc loadc %", 30, fill=(255, 255, 0))


def print_load_abs():
    print_text(355, 155, GET_LOAD_ABS, 75, fill=(255, 255, 0))
    print_text(350, 210, "abs load %", 30, fill=(255, 255, 0))


# fourth row
def print_temp():
    print_text(50, 240, GET_TEMP, 75, fill=(255, 0, 0))
    print_text(10, 290, "temperature C", 30, fill=(255, 0, 0))


def print_fuel_status():
    fuel_color = (255, 255, 255)
    #    print_text( (165, 240),"Open loop acceleration",  30, fill=fuel_color)

    if GET_FUEL_STATUS is not None:
        out_text = "not Known status"

        if GET_FUEL_STATUS == 2:
            out_text = "Closed normal"
            fuel_color = (55, 255, 55)

        if GET_FUEL_STATUS == 1:
            out_text = "Open temp"
            fuel_color = (55, 55, 255)

        if GET_FUEL_STATUS == 4:
            out_text == "Open load"
            fuel_color = (255, 255, 55)

        if GET_FUEL_STATUS == 8:
            out_text = "Open failure"
            fuel_color = (255, 55, 55)

        if GET_FUEL_STATUS == 16:
            out_text = "Closed failure"
            fuel_color = (255, 55, 55)

        print_text(165, 290, out_text, 30, fill=fuel_color)

    if GET_AFR is not None:
        print_text(170, 240, GET_AFR, 75, fill=(255, 255, 55))
    print_text(290, 250, GET_FUEL_LEVEL + "l", 30, fill=(255, 255, 255))


def print_accel():
    calc_accel()

    if not START_MEASURE:
        print_text(360, 250, str(GET_ACCEL), 45, fill=(0, 255, 0))
        print_text(360, 280, str(GET_DISTANCE), 45, fill=(255, 255, 55))
    else:
        print_text(360, 250, "00.--", 45, fill=(0, 255, 0))
        print_text(360, 280, "00.--", 45, fill=(255, 255, 55))


def calc_accel():
    global V0, V1, GET_DISTANCE, GET_ACCEL, TIME_START, TIME_FINISH, START_MEASURE
    #                if (int(GET_THROTTLE_ABS)>=70) and (int(GET_SPEED)>=30) and (START_MEASURE==False) :
    if (int(GET_THROTTLE_ABS) >= 45) and (START_MEASURE == False):
        TIME_START = time.time()
        V0 = GET_SPEED_EXACTLY * 1000 / 3600
        START_MEASURE = True
    if (int(GET_THROTTLE_ABS) < 40) and (START_MEASURE == True):
        TIME_FINISH = time.time()
        V1 = GET_SPEED_EXACTLY * 1000 / 3600
        GET_ACCEL = round(TIME_FINISH - TIME_START, 2)
        GET_DISTANCE = round(((V0 + V1) / 2) * GET_ACCEL, 2)
        START_MEASURE = False


def print_fuel_status_string():
    if GET_FUEL_STATUS is not None:
        print_text(0, 400, str(GET_FUEL_STATUS), 30, fill=(255, 255, 55))


def print_screen(screen_number):
    if screen_number is 0:

        # Print screen title
        print_text_midtop(400, 0, "MAIN INFO", 30, fill=(42, 157, 1))

        # Print speed
        print_text_topright(90, 40, GET_SPEED, 40, fill=(2, 135, 178))
        print_text_topleft(100, 40, "km/h", 40, fill=(2, 135, 178))

        # Print L/h
        if odometr > 0.1: # отображать расход на 100 км только после 100 метров пробега
            lp100_to_print = LP100
        else:
            lp100_to_print = "-.--"
        print_text_topright(90, 85, lp100_to_print, 40, fill=(2, 135, 178))
        print_text_topleft(100, 85, "L/h", 40, fill=(2, 135, 178))

        # Print trip L/100
        print_text_topright(90, 125, "val", 40, fill=(2, 135, 178))
        print_text_topleft(100, 125, "L/100", 40, fill=(2, 135, 178))

        # Print trip km
        print_text_topright(90, 165, "val", 40, fill=(2, 135, 178))
        print_text_topleft(100, 165, "km", 40, fill=(2, 135, 178))

        ### right side ###

        # print RPM
        print_text_topleft(500, 40, "rpm", 40, fill=(2, 135, 178))
        print_text_topright(490, 40, GET_RPM, 40, fill=(2, 135, 178))

        # print volts
        print_text_topleft(500, 85, "V", 40, fill=(2, 135, 178))
        print_text_topright(490, 85, "value", 40, fill=(2, 135, 178))

        # print coolant temp
        print_text_topleft(500, 125, "C", 40, fill=(2, 135, 178))
        print_text_topright(490, 125, GET_TEMP, 40, fill=(2, 135, 178))

        # print trip fuel litters
        print_text_topleft(500, 165, "L", 40, fill=(2, 135, 178))
        print_text_topright(490, 165, "value", 40, fill=(2, 135, 178))


def quit():
    global STOP_GET, STOP_PRINT, STOP_ACCEL
    STOP_GET = 0
    STOP_PRINT = 0
    STOP_ACCEL = 0


pygame.init()
clock = pygame.time.Clock()
# screen = pygame.display.set_mode((800, 480))
screen = pygame.display.set_mode((800, 600))
# pygame.display.toggle_fullscreen()
done = False
pygame.mouse.set_visible(False)

# connection = obd.OBD("/dev/ttyUSB0")  # auto-connects to USB or RF port
connection = obd.OBD("COM7") # config for Windows OS

Thread_getValues = threading.Thread(target=get_values)
Thread_getValues.daemon = False
Thread_getValues.start()

while not done:
    if odometr > 0:
        LP100 = (benz_potracheno / odometr) * 100.0  # расход бензина на 100 км (в литрах)

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            done = True
            quit()
        if event.type == pygame.QUIT:
            done = True
            quit()

    screen.fill((0, 0, 0))

    print_screen(0)

    # print_speed()
    # print_temp()
    # print_short_l()
    # print_long_l()
    # print_fuel_status()
    # print_fuel_status_string()
    # print_timing()
    # print_knock()
    # print_throttle()
    # print_throttle_abs()
    # print_load()
    # print_load_abs()
    # print_accel()
    # print_rpm()

    pygame.display.flip()
    clock.tick(60)
pygame.init()
sys.exit(0)
