import pygame, error, os
from mutagen.mp3 import MP3
from pydub import AudioSegment
from simpleaudio.shiny import play_buffer
from math import log10
from pydub.playback import play as play_sound
from threading import Thread
pygame.init()

pygame.mixer.init(buffer=16)


def set_effect_volume(volume):
    global effect_muted, effect_volume, sound_effect_list
    effect_volume = volume
    sound_effect_list.clear()
    if volume == 0:
        effect_muted = True
    else:
        effect_muted = False
    try:

        for effect in se_list:
            song = AudioSegment.from_wav(os.path.join("resources\\effects", effect))
            song += 20 * log10(volume/50 + 0.01) # volume/2-40  # 15 - 45 # (volume+45)*5/3
            sound_effect_list[effect[:effect.find(".")]] = song
    except FileNotFoundError:
        error.error(error.SoundError, 2)


def set_music_volume(volume):
    global music_volume
    music_volume = volume
    pygame.mixer.music.set_volume(volume / 100)


def play(file_name, resume=False, register=True, delay_ms=0, loops=-1):
    # resume - whether or not the song should be resumed from where last played
    # register - whether the position of played song should be registered
    global now_playing, last_playing, current_loop, last_resumed, last_register, max_loops

    if last_register:
        song_delay[now_playing] += get_pos()
    song_delay[now_playing] = (song_delay[now_playing] / 1000) % get_song_len(now_playing) * 1000

    last_resumed = bool(resume)
    last_register = bool(register)

    try:
        pygame.mixer.music.unload()
        if file_name in ("", "none"):
            pygame.mixer.music.stop()
            if register:
                last_playing = str(now_playing)
            return
        pygame.mixer.music.load("resources/music/" + file_name + ".mp3")
        pygame.mixer.music.play(loops=loops, start=(delay_ms / 1000 + set_song_delay[file_name] + (get_pos(file_name)/1000 if resume else 0)) % get_song_len(file_name))
        current_loop = 0
        max_loops = loops if loops != 0 else 1
        #  print(delay_ms / 1000 + set_song_delay[file_name] + (get_pos(file_name)/1000 if resume else 0))
    except pygame.error as e:
        print(f"error: {e}")
        error.error(error.SoundError, 1)

    if register:
        if resume:
            song_delay[file_name] += delay_ms
        else:
            song_delay[file_name] = delay_ms
        last_playing = str(now_playing)
    song_delay[file_name] = (song_delay[file_name] / 1000) % get_song_len(file_name) * 1000

    now_playing = str(file_name)


def play_effect(file_name):
    if file_name == "none":
        return
    if not effect_muted:
        try:
            thread = Thread(target=play_sound, args=[sound_effect_list[file_name]])
            thread.start()
        except FileNotFoundError:
            error.error(error.SoundError, 2)


def get_song_len(song_checked=None):
    if song_checked is None:
        song_checked = now_playing
    return MP3("resources/music/" + song_checked + ".mp3").info.length


def is_playing():
    return pygame.mixer.music.get_busy()


def get_pos(name=None):
    if now_playing == "":
        return 0
    if name is None:
        return pygame.mixer.music.get_pos() - 1000 * (song_length[now_playing] + set_song_delay[now_playing]) * current_loop
    return song_delay[name]


def handle():
    global now_playing, current_loop
    if not is_playing():
        now_playing = "none"
    if get_pos() >= song_length[now_playing] * 1000:
        current_loop += 1


def get_current_song():
    return now_playing


se_list = []
sound_effect_list = {}
for file in os.listdir("resources\\effects"):
    se_list.append(file)
se_list.sort()

set_song_delay = {"none": 0, "song1": 0.5, "song2": 1, "song3": 1, "death_song": 0.7, "winning_song": 0.6, "menu": 0.5,
                  "shop1": 0.3, "forest1": 1.1, "palace1": 1.1, "battle2": 0, "battle3": 0.2, "battle1": 0, "river1": 1.1,
                  "capital1": 1.1, "battle4": 0.4, "spludit1": 0.55, "spludit2": 1.1, "ocean": 1.1, "spongebob": 0.35,
                  "apple": 0, "battle5": 0.4}
song_delay = {i: 0 for i in set_song_delay}
song_length = {i: get_song_len(i) - set_song_delay[i] for i in set_song_delay}

now_playing = "none"
current_loop = 0
max_loops = 0

last_playing = "none"
last_resumed = False
last_register = False

effect_muted = False

effect_volume = 0.4
music_volume = 0.4
set_effect_volume(40)  # 0.8
set_music_volume(40)  # 0.5

if __name__ == "__main__":
    win = pygame.display.set_mode((256, 64))
    clock = pygame.time.Clock()
    test_song1 = "battle5"  # input("song: ")
    test_song2 = "song2"  # input("song: ")
    run = True
    while run:
        clock.tick(30)
        handle()
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    print(sound_effect_list)
                    play_effect("magic5")
                if event.key == pygame.K_a:
                    play(test_song1, resume=True)
                if event.key == pygame.K_s:
                    play(test_song1, resume=False, delay_ms=50000)
                if event.key == pygame.K_d:
                    play(test_song1, resume=False)
                if event.key == pygame.K_f:
                    play(test_song1, resume=True, delay_ms=50000)
                if event.key == pygame.K_r:
                    print(get_pos())
                    print(song_delay[get_current_song()])
                    print(get_song_len())
                if event.key == pygame.K_p:
                    print(now_playing)
                    play("death_song", delay_ms=get_pos()+song_delay["death_song"])
        pygame.display.update()
