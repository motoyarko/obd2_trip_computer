import random
import os
from gpiozero import Button
import platform
"""
main features:
* two playlists are generated. shuffled and normally ordered
* you can choose which to use by playlist_shuffle = True/False
* playlist_shuffle = False : after all files are played, continue from first item
* playlist_shuffle = True : after all files are played, shuffled playlist is re-generated and continue from first item
* system checks is there new/deleted files in music directory during start. if yes - all playlists are regenerated
* Continue playing from the last played song
* next track by press the button on raspberry 
"""

"""
TODO:
normilize variables names
move constants from functions to top of module
move buttons logic to separate module for using it by obd and player modules 
"""
debug_on = False
playlist_shuffle = True
playlist_file = 'playlist.txt'
playlist_file_shuffled = 'playlist_shuffled.txt'
play_info_file = 'play_info.txt'
music_folder = "/home/pi/Music"
music_folder_win = 'C:/Users/motoy/Music'


def kill_omxplayer1():
    """
    it kills omxplayer process
    After killing it, the next song from playlist starts playing in the play_loop()
    :return:
    """
    os.system('killall omxplayer.bin')
    if debug_on: print("next song")


if not platform.system().startswith("Windows"):
    button1 = Button(pin=2, pull_up=True, bounce_time=0.05, hold_time=2, hold_repeat=False)
    button2 = Button(pin=3, pull_up=True, bounce_time=0.05, hold_time=2, hold_repeat=False)
    button1.when_released = kill_omxplayer1


def get_audio_files_list(directory):
    """
    it scans home Music directory for *.mp3 *.flac files
    :return:
    list of music files with full path
    """
    files_list = []
    #directory = "/home/pi/Music"
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3") or file.endswith(".flac"):
                files_list.append(os.path.join(root, file))
    return files_list


def play_loop(playlist_normal, playlist_random):
    """
    main loop function.
    playlist_normal, playlist_random - list
    usage each of them depends of playlist_shuffle bool
    :return: Nne
    """
    os.system('killall omxplayer.bin')
    # files_counter = 0
    # print("total files in file system: " + str(len(playlist_normal)))
    if playlist_shuffle:
        playlist = playlist_random
    else:
        playlist = playlist_normal
    if debug_on: print("total files in playlist: " + str(len(playlist)))
    if debug_on: print("Random is on: " + str(playlist_shuffle))
    file_to_start_index = play_info_read(play_info_file)
    # check if data correct in play_info_file, if not - start from first file
    if (file_to_start_index < 0) or (file_to_start_index > len(playlist) - 1):
        file_to_start_index = 0

    while True:
        for index, f in enumerate(playlist):
            if index >= file_to_start_index:
                try:
                    if debug_on: print("file number is: " + str(index + 1))
                    play_info_write(play_info_file, index)
                    if debug_on: print("file name: " + f)
                    os.system('omxplayer -o local "%s"' % f)
                except a:
                    if debug_on: print(a)
            else:
                continue
        # If shuffled playlist fully played, re-shuffle it, save new shuffled playlist to file
        play_info_write(play_info_file, 0)
        file_to_start_index = 0
        if playlist_shuffle:
            random.shuffle(playlist_shuffled)
            playlist_write(playlist_file_shuffled, playlist_shuffled)


# Start file functions
def playlist_read(file):
    try:
        with open(file, 'r') as f:
            list = f.readlines()
            return [a[:-1] for a in list]  # return new list without '\n' at the end of each link
    except Exception as e:
        # if file doesn't exist - display message and create file
        # return []
        playlist_write(file, [])
        if debug_on: print("CAN'T READ PLAYLIST FILE")
        if debug_on: print(e)
        return []


def playlist_write(file, track_list):
    try:
        with open(file, 'w') as f:
            for item in track_list:
                f.writelines(item + '\n')
            if debug_on: print("new playlist is writen")
    except Exception as e:
        # If can't write in log file - display message, and print it in terminal
        if debug_on: print("ERRROR WRITING IN PLAYLIST FILE")
        if debug_on: print(e)


def compare_lists(list1, list2):
    """
    Returns True if equal
    """
    set1 = set(list1)
    set2 = set(list2)
    result = set1.difference(set2)
    if not result:
        return True
    else:
        if debug_on: print(str(len(result)) + " added/deleted files in the Music directory")
        return False


def play_info_write(file, play_info):
    try:
        with open(file, 'w') as f:
            f.write(str(play_info))
            if debug_on: print("new play info is writen")
    except Exception as e:
        # If can't write in log file - display message, and print it in terminal
        if debug_on: print("ERRROR WRITING IN PLAY INFO FILE")
        if debug_on: print(e)


def play_info_read(file):
    """
    read last played track iter from file
    :param file:
    :return: int
    """
    try:
        with open(file, 'r') as f:
            play_info = f.read()
            return int(play_info)  # return last track number
    except Exception as e:
        # if file doesn't exist - display message and create file
        # return []
        play_info_write(file, 0)
        if debug_on: print("CAN'T READ PLAY INFO FILE")
        if debug_on: print(e)
        return 0


# read Music folder for audio files
if not platform.system().startswith("Windows"):
    files_result = get_audio_files_list(music_folder)
else:
    files_result = get_audio_files_list(music_folder_win)

# Create playlist file if it doesn't exist
if not os.path.isfile(playlist_file):
    playlist_write(playlist_file, files_result)
if not os.path.isfile(playlist_file_shuffled):
    playlist_shuffled = files_result.copy()
    random.shuffle(playlist_shuffled)
    playlist_write(playlist_file_shuffled, playlist_shuffled)

# compare playlist file and newelly readed files list from the Music folder
# and rewrite playlist file with actual data if needed
old_playlist = playlist_read(playlist_file)
if not compare_lists(files_result, old_playlist):
    playlist_write(playlist_file, files_result)
    playlist_shuffled = files_result.copy()
    random.shuffle(playlist_shuffled)
    playlist_write(playlist_file_shuffled, playlist_shuffled)
    play_info_write(play_info_file, 0)
else:
    playlist_shuffled = playlist_read(playlist_file_shuffled)


# Maybe it is not needed
if len(playlist_shuffled) == 0:  # for case if shuffled playlist is blank
    playlist_shuffled = files_result.copy()
    random.shuffle(playlist_shuffled)
    playlist_write(playlist_file_shuffled, playlist_shuffled)

play_loop(playlist_normal=files_result, playlist_random=playlist_shuffled)
