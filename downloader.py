from pytube import YouTube, Playlist, Channel
import os
import pathlib
import re


def directories(DIR_DATA):
    dir_check_data = os.path.isdir(DIR_DATA)

    if dir_check_data == False:
        os.mkdir(os.path.join(DIR_DATA))
        print("Data folder created.")


def download_video(quality, video):
    yt = YouTube(video, use_oauth=True, allow_oauth_cache=True)
    py_path = pathlib.Path(__file__).parent.resolve()
    DIR_DATA = os.path.join(py_path, "data")

    directories(DIR_DATA)
    video_name = re.sub(r'[\\/:*?"<>|]', "", yt.title).replace(" ", "_")
    video_name = f"{video_name}.mp4"

    if quality != "highest":
        try:
            video = yt.streams.filter(res=f"{quality}p").first().download(DIR_DATA)
        except:
            print(
                f'Error: Resolution does not exist for video "{yt.title}"! downloading highest quality.'
            )
            video = yt.streams.get_highest_resolution().download(
                DIR_DATA, filename=video_name
            )
    else:
        video = yt.streams.get_highest_resolution().download(
            DIR_DATA, filename=video_name
        )
    return os.path.join(DIR_DATA, video_name)


def download_audio(video):
    yt = YouTube(video, use_oauth=True, allow_oauth_cache=True)
    py_path = pathlib.Path(__file__).parent.resolve()
    DIR_DATA = os.path.join(py_path, "data")

    directories(DIR_DATA)
    video_name = re.sub(r'[\\/:*?"<>|]', "", yt.title).replace(" ", "_")
    video_name = f"{video_name}.mp3"
    video = (
        yt.streams.filter(only_audio=True)
        .first()
        .download(DIR_DATA, filename=video_name)
    )
    return os.path.join(DIR_DATA, video_name)


def downloader(link, quality, audio_mode):
    video_id = None
    if "https://www.youtube.com" in link or "https://youtu.be" in link:
        try:
            if "/watch?v=" in link or "/shorts/" in link or "youtu.be" in link:
                if "/watch?v=" in link:
                    video_id = re.sub(".*v=|&.*", "", link)

                if "/shorts/" in link:
                    video_id = re.sub(".*/shorts/|&.*", "", link)
                if "youtu.be" in link:
                    video_id = re.sub(".*be/", "", link)
                video = f"https://www.youtube.com/watch?v={video_id}"

                if audio_mode == "False":
                    file_path = download_video(quality, video)

                if audio_mode == "True":
                    file_path = download_audio(video)

                return video_id, file_path

            if "playlist?list=" in link:
                playlists = Playlist(link)
                for i, _ in enumerate(playlists.videos, start=1):
                    try:
                        video = playlists.video_urls[i - 1]
                        if audio_mode == "False":
                            file_path = download_video(quality, video)

                        if audio_mode == "True":
                            file_path = download_audio(video)

                    except Exception as e:
                        print(f"Error: {e}")
                    return video_id, file_path

            print(f"ID: {video_id}")
            print(f"link: {video}")
            print(f"quality: {quality}")
            print(f"Audio: {audio_mode}")

        except Exception as e:
            print(f"Error: {e}")
            return None
    else:
        print("No valid link provided!")
        return None
