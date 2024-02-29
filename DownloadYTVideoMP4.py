import os, sys, urllib3
from pytube import YouTube 
from tkinter import filedialog
from tkinter import messagebox
from pprint import pprint
  
# url input from user 
yt = YouTube( 
    str(input("Enter the URL of the video you want to download: \n>> "))) 
  
video = yt.streams.get_highest_resolution()




print('Found video:', yt.title)
pprint(yt.vid_info)

print('Waiting for comfirmation through dialog box...')
if False == messagebox.askyesno('Youtube MP4 Downloader', f'Is "{yt.title}" the correct video?'):
    print('Recieved: Wrong video, cancel download.')
    sys.exit(0)
print('Recieved: Correct video, continue with download.')

# check for destination to save file 
# print("Enter the destination (leave blank for current directory)") 
# destination = str(input(">> ")) or '.'
print('Waiting for comfirmation through file dialog prompt...')
destination = filedialog.askdirectory(initialdir=os.getcwd())
print('Recieved.')
print('Download Destination:', destination)

print('Waiting for comfirmation through dialog box...')
if messagebox.askyesno('Youtube MP4 Downloader', f'Download thumbnail?'):
    thumbnailURL = yt.thumbnail_url
    
    res = urllib3.request('GET', thumbnailURL)
    ext = os.path.splitext(thumbnailURL)[1].split('?')[0]
    print('Recieved EXT:', ext)
    
    with open(f'{destination}/{yt.title.replace("|", "-")}-Thumbnail{ext}', 'wb') as f:
        f.write(res.data)


print('Downloading...')
# download the file 
out_file = video.download(output_path=destination, max_retries=2) 
print('Saving...')

# save the file 
# base, ext = os.path.splitext(out_file) 
# new_file = base + '.mp4'
# os.rename(out_file, new_file) 
print('Download & Save complete!')

# result of success 
print(yt.title + " has been successfully downloaded. As a MP4")