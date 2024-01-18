from pytube import YouTube, Playlist
import pandas as pd
import re
import datetime 
import time
import warnings

warnings.filterwarnings("ignore")
df = pd.DataFrame()
time_today = datetime.datetime.today()


csv_loc = ('P:\\Projects\\Python\\Video_downloader\\download_history.csv')
d_loc = ('P:\\Projects\\Python\\Video_downloader\\Output')

state_toggle = True
while state_toggle == True:

    try:
        df = pd.read_csv(csv_loc,usecols=['Date', 'Title', 'Length','URL','Video Thumbnail','Channel','Channel URL'])
    except:
        df = pd.DataFrame(columns= ['Date', 'Title', 'Length','URL','Video Thumbnail','Channel','Channel URL'])
    
    video_link = input('Please provide a video link: ')
    if 'list=' in video_link:
        playlist_grab = Playlist(video_link)
        print('Playlist has been selected selected')
        
        print(f'\nDownloading: {playlist_grab.title}')

        link_i = 0
        for video in playlist_grab.videos:
            
            try:
                df = pd.read_csv(csv_loc,usecols=['Date', 'Title', 'Length','URL','Video Thumbnail','Channel','Channel URL'])
            except:
                df = pd.DataFrame(columns= ['Date', 'Title', 'Length','URL','Video Thumbnail','Channel','Channel URL'])

            try:
                download_vid = video.streams.get_highest_resolution()
                download_vid.download(d_loc)
                print(f'\nVideo Downloaded Successfully!\n{video.title}\nSaved in {d_loc}\n')

            
                link_i = link_i + 1
                list_link = playlist_grab.video_urls[link_i]
            except:
                pass

            time_secs = time.gmtime(video.length)
            time_long = time.strftime("%H:%M:%S",time_secs)
            
            df = df.append({'Date' : time_today,'Title' : video.title, 'Length': time_long, 'URL' : list_link, 'Video Thumbnail' : video.thumbnail_url,'Channel' : video.author, 'Channel URL' : video.channel_url}, ignore_index=True)
            df = df.to_csv(csv_loc)

        while True:
            confirm_exit = input('Would you like to Download anyting else? ').lower()
            if confirm_exit == 'yes' or confirm_exit == 'y': 
                break 

            elif confirm_exit == 'no' or confirm_exit == 'n':
                print('Exiting...')
                state_toggle = False
                break
            else:
                print("I don't know what that means...")

    else:
        if '/watch?v=' in video_link:
            video_link = re.sub('.*v=|&.*','',video_link)
            print(f'Link cleaned to https://www.youtube.com/watch?v={video_link}')
            clean_link = (f'https://www.youtube.com/watch?v={video_link}')


        if '/shorts/' in video_link:
            video_link = re.sub('.*/shorts/|&.*','',video_link)
            print(f'Link cleaned to https://www.youtube.com/shorts/{video_link}')
            clean_link = (f'https://www.youtube.com/shorts/{video_link}')


        
        try:
            yt = YouTube(clean_link)
            author = yt.author

            if yt.length > 901:
                print('\n**WARNING**\nVideo is longer than 15 minuites! Please be patient!\n**WARNING**\n') 

            download_vid = yt.streams.get_highest_resolution()

            download_vid.download(d_loc)

            time_secs = time.gmtime(yt.length)
            time_long = time.strftime("%H:%M:%S",time_secs)
            df = df.append({'Date' : time_today,'Title' : yt.title, 'Length': time_long, 'URL' : clean_link, 'Video Thumbnail' : yt.thumbnail_url,'Channel' : yt.author, 'Channel URL' : yt.channel_url},ignore_index=True)
                
            print(f'\nVideo Downloaded Successfully!\n{yt.title}\nSaved in {d_loc}\n')

            df = df.to_csv(csv_loc)

            while True:
                confirm_exit = input('Would you like to Download anyting else? ').lower()
                if confirm_exit == 'yes' or confirm_exit == 'y': 
                    break 

                elif confirm_exit == 'no' or confirm_exit == 'n':
                    print('Exiting...')
                    state_toggle = False
                    break
                else:
                    print("\nI don't know what that means...")
                    
        except:
            print('An error occured.')



