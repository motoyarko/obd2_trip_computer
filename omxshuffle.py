import random
import os
from gpiozero import Button

"""
TODO:
normilize variables names
move constants from functions to top of module
move buttons logic to separate module for using it by obd and player modules 
"""

playlist_shuffle = True
playlist_file = 'playlist.txt'
playlist_file_shuffled = 'playlist_shuffled.txt'
play_info_file = 'play_info.txt'

button1 = Button(pin=2, pull_up=True, bounce_time=0.05, hold_time=2, hold_repeat=False)
button2 = Button(pin=3, pull_up=True, bounce_time=0.05, hold_time=2, hold_repeat=False)


def kill_omxplayer1():
    os.system('killall omxplayer.bin')
    print("next song")


button1.when_released = kill_omxplayer1


def get_audio_files_list():
    files_result = []
    directory = "/home/pi/Music"
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3") or file.endswith(".flac"):
                files_result.append(os.path.join(root, file))
    return files_result


def play_loop():
    os.system('killall omxplayer.bin')
    # files_counter = 0
    print("total files in file system: " + str(len(files_result)))
    if playlist_shuffle:
        playlist = playlist_shuffled
    else:
        playlist = files_result
    print("total files in playlist: " + str(len(playlist)))
    print("Random is on: " + str(playlist_shuffle))
    file_to_start = play_info_read(play_info_file)
    # check if data correct in play_info_file, if not - start from first file
    if (file_to_start < 0) or (file_to_start > len(playlist) - 1):
        file_to_start = 0

    while True:
        for index, f in enumerate(playlist):
            if (index >= file_to_start):
                try:
                    print("file number is: " + str(index + 1))
                    play_info_write(play_info_file, index)
                    print("file name: " + f)
                    os.system('omxplayer -o local "%s"' % f)

                except a:
                    print(a)
            else:
                continue

        # If shuffled playlist fully played, reshufle it, save new shufled playlist to file
        play_info_write(play_info_file, 0)
        file_to_start = 0
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
        print("CAN'T READ PLAYLIST FILE")
        print(e)
        return []


def playlist_write(file, track_list):
    try:
        with open(file, 'w') as f:
            for item in track_list:
                f.writelines(item + '\n')
            print("new playlist is writen")
    except Exception as e:
        # If can't write in log file - display message, and print it in terminal
        print("ERRROR WRITING IN PLAYLIST FILE")
        print(e)


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
        print(str(len(result)) + " added/deleted files in the Music directory")
        return False


def play_info_write(file, play_info):
    try:
        with open(play_info_file, 'w') as f:
            f.write(str(play_info))
            print("new play info is writen")
    except Exception as e:
        # If can't write in log file - display message, and print it in terminal
        print("ERRROR WRITING IN PLAY INFO FILE")
        print(e)


def play_info_read(file):
    try:
        with open(file, 'r') as f:
            play_info = f.read()
            return int(play_info)  # return last track number
    except Exception as e:
        # if file doesn't exist - display message and create file
        # return []
        play_info_write(file, 0)
        print("CAN'T READ PLAY INFO FILE")
        print(e)
        return 0


# read Music folder for audio files
files_result = get_audio_files_list()

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

if len(playlist_shuffled) == 0:  # for case if shuffled playlist is blank
    playlist_shuffled = files_result.copy()
    random.shuffle(playlist_shuffled)
    playlist_write(playlist_file_shuffled, playlist_shuffled)

play_loop()
