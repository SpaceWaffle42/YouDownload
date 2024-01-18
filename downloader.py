from pytube import YouTube, Playlist, Channel
import os
import pathlib 
import re

def directories(DIR_DATA):
    dir_check_data = os.path.isdir(DIR_DATA)

    if dir_check_data == False:
        os.mkdir(os.path.join(DIR_DATA))
        print("Data folder created.")

def download_video(quality,video):
    yt = YouTube(video, use_oauth=True, allow_oauth_cache=True)
    py_path = pathlib.Path(__file__).parent.resolve()

    DIR_DATA = os.path.join(py_path, "data")
    directories(DIR_DATA)
    if quality != 'highest':
        try:
            video = yt.streams.filter(res=f'{quality}p').first().download(DIR_DATA)
        except: 
            print(f'Error: Resolution does not exist for video "{yt.author}"! downloading highest quality.')
            video = yt.streams.get_highest_resolution().download(DIR_DATA)
    else: video = yt.streams.get_highest_resolution().download(DIR_DATA)
    
def downloader(link,quality,audio_mode):
    try:
        if '/watch?v=' in link or '/shorts/' in link or 'youtu.be' in link:
            if '/watch?v=' in link:
                video = re.sub('.*v=|&.*','',link)

            if '/shorts/' in link:
                video = re.sub('.*/shorts/|&.*','',link)
            if 'youtu.be' in link:
                video = re.sub('.*be/','',link)
            video = (f'https://www.youtube.com/watch?v={video}')

            download_video(quality,video)

        if 'playlist?list=' in link:
            playlists = Playlist(link)
            for i, _ in enumerate(playlists.videos, start=1):
                try:
                    video = playlists.video_urls[i-1]
                    download_video(quality,video)
                except Exception as e:
                    print(f'Error: {e}')
        print(f"link: {video}")
        print(f"quality: :{quality}")
        print(f"Audio: {audio_mode}")
    except Exception as e:
        print(f'Error: {e}')