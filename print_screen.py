import platform

if platform.system().startswith("Windows"):
    background_image_file = "background_image.bmp"
    background_image_music_player_file = "background_image_music_player.bmp"
    font_file = "Audiowide-Regular.ttf"
else:
    background_image_file = "/home/pi/obd2_trip_computer/background_image.bmp"
    background_image_music_player_file = "/home/pi/obd2_trip_computer/background_image_music_player.bmp"
    font_file = "/home/pi/obd2_trip_computer/Audiowide-Regular.ttf"


##### Resolve variables errors #########

class PrintScreen:
    def __init__(self, variables, font_file, pygame):
        self.font_file = font_file
        self.pygame = pygame
        self.background_image = pygame.image.load(background_image_file)
        self.background_image_music_player = pygame.image.load(background_image_music_player_file)
        self.font_file = font_file

    def print_text_topleft(self, x, y, text, size, fill):
        font = self.pygame.font.Font(self.font_file, size)
        puttext = font.render(text, True, fill)
        text_rect = puttext.get_rect()
        text_rect.topleft = (x, y)
        screen.blit(puttext, text_rect)

    def print_text_topright(self, x, y, text, size, fill):
        font = self.pygame.font.Font(self.font_file, size)
        puttext = font.render(text, True, fill)
        text_rect = puttext.get_rect()
        text_rect.topright = (x, y)
        screen.blit(puttext, text_rect)

    def print_text_midtop(self, x, y, text, size, fill):
        # font = pygame.font.Font(font_file, size)
        font = self.pygame.font.Font(None, size)
        puttext = font.render(text, True, fill)
        text_rect = puttext.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(puttext, text_rect)

    def print_fuel_status_string(self):
        if GET_FUEL_STATUS is not None:
            print_text_topleft(0, 500, GET_FUEL_STATUS, 30, fill=(255, 255, 55))

    # function in develop. isn't finished yet
    def print_line(self, name, value, line, position, font_size):
        # set the y position of text according to the line number
        line_to_y = {0: 0, 1: 30, 2: 75, 3: 115, 4: 155, 5: 195}
        y = line_to_y[line]

        if position is "left":
            print_text_topright(140, 75, "{:.1f}".format(average_speed_trip), font_size_values, fill=default_text_color)
            print_text_topleft(150, 75, "km/h av", font_size_values, fill=default_text_color)

    def print_screen(self, screen_number):
        if screen_number is 0:
            # ############################### SCREEN 0 #########################################################
            # Print screen title
            self.print_text_midtop(150, 0, "trip odometer", 30, fill=title_text_color)
            self.print_text_midtop(500, 0, "odometer", 30, fill=title_text_color)

            # Print L/h or instant L/100km in motion
            if GET_SPEED > 0:
                self.print_text_topright(140, 30, "{:.1f}".format(LP100_inst), font_size_values, fill=default_text_color)
                self.print_text_topleft(150, 30, "L/100", font_size_values, fill=default_text_color)
            elif GET_RPM > engine_on_rpm:
                self.print_text_topright(140, 30, "{:.1f}".format(LPH), font_size_values, fill=default_text_color)
                self.print_text_topleft(150, 30, "L/h", font_size_values, fill=default_text_color)
            else:
                # do we need it or it setting to zero in calculating in main loop ???
                self.print_text_topright(140, 30, "0.0", font_size_values, fill=default_text_color)
                self.print_text_topleft(150, 30, "L/h", font_size_values, fill=default_text_color)

            # Print av speed trip
            self.print_text_topright(140, 75, "{:.1f}".format(average_speed_trip), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 75, "km/h av", font_size_values, fill=default_text_color)

            # Print trip L/100
            if odometer_trip > 0.1:
                lp100_to_print = "{:.1f}".format(LP100_trip)  # display Lp100km value after 0.1 km trip
            else:
                lp100_to_print = "-.-"
            self.print_text_topright(140, 115, lp100_to_print, font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 115, "l/100", font_size_values, fill=default_text_color)

            # Print trip km
            self.print_text_topright(140, 155, "{:.1f}".format(odometer_trip), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 155, "km", font_size_values, fill=default_text_color)

            # Print trip L
            self.print_text_topright(140, 195, "{:.1f}".format(fuel_used_trip), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 195, "l", font_size_values, fill=default_text_color)

            # right side first row

            # print speed
            self.print_text_topleft(500, 30, "km/h", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 30, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)

            # print av speed full
            self.print_text_topleft(500, 75, "km/h av", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 75, "{:.1f}".format(average_speed_full), font_size_values, fill=default_text_color)

            # print av L/100 full
            self.print_text_topleft(500, 115, "l/100 av", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 115, "{:.1f}".format(LP100_full), font_size_values, fill=default_text_color)

            # print odometer full
            self.print_text_topleft(500, 155, "km", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 155, "{:.1f}".format(odometer_full), font_size_values, fill=default_text_color)

            # print fuel litters full
            self.print_text_topleft(500, 195, "l", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 195, "{:.1f}".format(fuel_used_full), font_size_values, fill=default_text_color)

            # #######sensors data - second row

            # Print screen title
            self.print_text_midtop(105, 270, "sensors", 30, fill=title_text_color)

            # print volts
            if ELM_VOLTAGE < volts_alert:
                self.print_text_topright(140, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=alert_text_color)
                self.print_text_topleft(150, 305, "V", font_size_values, fill=alert_text_color)
            else:
                self.print_text_topright(140, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=default_text_color)
                self.print_text_topleft(150, 305, "V", font_size_values, fill=default_text_color)

            # print coolant temp
            degree_sign = u"\N{DEGREE SIGN}"
            if GET_TEMP >= temp_alert_high:
                self.print_text_topright(140, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=alert_text_color)
                self.print_text_topleft(150, 345, degree_sign + "C", font_size_values, fill=alert_text_color)
            else:
                if GET_TEMP < temp_alert_low:
                    self.print_text_topright(140, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=cold_text_color)
                    self.print_text_topleft(150, 345, '\u00b0' + "C Engine", font_size_values, fill=cold_text_color)
                else:
                    self.print_text_topright(140, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=default_text_color)
                    self.print_text_topleft(150, 345, '\u00b0' + "C Engine", font_size_values, fill=default_text_color)

            self.print_text_topright(140, 385, "{:.0f}".format(write_flash_counter), font_size_values,
                                fill=default_text_color)
            self.print_text_topleft(150, 385, "Write", font_size_values, fill=default_text_color)

            #### CVT TEMP #########
            if CVT_TEMP >= temp_alert_high:
                self.print_text_topright(140, 425, "{:.0f}".format(CVT_TEMP), font_size_values, fill=alert_text_color)
                self.print_text_topleft(150, 425, degree_sign + "C CVT ", font_size_values, fill=alert_text_color)
            else:
                if CVT_TEMP < temp_alert_low:
                    self.print_text_topright(140, 425, "{:.0f}".format(CVT_TEMP), font_size_values, fill=cold_text_color)
                    self.print_text_topleft(150, 425, '\u00b0' + "C CVT", font_size_values, fill=cold_text_color)
                else:
                    self.print_text_topright(140, 425, "{:.0f}".format(CVT_TEMP), font_size_values, fill=default_text_color)
                    self.print_text_topleft(150, 425, '\u00b0' + "C CVT", font_size_values, fill=default_text_color)

        # ############################### SCREEN 1 #########################################################
        if screen_number is 1:
            screen.blit(background_image, (0, 0))  # ?
            # Print screen title
            self.print_text_midtop(250, 0, "Sensors", 30, fill=title_text_color)
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
            self.print_text_topright(140, 385, "{:.0f}:{:.0f}".format(time_full // 3600.0, (time_full % 3600) / 60),
                                font_size_values, fill=default_text_color)
            # time_full in seconds. First print hours , then print minutes
            self.print_text_topleft(150, 385, "motor hours", font_size_values, fill=default_text_color)

            # Print long term fuel trim
            self.print_text_topright(140, 30, "{:+.1f}".format(GET_LONG_L), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 30, "% LTFT", font_size_values, fill=default_text_color)

            # print STFT
            self.print_text_topright(140, 70, "{:+.1f}".format(GET_SHORT_L), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 70, "% STFT", font_size_values, fill=default_text_color)

            # Print MAF
            self.print_text_topright(140, 115, "{:.1f}".format(GET_MAF), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 115, "g/cm^3 MAF", font_size_values, fill=default_text_color)

            # Print speed
            self.print_text_topright(140, 155, "{:.0f}".format(GET_SPEED), font_size_values, fill=default_text_color)
            self.print_text_topleft(150, 155, "km/h", font_size_values, fill=default_text_color)

            # print RPM
            self.print_text_topleft(500, 30, "rpm", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 30, "{:.0f}".format(GET_RPM), font_size_values, fill=default_text_color)

            # print volts
            if ELM_VOLTAGE < volts_alert:
                self.print_text_topleft(500, 305, "V", font_size_values, fill=alert_text_color)
                self.print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=alert_text_color)
            else:
                self.print_text_topleft(500, 305, "V", font_size_values, fill=default_text_color)
                self.print_text_topright(490, 305, "{:.1f}".format(ELM_VOLTAGE), font_size_values, fill=default_text_color)

            # print coolant temp
            degree_sign = u"\N{DEGREE SIGN}"
            if GET_TEMP > temp_alert_high:
                self.print_text_topleft(500, 345, degree_sign + "C engine", font_size_values, fill=alert_text_color)
                self.print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=alert_text_color)
            else:
                self.print_text_topleft(500, 345, '\u00b0' + "C engine", font_size_values, fill=default_text_color)
                self.print_text_topright(490, 345, "{:.0f}".format(GET_TEMP), font_size_values, fill=default_text_color)

            self.print_text_topleft(500, 385, "wr_count", font_size_values, fill=default_text_color)
            self.print_text_topright(490, 385, "{:.0f}".format(write_flash_counter), font_size_values,
                                fill=default_text_color)

        # ############################### SCREEN 2 #########################################################
        if screen_number is 2:  # Music player
            screen.blit(background_image_music_player, (0, 0))

            # print_text_midtop(343, 50, "Music Player", 40, fill=alert_text_color)
            if playlist_shuffle:
                self.print_text_topright(349, 50, "Shuffle is ON:", font_size_values, fill=(20, 20, 200))
            else:
                self.print_text_topright(349, 50, "Shuffle is OFF:", font_size_values, fill=(20, 20, 200))

            self.print_text_topright(639, 50, str(song_number), font_size_values, fill=(20, 20, 200))
            self.print_text_topleft(643, 50, "/" + str(song_total), font_size_values, fill=(20, 20, 200))

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

                    self.print_text_midtop(443, 100, first_line, 50, fill=alert_text_color)

                    # print second half of items in list on second line
                    second_line = "".join(str(i) + " " for i in tmp_str_list[len(tmp_str_list) // 2:])
                    if len(second_line) > max_characters_displayed_per_line:
                        second_line = second_line[:max_characters_displayed_per_line]
                    self.print_text_midtop(443, 140, second_line, 50, fill=alert_text_color)

                except Exception as e:
                    # print(e)

                    self.print_text_midtop(443, 140, song_title[:max_characters_displayed_per_line - 1])
            else:
                self.print_text_midtop(443, 100, song_title, 50, fill=alert_text_color)

        # ############################### SCREEN 10 #########################################################
        if screen_number is 10:
            self.print_text_midtop(343, 100, "OBDII adapter disconnected", 40, fill=alert_text_color)
        # ############################### SCREEN 11 #########################################################
        if screen_number is 11:
            self.print_text_midtop(343, 100, "  CONNECTING...", 50, fill=default_text_color)
            self.pygame.display.flip()
