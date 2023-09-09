import os
import json
from collections import Counter

# Specify the path to your folder containing videos
folder_path = "/home/tkarthikeyan/IIT Delhi/RP/rp/YoutubeDownloader/class5videos_not_complete"

# Read the list of video names from the text file
# with open("video_list.txt", "r") as file:
#     video_names = [line.strip() for line in file]
urls=[]
json_file = open('/home/tkarthikeyan/IIT Delhi/RP/rp/WebScrapper/class5math.json','r')
data = json.load(json_file)
print("#entries ", len(data))
for d in data:
    # url_new = "https://www.youtube.com/watch?v="
    urls.append(d['vid']+".mp4")
# print("urls=",urls)
print("#video links ",len(urls))

c= Counter(urls)
for k,v in c.items():
    if v>1:
        print(k,v)
print('counts checked')


print("#unique video links ", len(set(urls)))
json_file.close()

# Get a list of files in the folder
folder_files = os.listdir(folder_path)


# Initialize a list to store missing videos
missing_videos = []

# Compare the lists and find missing videos
for video_name in urls:
    if video_name not in folder_files:
        print("missing video ",video_name)
        missing_videos.append(video_name)

# Print the missing videos
if missing_videos:
    print("Missing videos:")
    for video in missing_videos:
        print(video)
else:
    print("All videos are present in the folder.")