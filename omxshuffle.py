import random
import os
from gpiozero import Button
import platform
#from buttons import buton_process
#from main import STOP_PLAYER

#STOP_PLAYER = 1

"""
TODO:
normilize variables names
move constants from functions to top of module
move buttons logic to separate module for using it by obd and player modules 
"""
screen_last = 1

debug_on = True
playlist_shuffle = False
music_folder = os.path.expanduser('~/Music')

if platform.system().startswith("Windows"):
    playlist_file = 'playlist.pls'
    playlist_file_shuffled = 'playlist_shuffled.pls'
    play_info_file = 'play_info.pls'
    #music_folder = "C:/Users/motoy/Music"
else:
    playlist_file = '/home/pi/obd2_trip_computer/playlist.txt'
    playlist_file_shuffled = '/home/pi/obd2_trip_computer/playlist_shuffled.txt'
    play_info_file = '/home/pi/obd2_trip_computer/play_info.txt'
    #music_folder = "/home/pi/Music"

#music_folder_win = 'C:/Users/motoy/Music'

files_result =[]
playlist_shuffled = []

def get_audio_files_list(directory):
    """
    it scans home Music directory for *.mp3 *.flac files
    :return:
    list of music files with full path
    """
    files_list = []
    for root, subdirectories, files in os.walk(directory):
        for file in files:
            if file.endswith(".mp3") or file.endswith(".wav"):
            #if file.endswith(".mp3"):
                files_list.append(os.path.join(root, file))
    return files_list

def play_loop(playlist_normal, playlist_random, pygame, STOP_PLAYER):
    #global STOP_PLAYER
    """
    main loop function.
    playlist_normal, playlist_random - list
    usage each of them depends of playlist_shuffle bool
    :return: None
    """
    #os.system('killall omxplayer.bin')
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
    try:
        while STOP_PLAYER:
            for index, f in enumerate(playlist):
                if index >= file_to_start_index:
                    while pygame.mixer.music.get_busy() == 1:
                        print("-----STOP_PLAYER!: " + str(STOP_PLAYER))
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
                        if debug_on: print("file name: " + f)
                        pygame.mixer.music.load(f)
                        pygame.mixer.music.play(loops=0, start=0.0, fade_ms=2000)
                    except a:
                        if debug_on: print(a)
                        print("-----EXIT from Play loop 5")
                        pygame.mixer.music.fadeout(1000)
                        
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
    import sys
    try:
        with open(file, 'w') as f:
            for item in track_list:
                try:
                    f.writelines(item + '\n')
                    #print(sys.getfilesystemencoding())
                    #item_utf8 = item.encode('utf8', 'surrogateescape').decode('utf8')
                    #print("item_utf_8")
                    #f.writelines(u'\n')
                    #print("writelines")
                except Exception as e:
                    if debug_on: print("try in file write")
                    if debug_on: print("ERRROR WRITING IN PLAYLIST FILE")
                    if debug_on: print(e)
                    #if debug_on: print(item)
            if debug_on: print("new playlist is writen")
    except Exception as e:
        # If can't write in log file - display message, and print it in terminal
        if debug_on: print("first try")
        if debug_on: print("ERRROR WRITING IN PLAYLIST FILE")
        if debug_on: print(e)
        if debug_on: print(item)


def compare_lists(list1, list2):
    """
    Returns True if equal
    """
    set1 = set(list1)
    set2 = set(list2)
    result1 = set1.difference(set2)
    result2 = set2.difference(set1)
    #The difference method returns a new set having all the elements of set1 which is not present in set2
    #If we deleting files, it can be case when difference is {}
    if not result1 and not result2:
        return True
    else:
        if debug_on: print(str(len(result1)+len(result2)) + " added/deleted files in the Music directory")
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


def get_playlist():
    #get_audio_files_list(music_folder)
    
    # read Music folder for audio files
    files_result = get_audio_files_list(music_folder)
    #print(files_result)
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
        print("test string!!!")
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
    return [files_result, playlist_shuffled]
