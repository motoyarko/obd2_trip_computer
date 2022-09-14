#!/usr/bin/python

# Thanks to:
# https://sohabr.net/habr/post/252207/
# https://www.drive2.ru/l/481530293824520264/


"""
Autostart:

sudo nano /etc/xdg/lxsession/LXDE-pi/autostart 
insert before last line
/usr/bin/python3 /home/pi/obd2_trip_computer/main.py
"""
# from mutagen import mp3
from __future__ import division
import os
import threading
import time
import sys
import obd
import pygame
import csv
import platform
import time
from gpiozero import Button
from omxshuffle import get_playlist, play_info_read, play_info_write, playlist_write
import random

# import asyncio
c = threading.Condition()

playlist_normal, playlist_shuffled = get_playlist()
# playlist_normal = get_playlist()[0]
debug_on = True

song_title = ""
song_number = 0
song_total = 0
playlist_shuffle = True

com_port = "COM2"
global screen_counter
screen_counter = 0
screen_last = 2
fuel_status = False
engine_on_rpm = 200
time_start = 0
time_loop = 0
time_new = 0
time_old = 0
fuel_used_trip = 0
LP100_trip = 0.0
LP100_inst = 0.0
odometer_trip = 0.0
odometer_add_loop = 0.0
AirFuelRatio = 14.70
FuelDensityGramsPerLiter = 750.0
average_speed_trip = 0.0
time_trip = 0
LPH = 0.0
LP100_full = 0.0
odometer_full = 0.0
fuel_used_full = 0.0
# motor_time_full = 0
volts_alert = 12.6
temp_alert_high = 100.0
temp_alert_low = 50.0
# font_file = 'UbuntuMono-B.ttf'
# font_file = "/home/pi/obd2_trip_computer/Audiowide-Regular.ttf"
font_size_values = 35

# Different sources of the background image depending of platform. It is needed for startup on raspberry. TBC
if platform.system().startswith("Windows"):
    background_image = pygame.image.load("background_image.bmp")
    background_image_music_player = pygame.image.load("background_image_music_player.bmp")
    log_file = 'log.csv'
    font_file = "Audiowide-Regular.ttf"
    playlist_file = 'playlist.pls'
    playlist_file_shuffled = 'playlist_shuffled.pls'
    play_info_file = 'play_info.pls'
else:
    background_image = pygame.image.load("/home/pi/obd2_trip_computer/background_image.bmp")
    background_image_music_player = pygame.image.load("/home/pi/obd2_trip_computer/background_image_music_player.bmp")
    log_file = '/home/pi/obd2_trip_computer/log.csv'
    font_file = "/home/pi/obd2_trip_computer/Audiowide-Regular.ttf"
    playlist_file = '/home/pi/obd2_trip_computer/playlist.txt'
    playlist_file_shuffled = '/home/pi/obd2_trip_computer/playlist_shuffled.txt'
    play_info_file = '/home/pi/obd2_trip_computer/play_info.txt'

time_old_journal = 0
odometer_add_journal = 0.0
fuel_add_journal = 0.0
time_add_journal = 0.0
time_full = 0.0
average_speed_full = 0.0
odometer_eeprom = 0.0
benz_eeprom = 0.0
time_eeprom = 0.0
#default_text_color = (102, 102, 102)
default_text_color = (230, 230, 230)
# default_text_color = (0, 0, 0)
alert_text_color = (235, 7, 49)
cold_text_color = (54, 47, 191)
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
CVT_TEMP = 0.0

# variables for stopping application
STOP_ACCELERATION = 1
STOP_PRINT = 1
STOP_GET = 1
STOP_PLAYER = 1


def stop_play():
    pygame.mixer.music.fadeout(1000)
    if debug_on: print("next song")


def button_process():
    global screen_counter
    if screen_counter < screen_last:
        screen_counter += 1
    else:
        screen_counter = 0


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
    # font = pygame.font.Font(font_file, size)
    font = pygame.font.Font(None, size)
    puttext = font.render(text, True, fill)
    text_rect = puttext.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(puttext, text_rect)


def get_values():
    from obd import OBDCommand
    from obd.protocols import ECU
    global GET_FUEL_STATUS, GET_TEMP, GET_RPM, GET_SPEED, GET_LOAD, GET_SHORT_L, GET_LONG_L, GET_MAF, ELM_VOLTAGE, CVT_TEMP

    def decode(messages):
        """ decoder for CVT temp messages """
        d = messages[0].data  # only operate on a single message
        d = d[15]  # Select single bit N
        N = d
        print("N: " + str(N))  # Real value of temp
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

    connection.supported_commands.add(cvt_temp_command)
    while STOP_GET:
        cmd = obd.commands.RPM  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_RPM = response.value.magnitude
        else:
            GET_RPM = 0.0

        if not STOP_GET:
            break

        cmd = obd.commands.MAF  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_MAF = response.value.magnitude
        else:
            GET_MAF = 0.0

        if not STOP_GET:
            break

        cmd = obd.commands.SPEED  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SPEED = response.value.magnitude
        else:
            GET_SPEED = 0.0

        if not STOP_GET:
            break

        cmd = obd.commands.SHORT_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_SHORT_L = response.value.magnitude
        else:
            GET_SHORT_L = 0.0

        if not STOP_GET:
            break

        cmd = obd.commands.LONG_FUEL_TRIM_1  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LONG_L = response.value.magnitude
        else:
            GET_LONG_L = 0.0

        if not STOP_GET:
            break

        cmd = obd.commands.ENGINE_LOAD  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_LOAD = response.value.magnitude
        else:
            GET_LOAD = 0.0

        if not STOP_GET:
            break

        cmd = obd.commands.COOLANT_TEMP  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_TEMP = response.value.magnitude

        if not STOP_GET:
            break

        cmd = obd.commands.FUEL_STATUS  # select an OBD command (sensor)
        response = connection.query(cmd)  # send the command, and parse the response
        if response.value is not None:
            GET_FUEL_STATUS = response.value[0]

        if not STOP_GET:
            break

        cmd = obd.commands.ELM_VOLTAGE
        response = connection.query(cmd)
        if response.value is not None:
            ELM_VOLTAGE = response.value.magnitude

        if not STOP_GET:
            break

        cmd = cvt_temp_command
        response = connection.query(cmd)
        if response.value is not None:
            CVT_TEMP = response
            # print(response)


def play_loop(playlist_normal, playlist_random, pygame):
    global song_title, song_number, song_total, playlist_shuffle
    # debug_on = True
    # playlist_shuffle = True
    # debug_on = True
    # playlist_shuffle = False
    # playlist_file = '/home/pi/obd2_trip_computer/playlist.txt'
    # playlist_file_shuffled = '/home/pi/obd2_trip_computer/playlist_shuffled.txt'
    # play_info_file = '/home/pi/obd2_trip_computer/play_info.txt'
    # music_folder = "/home/pi/Music"
    # music_folder_win = 'C:/Users/motoy/Music'
    """
    main loop function.
    playlist_normal, playlist_random - list
    usage each of them depends of playlist_shuffle bool
    :return: None
    """

    if playlist_shuffle:
        playlist = playlist_random
    else:
        playlist = playlist_normal
    song_total = len(playlist)
    if debug_on: print("total files in playlist: " + str(len(playlist)))
    if debug_on: print("Random is on: " + str(playlist_shuffle))
    file_to_start_index = play_info_read(play_info_file)
    # check if data correct in play_info_file, if not - start from first file
    if (file_to_start_index < 0) or (file_to_start_index > len(playlist) - 1):
        file_to_start_index = 0
    try:
        while STOP_PLAYER:
            for index, f in enumerate(playlist):
                if index >= file_to_start_index:
                    while pygame.mixer.music.get_busy() == 1:
                        # print("-----STOP_PLAYER!: " + str(STOP_PLAYER))
                        if STOP_PLAYER == 0:
                            print("-----EXIT from Play loop 4")
                            pygame.mixer.music.fadeout(1000)
                            break
                    try:
                        if STOP_PLAYER == 0:
                            print("-----EXIT from Play loop 3")
                            pygame.mixer.music.fadeout(1000)
                            break
                        if debug_on: print("file number is: " + str(index + 1))
                        play_info_write(play_info_file, index)
                        song_number = index + 1
                        temp_song_title = f
                        # prepare song title. symbols /\ are different in win and linux
                        if platform.system().startswith("Windows"):
                            temp_song_title = temp_song_title.rsplit("\\")[-1]
                            song_title = temp_song_title[:temp_song_title.rfind(".")]  # TBU . it is possible case if filename "file.....mp3"
                        else:
                            temp_song_title = temp_song_title.rsplit("/")[-1]
                            song_title = temp_song_title[:temp_song_title.rfind(".")]

                        if debug_on: print("file name: " + f)
                        pygame.mixer.music.load(f)
                        pygame.mixer.music.set_volume(1.0)
                        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=2000)
                    except Exception as a:
                        if debug_on: print(a)
                        print("-----EXIT from Play loop 5")
                        pygame.mixer.music.fadeout(1000)
                        continue


                else:
                    if STOP_PLAYER == 0:
                        print("-----EXIT from Play loop 2")
                        pygame.mixer.music.fadeout(1000)
                        break
                    continue
            # If shuffled playlist fully played, re-shuffle it, save new shuffled playlist to file
            if STOP_PLAYER == 0:
                print("-----EXIT from Play loop 1")
                pygame.mixer.music.fadeout(1000)
                break
            play_info_write(play_info_file, 0)
            file_to_start_index = 0
            if playlist_shuffle:
                random.shuffle(playlist_shuffled)
                playlist_write(playlist_file_shuffled, playlist_shuffled)

    finally:
        pygame.mixer.music.fadeout(1000)
        print("------EXIT from Play loop 0")


def print_fuel_status_string():
    if GET_FUEL_STATUS is not None:
        print_text_topleft(0, 500, GET_FUEL_STATUS, 30, fill=(255, 255, 55))


# function in develop. isn't finished yet
def print_line(name, value, line, position, font_size):
    # set the y position of text according to the line number
    line_to_y = {0: 0, 1: 30, 2: 75, 3: 115, 4: 155, 5: 195}
    y = line_to_y[line]

    if position is "left":
        print_text_topright(140, 75, "{:.1f}".format(average_speed_trip), font_size_values, fill=default_text_color)
        print_text_topleft(150, 75, "km/h av", font_size_values, fill=default_text_color)


def print_screen(screen_number):
    if screen_number is 0:
        # ############################### SCREEN 0 #########################################################
        # Print screen title
        print_text_midtop(150, 0, "trip odometer", 30, fill=title_text_color)
        print_text_midtop(500, 0, "odometer", 30, fill=title_text_color)

        # Print L/h or instant L/100km in motion
        if GET_SPEED > 0:
            print_text_topright(140, 30, "{:.1f}".format(LP100_inst), font_size_values, fill=default_text_color)
            print_text_topleft(150, 30, "L/100", font_size_values, fill=default_text_color)
        elif GET_RPM > engine_on_rpm:
            print_text_topright(140, 30, "{:.1f}".format(LPH), font_size_values, fill=default_text_color)
            print_text_topleft(150, 30, "L/h", font_size_values, fill=default_text_color)
        else:
            # do we need it or it setting to zero in calculating in main loop ???
            print_text_topright(140, 30, "0.0", font_size_values, fill=default_text_color)
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
        print_text_topright(140, 195, "{:.1f}".format(fuel_used_trip), font_size_values, fill=default_text_color)
        print_text_topleft(150, 195, "l", font_size_values, fill=default_text_color)

        # right side first row

        # print speed
        print_text_topleft(500, 30, "km/h", font_size_values, fill=default_text_color)
        print_text_topright(490, 30, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)

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
        print_text_topleft(500, 195, "l", font_size_values, fill=default_text_color)
        print_text_topright(490, 195, "{:.1f}".format(fuel_used_full), font_size_values, fill=default_text_color)

        # #######sensors data - second row

        # Print screen title
        print_text_midtop(105, 270, "sensors", 30, fill=title_text_color)

        # print volts
        if ELM_VOLTAGE < volts_alert:
            print_text_topright(140, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=alert_text_color)
            print_text_topleft(150, 305, "V", font_size_values, fill=alert_text_color)
        else:
            print_text_topright(140, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=default_text_color)
            print_text_topleft(150, 305, "V", font_size_values, fill=default_text_color)

        # print coolant temp
        degree_sign = u"\N{DEGREE SIGN}"
        if GET_TEMP >= temp_alert_high:
            print_text_topright(140, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=alert_text_color)
            print_text_topleft(150, 345, degree_sign + "C", font_size_values, fill=alert_text_color)
        else:
            if GET_TEMP < temp_alert_low:
                print_text_topright(140, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=cold_text_color)
                print_text_topleft(150, 345, '\u00b0' + "C Engine", font_size_values, fill=cold_text_color)
            else:
                print_text_topright(140, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=default_text_color)
                print_text_topleft(150, 345, '\u00b0' + "C Engine", font_size_values, fill=default_text_color)

        print_text_topright(140, 385, "{:.0f}".format(write_flash_counter), font_size_values, fill=default_text_color)
        print_text_topleft(150, 385, "Write", font_size_values, fill=default_text_color)

        #### CVT TEMP #########
        if CVT_TEMP >= temp_alert_high:
            print_text_topright(140, 425, "{:.0f}".format(CVT_TEMP), font_size_values, fill=alert_text_color)
            print_text_topleft(150, 425, degree_sign + "C CVT ", font_size_values, fill=alert_text_color)
        else:
            if CVT_TEMP < temp_alert_low:
                print_text_topright(140, 425, "{:.0f}".format(CVT_TEMP), font_size_values, fill=cold_text_color)
                print_text_topleft(150, 425, '\u00b0' + "C CVT", font_size_values, fill=cold_text_color)
            else:
                print_text_topright(140, 425, "{:.0f}".format(CVT_TEMP), font_size_values, fill=default_text_color)
                print_text_topleft(150, 425, '\u00b0' + "C CVT", font_size_values, fill=default_text_color)

    # ############################### SCREEN 1 #########################################################
    if screen_number is 1:
        screen.blit(background_image, (0, 0))  # ?
        # Print screen title
        print_text_midtop(250, 0, "Sensors", 30, fill=title_text_color)
        """
        # Print long term fuel trim
        print_text_topright(140, 265, "{:+.1f}".format(GET_LONG_L), font_size_values, fill=default_text_color)
        print_text_topleft(150, 265, "% LTFT", font_size_values, fill=default_text_color)

        # Print MAF
        print_text_topright(140, 305, "{:.1f}".format(GET_MAF), font_size_values, fill=default_text_color)
        print_text_topleft(150, 305, "g/cm^3 MAF", font_size_values, fill=default_text_color)

        # Print get load
        print_text_topright(140, 345, "{:.1f}".format(GET_LOAD), font_size_values, fill=default_text_color)
        print_text_topleft(150, 345, "% ENG LOAD", font_size_values, fill=default_text_color)

        # Print speed
        print_text_topright(140, 385, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)
        print_text_topleft(150, 385, "km/h", font_size_values, fill=default_text_color)

        # right side second row
        """
        # print motor time   
        print_text_topright(140, 385, "{:.0f}:{:.0f}".format(time_full // 3600.0, (time_full % 3600) / 60),
                            font_size_values, fill=default_text_color)
        # time_full in seconds. First print hours , then print minutes
        print_text_topleft(150, 385, "motor hours", font_size_values, fill=default_text_color)

        # Print long term fuel trim
        print_text_topright(140, 30, "{:+.1f}".format(GET_LONG_L), font_size_values, fill=default_text_color)
        print_text_topleft(150, 30, "% LTFT", font_size_values, fill=default_text_color)

        # print STFT
        print_text_topright(140, 70, "{:+.1f}".format(GET_SHORT_L), font_size_values, fill=default_text_color)
        print_text_topleft(150, 70, "% STFT", font_size_values, fill=default_text_color)

        # Print MAF
        print_text_topright(140, 115, "{:.1f}".format(GET_MAF), font_size_values, fill=default_text_color)
        print_text_topleft(150, 115, "g/cm^3 MAF", font_size_values, fill=default_text_color)

        # Print speed
        print_text_topright(140, 155, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)
        print_text_topleft(150, 155, "km/h", font_size_values, fill=default_text_color)

        # print RPM
        print_text_topleft(500, 30, "rpm", font_size_values, fill=default_text_color)
        print_text_topright(490, 30, "{:.0f}".format(GET_RPM), font_size_values, fill=default_text_color)



        # print volts
        if ELM_VOLTAGE < volts_alert:
            print_text_topleft(500, 305, "V", font_size_values, fill=alert_text_color)
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=alert_text_color)
        else:
            print_text_topleft(500, 305, "V", font_size_values, fill=default_text_color)
            print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=default_text_color)

        # print coolant temp
        degree_sign = u"\N{DEGREE SIGN}"
        if GET_TEMP > temp_alert_high:
            print_text_topleft(500, 345, degree_sign + "C engine", font_size_values, fill=alert_text_color)
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=alert_text_color)
        else:
            print_text_topleft(500, 345, '\u00b0' + "C engine", font_size_values, fill=default_text_color)
            print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=default_text_color)

        print_text_topleft(500, 385, "wr_count", font_size_values, fill=default_text_color)
        print_text_topright(490, 385, "{:.0f}".format(write_flash_counter), font_size_values, fill=default_text_color)

    # ############################### SCREEN 2 #########################################################
    if screen_number is 2:  # Music player
        screen.blit(background_image_music_player, (0, 0))

        #print_text_midtop(343, 50, "Music Player", 40, fill=alert_text_color)
        if playlist_shuffle:
            print_text_topright(349, 50, "Shuffle is ON:", font_size_values, fill=(20, 20, 200))
        else:
            print_text_topright(349, 50, "Shuffle is OFF:", font_size_values, fill=(20, 20, 200))

        print_text_topright(639, 50, str(song_number), font_size_values, fill=(20, 20, 200))
        print_text_topleft(643, 50, "/" + str(song_total), font_size_values, fill=(20, 20, 200))

        max_characters_displayed_per_line = 40
        if len(song_title) > max_characters_displayed_per_line:
            # try to split song title to two lines
            try:

                tmp_str_list = song_title.split()  # split on  strings

                # print first half of items in list on first line
                first_line = "".join(str(i) + " " for i in tmp_str_list[: len(tmp_str_list) // 2])
                if len(first_line) > max_characters_displayed_per_line:
                    raise Exception(
                        "first half of song title is too long. print first max_characters_displayed_per_line")

                print_text_midtop(443, 100, first_line, 50, fill=alert_text_color)

                # print second half of items in list on second line
                second_line = "".join(str(i) + " " for i in tmp_str_list[len(tmp_str_list) // 2:])
                if len(second_line) > max_characters_displayed_per_line:
                    second_line = second_line[:max_characters_displayed_per_line]
                print_text_midtop(443, 140, second_line, 50, fill=alert_text_color)

            except Exception as e:
                # print(e)

                print_text_midtop(443, 140, song_title[:max_characters_displayed_per_line - 1])
        else:
            print_text_midtop(443, 100, song_title, 50, fill=alert_text_color)


    # ############################### SCREEN 10 #########################################################
    if screen_number is 10:
        print_text_midtop(343, 100, "OBDII adapter disconnected", 40, fill=alert_text_color)
    # ############################### SCREEN 11 #########################################################
    if screen_number is 11:
        print_text_midtop(343, 100, "  CONNECTING...", 50, fill=default_text_color)
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
    global STOP_GET, STOP_PRINT, STOP_ACCELERATION, STOP_PLAYER
    c.acquire()
    STOP_GET = 0
    STOP_PRINT = 0
    STOP_ACCELERATION = 0
    STOP_PLAYER = 0
    c.notifyAll()
    c.release()


def connect():
    if platform.system().startswith("Windows"):
        connection_obj = obd.OBD(com_port)  # config for Windows OS
        return connection_obj
    else:
        # connection_obj = obd.OBD("/dev/ttyUSB0")  # connect to specific port in linux
        connection_obj = obd.OBD()
        return connection_obj  # return connection object in main loop


pygame.quit()  # it is needed for prevent visual issues. TBC
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((940, 624))  # set the resolution of app window or full screen mode
# pygame.display.toggle_fullscreen()  # Uncomment for fullscreen mode

done = False  # set the while exit-value for main loop
# pygame.mouse.set_visible(False)  # do not display mouse cursor
screen.blit(background_image, (0, 0))
print_screen(11)  # display the connection message
connection = connect()  # initialize obd connection

"""
Adding custom querry for OBD (CVT_TEMP)
"""

# initialize thread for reading data from ECU
Thread_getValues = threading.Thread(target=get_values)
Thread_getValues.daemon = False
Thread_getValues.start()
# Thread_getValues.join()

music_player_thread = threading.Thread(target=play_loop, args=(playlist_normal, playlist_shuffled, pygame))
music_player_thread.daemon = False
music_player_thread.start()
# music_player_thread.join()

if not platform.system().startswith("Windows"):
    button1 = Button(pin=2, pull_up=True, bounce_time=0.05, hold_time=2, hold_repeat=False)
    button2 = Button(pin=3, pull_up=True, bounce_time=0.05, hold_time=2, hold_repeat=False)
    button1.when_released = stop_play
    print("Screen counter: " + str(screen_counter))
    button2.when_released = button_process

# checking is log file available or not. creating new one if not
if not os.path.isfile(log_file):
    create_log_file()

# do once to display average speed, fuel consumption before the ignition is on
# start
log_data = csv_read()
odometer_full = float(log_data[0])
fuel_used_full = float(log_data[1])
time_full = float(log_data[2])

if odometer_full > 0.1:  # 0.1 because too high values are displayed after reset log file
    LP100_full = (fuel_used_full / odometer_full) * 100.0
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
        print_screen(10)  # display values on screen 0
        connection = connect()  # try to reconnect
    else:
        # if connection with elm327 adapter is available
        # main loop
        if GET_RPM > engine_on_rpm:
            FuelFlowLitersPerSecond = 0.0
            odometer_add_loop = 0.0

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
            time_loop = time_new - time_old  # * tcorrect  # time after the last speed calculating

            # if time1 > 10:
            #    time1 = 0

            time_old = time_new  # write new time for comparing in new cycle

            fuel_add_loop = FuelFlowLitersPerSecond * time_loop
            fuel_used_trip = fuel_used_trip + fuel_add_loop  # fuel consumption for trip

            if GET_SPEED > 0:
                odometer_add_loop = (((
                                                  GET_SPEED * 1000.0) / 3600.0) * time_loop) / 1000.0  # calculate distance per time_loop
                odometer_trip = odometer_trip + odometer_add_loop  # odometer value per trip
                if odometer_add_loop > 0:
                    LP100_inst = (fuel_add_loop / odometer_add_loop) * 100.0  # instant fuel consumption

            if odometer_trip > 0 and time_trip > 0:
                average_speed_trip = odometer_trip / (time_trip / 3600.0)

            # Writing data to log file on drive
            # every 30 minutes on speeds > 10km/h
            # every 60 seconds on speeds 1...10km/h
            # every 30 seconds on speeds <= 1km/h
            if ((GET_SPEED > 1) and (GET_SPEED < 10) and ((time_new - time_old_journal) > 60)) or \
                    ((GET_SPEED <= 1) and ((time_new - time_old_journal) > 30)) or \
                    ((time_new - time_old_journal) > 1800):
                # read data from log file
                log_data = csv_read()
                # calculate new values of data in log file
                odometer_eeprom = float(log_data[0]) + odometer_add_journal + odometer_add_loop
                benz_eeprom = float(log_data[1]) + fuel_add_journal + fuel_add_loop
                time_eeprom = float(log_data[2]) + time_add_journal + time_loop
                # Write new data in log file
                csv_write(odometer_eeprom, benz_eeprom, time_eeprom)

                # debug code for investigate with count of writing operations
                write_flash_counter += 1

                # calculations for the average values
                odometer_full = odometer_eeprom
                fuel_used_full = benz_eeprom
                time_full = time_eeprom
                if odometer_full > 0:
                    LP100_full = (fuel_used_full / odometer_full) * 100.0
                if time_full > 0:
                    average_speed_full = odometer_full / (time_full / 3600.0)

                odometer_add_journal = 0
                fuel_add_journal = 0
                time_add_journal = 0
                time_old_journal = time_new

            else:
                odometer_add_journal = odometer_add_journal + odometer_add_loop
                fuel_add_journal = fuel_add_journal + fuel_add_loop
                time_add_journal += time_loop

                odometer_full = odometer_eeprom + odometer_add_journal
                fuel_used_full = benz_eeprom + fuel_add_journal
                time_full = time_eeprom + time_add_journal
                if odometer_full > 0:
                    LP100_full = (fuel_used_full / odometer_full) * 100.0
                if time_full > 0:
                    average_speed_full = odometer_full / (time_full / 3600.0)

        else:
            if GET_SPEED == 0:
                time_start = 0
                time_trip = 0
                odometer_trip = 0
                fuel_used_trip = 0
                average_speed_trip = 0  # for displaying 0 if engine off
                LPH = 0.0

        if odometer_trip > 0:
            LP100_trip = (fuel_used_trip / odometer_trip) * 100.0  # Fuel consumption L/100km

        # screen.fill(background_color)
        # uncomment for using background image
        screen.blit(background_image, (0, 0))
        print_screen(screen_counter)  # display values on screen 0

    # manage events to quit the application. works only with keyboard and mouse
    # print("MAIN-STOP_PLAYER!: " + str(STOP_PLAYER))
    # left arrow - next screen
    # right arrow - next song
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            done = True
            quit_app()

        if event.type == pygame.QUIT:
            done = True
            quit_app()

        if event.type == pygame.KEYDOWN:  # changing screen
            if event.key == pygame.K_LEFT:
                if screen_counter < screen_last:
                    screen_counter += 1
                else:
                    screen_counter = 0

            if event.key == pygame.K_RIGHT:
                stop_play()

    pygame.display.flip()  # Update the full display Surface to the screen
    clock.tick(25)  # set fps for the app

pygame.display.quit()
# music_player_thread.stop()
print("EEEEEEEEEND")

sys.exit(0)
