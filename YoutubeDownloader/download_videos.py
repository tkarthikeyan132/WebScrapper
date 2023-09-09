import pandas as pd
import urllib.request
import os
from bs4 import BeautifulSoup
import requests
from pytube import YouTube
import json

def get_new_urls(urls):
    try:
        youtube_collected_ids = []
        for file_name in os.listdir("youtube_videos"):
            if ".mp4" in file_name:
                youtube_collected_ids.append(file_name.split('.mp4')[0])
    except:
        os.system('mkdir -p youtube_videos')
        youtube_collected_ids = []

    youtube_urls = [
        url for url in urls if ("youtube" in url and url.split("?v=")[1].split("&")[0] not in youtube_collected_ids)
    ]
    return youtube_urls

def download_youtube_videos(youtube_urls):
    error_urls = []
    for video_url in youtube_urls:
        try:
            stream = YouTube(video_url).streams.filter(progressive=True, subtype='mp4').order_by('resolution').desc().first()
            if not stream:
                raise
            stream.download(filename=f'youtube_videos/{video_url.split("?v=")[1].split("&")[0]}.mp4')
        except:        
            error_urls.append(video_url)
    if len(error_urls):
        try:
            with open('youtube_error_urls.txt', 'r') as f:
                original_error_urls = f.read().split('\n')
        except:
            os.system('touch youtube_error_urls.txt')
            original_error_urls = []
        error_urls.extend(original_error_urls)
        error_urls = list(set(error_urls))
        with open('youtube_error_urls.txt', 'w') as f:
            f.write('\n'.join(error_urls))

## Code change starts
# mode = 1 means normal mode, mode = 2 means error mode
MODE = 2
urls = []
if MODE == 1:
    print("MODE 1: NORMAL")
    json_file = open('/home/tkarthikeyan/IIT Delhi/RP/rp/WebScrapper/class5math.json','r')
    data = json.load(json_file)
    print("#entries ", len(data))
    for d in data:
        url_new = "https://www.youtube.com/watch?v="
        urls.append(url_new+d['vid'])
    # print("urls=",urls)
    print("#video links ",len(urls))
    json_file.close()
elif MODE == 2:
    print("MODE 2: ERROR")
    txt_file = open("error_urls.txt", 'r')
    for line in txt_file:
        # Strip any leading/trailing whitespace and add the URL to the list
        urls.append(line.strip())
## Code change ends

# urls = ["https://www.youtube.com/watch?v=Qh1B2xfbhgg"]
youtube_urls = get_new_urls(urls)
print(youtube_urls)
download_youtube_videos(youtube_urls)
print("COMPLETED")