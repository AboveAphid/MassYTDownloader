import os, sys, urllib3, json, tkinter as tk, time
from tkinter import filedialog, ttk, messagebox, scrolledtext
from threading import Thread
# from ChannelVideoGetter import ChannelVideoGetter
from pytubeFix import pytubeFix
from pytube import YouTube, Playlist
from pprint import pprint
from queue import Queue

def cleanseTitle(title:str):
    invalidChars = '<>:"/\|?*'
    for char in invalidChars:
        title = title.replace(char, '-')
    return title

def removeDuplicates(dups):
    return list(dict.fromkeys(dups))








videos = []
destinationDir = ''
numOfWorkers = 5


print('Waiting for video links through menu prompt...')


root = tk.Tk() 
  
root.title("Youtube Mass Downloader") 
  
ttk.Label(root, text="Youtube Mass Downloader", 
          font=("Times New Roman", 15)).grid(row=0) 
ttk.Label(root, text="Enter video URLs seperated by a newline", font=("Bold", 12)).grid(row=1) 
  
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, 
                                      width=40, height=8, 
                                      font=("Times New Roman", 13)) 
text_area.grid(row=2, pady=10, padx=10) 

def submit(text_area:scrolledtext.ScrolledText):
    global videos, directoryVar, destinationDir, numOfWorkers, channelDownloadCheckButtonVar, channelDownloadEntryVar
    
    print('Recieved Videos:')
    val = text_area.get("1.0","end-1c")
    for possiblelink in val.splitlines():
        if possiblelink.strip() != '':
            cleansedLink = possiblelink.strip()
            print(cleansedLink)
            videos.append(cleansedLink)

    # Mass Channel Downloader (Downloads all the videos from a channel)
    if channelDownloadCheckButtonVar.get() == 1:
        if messagebox.askyesno('Youtube Mass Downloader', 'You have selected Mass Channel Downloader. \nThis downloads all videos from choosen channel. \n Are you sure you want to continue?'):
            print('Channel videos:')
            channelVideoGetter = pytubeFix.ChannelVideoGetter(channelDownloadEntryVar.get())
            channelVideos = channelVideoGetter.getVideoLinks()
            if channelVideos:
                link : str
                for link in channelVideos:
                    link = link.strip()
                    print('Added video from channel:', link)
                    videos.append(link.strip())

    if playlistDownloadCheckButtonVar.get() == 1:
        print('Playlist videos:')
        playlist = Playlist(playlistDownloadEntryVar.get())
        playlistVideos = playlist.video_urls
        if playlistVideos:
            link : str
            for link in playlistVideos:
                link = link.strip()
                print('Added video from playlist:', link)
                videos.append(link.strip())

    destinationDir = directoryVar.get()

    if destinationDir == '':
        destinationDir = os.getcwd()

    numOfWorkers = numOfWorkersVar.get()

    if subtitlesLangVar.get() == '':
        subtitlesLangVar.set('en')

    ans = messagebox.askyesnocancel('Mass Youtube Downloader', f'You have choosen to download {len(videos)} videos. \nAre you sure you want to continue?')

    if ans:
        messagebox.showinfo('Mass Youtube Downloader', 'Close this window to start downloading.')
        root.destroy()
    elif ans == False:
        pass
    else:
        root.destroy()
        Thread(target=messagebox.showwarning, args=('Mass Youtube Downloader', 'Exiting...')).start()
        videos = [] # Overide videos incase sys.exit doesn't work
        sys.exit(0)
            

def setDirectory():
    global destinationDir, directoryVar
    destinationDir = filedialog.askdirectory(initialdir=os.getcwd())
    destinationDir = destinationDir.replace('/', '\\')
    directoryVar.set(destinationDir)
    updateDirectoryEntrySize()


def updateDirectoryEntrySize():
    global directoryVar, directoryEntry
    lengthOfDirectory = len(directoryVar.get())
    if lengthOfDirectory > 30:
        directoryEntry.configure(width=lengthOfDirectory)
    else:
        directoryEntry.configure(width=50)


channelDownloadCheckButtonVar = tk.IntVar()
channelDownloadCheckButton = ttk.Checkbutton(root, text='Mass Channel Downloader', variable=channelDownloadCheckButtonVar)
channelDownloadCheckButton.grid(row=3, sticky=tk.W)

channelDownloadEntryVar = tk.StringVar()
channelDownloadEntry = ttk.Entry(root, textvariable=channelDownloadEntryVar,width=30)
channelDownloadEntry.grid(row=3, sticky=tk.W, padx=170)

tk.Label(root, text="(url)").grid(row=3, sticky=tk.W, padx=350)

playlistDownloadCheckButtonVar = tk.IntVar()
playlistDownloadCheckButton = ttk.Checkbutton(root, text='Playlist Downloader', variable=playlistDownloadCheckButtonVar)
playlistDownloadCheckButton.grid(row=4, sticky=tk.W)

playlistDownloadEntryVar = tk.StringVar()
playlistDownloadEntry = ttk.Entry(root, textvariable=playlistDownloadEntryVar,width=30)
playlistDownloadEntry.grid(row=4, sticky=tk.W, padx=160)

tk.Label(root, text="(url)").grid(row=4, sticky=tk.W, padx=345)

downloadVideosCheckButtonVar = tk.IntVar()
downloadVideosCheckButtonVar.set(1)
downloadVideosCheckButton = ttk.Checkbutton(root, text='Download Video', variable=downloadVideosCheckButtonVar)
downloadVideosCheckButton.grid(row=5, sticky=tk.W)

downloadThumbnailsCheckButtonVar = tk.IntVar()
downloadThumbnailsCheckButton = ttk.Checkbutton(root, text='Download Thumbnails', variable=downloadThumbnailsCheckButtonVar)
downloadThumbnailsCheckButton.grid(row=6, sticky=tk.W)

downloadSubtitlesCheckButtonVar = tk.IntVar()
downloadSubtitlesCheckButton = ttk.Checkbutton(root, text='Download Subtitles', variable=downloadSubtitlesCheckButtonVar)
downloadSubtitlesCheckButton.grid(row=7, sticky=tk.W)

subtitlesLangVar = tk.StringVar()
subtitlesLangVar.set('en')
subtitlesLangEntry = ttk.Entry(root, textvariable=subtitlesLangVar,width=5)
subtitlesLangEntry.grid(row=7, sticky=tk.W, padx=130)

tk.Label(root, text="(Language Code)").grid(row=7, sticky=tk.W, padx=170)

downloadInfoCheckButtonVar = tk.IntVar()
downloadInfoCheckButton = ttk.Checkbutton(root, text='Download Json Info', variable=downloadInfoCheckButtonVar)
downloadInfoCheckButton.grid(row=8, sticky=tk.W)

setDirButton = ttk.Button(root, text="Set Directory", command=setDirectory)
setDirButton.grid(row=9, sticky=tk.W)

directoryVar = tk.StringVar()
directoryEntry = ttk.Entry(root, textvariable=directoryVar,width=50)
directoryEntry.grid(row=9, sticky=tk.W, padx=90)

updatedDirectoryInputSizeButton = ttk.Button(root, text="Update", command=updateDirectoryEntrySize)
updatedDirectoryInputSizeButton.grid(row=9, sticky=tk.E)


numOfWorkersLabel = ttk.Label(root, text="Number Of Workers:")
numOfWorkersLabel.grid(row=10, sticky=tk.W)

numOfWorkersVar = tk.IntVar()
numOfWorkersVar.set(numOfWorkers)
numOfWorkersSpinBox = ttk.Spinbox(root, textvariable=numOfWorkersVar, from_ = 1, to = 30)
numOfWorkersSpinBox.grid(row=11, sticky=tk.W, padx=120)

submitButton = ttk.Button(root, text="Submit", command=lambda: submit(text_area))
submitButton.grid(row=12)



# placing cursor in text area 
text_area.focus() 
root.mainloop() 







def download(url, destination=os.getcwd(), downloadThumbnail=False, downloadSubtitles=False, downloadInfoJson=False, downloadVideo=True, subtitleLang='en'):
    if destination == '':
        destination = os.getcwd()


    
    try:
        if os.path.exists(f'{destination}') == False:
            os.mkdir(f'{destination}')

        if os.path.exists(f'{destination}\\videos.txt') == False:
            open(f'{destination}\\videos.txt', 'w').close()
        with open(f'{destination}\\videos.txt', 'a') as f:
            f.write(url + '\n')

        yt = YouTube(url)

        if yt.age_restricted:
            print('Video Age Restricted:', url, ' | Trying bypass...')
            yt.bypass_age_gate()
            print('Tried bypass.')



        title = yt.title
        cleansedTitle = cleanseTitle(title)


        video = yt.streams.get_highest_resolution()

        if downloadThumbnail:
            try:
                thumbnailURL = yt.thumbnail_url
            
                res = urllib3.request('GET', thumbnailURL)
                ext = os.path.splitext(thumbnailURL)[1].split('?')[0]
                print('Recieved EXT:', ext)
                
                if os.path.exists(f'{destination}\\thumbnails') == False:
                    os.mkdir(f'{destination}\\thumbnails')


                with open(f'{destination}\\thumbnails\\{cleansedTitle}-Thumbnail{ext}', 'wb') as f:
                    f.write(res.data)
            except:
                print('[ERROR] Failed to download thumbnail:', url)

        if downloadSubtitles:
            try:
                if subtitleLang == '':
                    subtitleLang = 'en'

                if os.path.exists(f'{destination}\\captions') == False:
                    os.mkdir(f'{destination}\\captions')
                
                if yt.captions:

                    # print('HAS CAPTIONS')

                    caption = yt.captions[subtitleLang]

                    jsonCaps = caption.json_captions

                    captionFix = pytubeFix.CaptionFix()
                    captionFix.downloadCaptions(jsonCaps, f'{destination}\\captions\\{cleansedTitle}-Captions.txt')


                else:
                    jsonCaps = {}

                if os.path.exists(f'{destination}\\captions\\json') == False:
                    os.mkdir(f'{destination}\\captions\\json')

                with open(f'{destination}\\captions\\json\\{cleansedTitle}-CaptionsJson.json', 'w') as f:
                    json.dump(jsonCaps, f)
            except:
                print('[ERROR] Failed to download subtitles:', url)


        
        if downloadInfoJson:
            try:    
                if os.path.exists(f'{destination}\\info') == False:
                    os.mkdir(f'{destination}\\info')

                infoJson = yt.vid_info

                
                jsonfilepath = f'{destination}\\info\\{cleansedTitle}-Info.json'
                with open(jsonfilepath, 'w') as f:
                    json.dump(infoJson, f)

                

                extraInfo = {
                    'publishDate': yt.publish_date.date().ctime(),
                    'author': yt.author,
                    'channelurl': yt.channel_url,
                    'channelid': yt.channel_id,
                    'keywords': yt.keywords,
                    'length': yt.length,
                    'views': yt.views,
                    'rating': yt.rating,
                    'metadata': {
                        'raw': yt.metadata.raw_metadata,
                        'normal': yt.metadata.metadata
                    }
                }

                # print(extraInfo)

                if os.path.exists(f'{destination}\\info\\clean') == False:
                    os.mkdir(f'{destination}\\info\\clean')

                cleanJsonfilepath = f'{destination}\\info\\clean\\{cleansedTitle}-Clean.json'
                with open(cleanJsonfilepath, 'w') as f:
                    json.dump(extraInfo, f)
            
                
                if os.path.exists(f'{destination}\\info\\descriptions') == False:
                    os.mkdir(f'{destination}\\info\\descriptions')
  
                descriptionfilepath = f'{destination}\\info\\descriptions\\{cleansedTitle}-Description.txt'
                with open(descriptionfilepath, 'wb') as f:
                    if yt.description:
                        f.write(yt.description.encode()) # We right it encoded because sometimes it can't decipher the chars
            except Exception as e:
                print('[ERROR] Failed to download info json:', url, ' Error:', e)

        if downloadVideo:
            try:
                if os.path.exists(f'{destination}\\videos') == False:
                    os.mkdir(f'{destination}\\videos')

                
                video.download(destination, f'{destination}\\videos\\{cleansedTitle}.mp4')
            except:
                print('[ERROR] Failed to download video:', url)

        return True, None
    except Exception as e:
        print(e)
        print('Failed to download:', url)
        return False, e

successfulDownloads = 0
problemedDownloads = []

class Worker(Thread): 
    def __init__(self, queue:Queue, savedirectory:str, WorkerID=0, doDownloadThumbnails=False, doDownloadSubtitles=False, doDownloadInfo=False, doDownloadVideo=True, doMassChannelDownload=False, subtitleLang='en'):
        self.queue = queue
        self.loop = True
        Thread.__init__(self)
        
        self.savedir = savedirectory
        self.subtitleLang = subtitleLang
        self.downloadThumbnails = doDownloadThumbnails
        self.downloadSubtitles = doDownloadSubtitles
        self.downloadInfo = doDownloadInfo
        self.downloadVideo = doDownloadVideo
        self.downloadChannel = doMassChannelDownload
        self.id = WorkerID
    
    def run(self):
        global successfulDownloads, problemedDownloads
        self.log('Started Running!')
        while self.loop:

            link = self.queue.get()

            completed = False
            error = None
            try:
                self.log(f"Downloading {link}")
                completed, error = download(link, self.savedir, self.downloadThumbnails, self.downloadSubtitles, self.downloadInfo, self.downloadVideo, self.subtitleLang)
                
            except Exception as e:
                self.log('Error in worker:', e)
                error = e
                pass
            finally:
                self.log("Downloaded successfully:", completed)
                
            if completed == False:
                self.log("Error while downloading:", error)
                problemedDownloads.append({'Link': str(link), 'Error':str(error)})
            else:
                successfulDownloads += 1

            self.queue.task_done()
            

        self.log('Finished!') # Idk how this isn't getting called when exiting tho whatever... :/

    def log(self, *args):
        newargs = []
        for i in args:
            newargs.append(str(i))
        print(f"[WORKER-{self.id}] {' '.join(newargs)}")


    def exit(self):

        self.log('Exiting...')
        self.loop = False







videos = removeDuplicates(videos)

options = {
    'masschanneldownload': channelDownloadCheckButtonVar.get(),
    'downloadVideos': downloadVideosCheckButtonVar.get(),
    'downloadThumbnails': downloadThumbnailsCheckButtonVar.get(),
    'downloadSubtitles': downloadSubtitlesCheckButtonVar.get(),
    'subtitleLang': subtitlesLangVar.get(),
    'downloadInfo': downloadInfoCheckButtonVar.get(),
    'directory': destinationDir,
    'numOfWorkers': numOfWorkers,
    'videos': videos
}



print('Recieved configuration:')
pprint(options)










saveDir = options['directory']
numberOfWorkers = options['numOfWorkers']
mass = options['videos']
subtitlesLang = options['subtitleLang']



if options['masschanneldownload'] == 1 or options['masschanneldownload'] == True:
    doMassChannelDownload = True
else:
    doMassChannelDownload = False
if options['downloadVideos'] == 1 or options['downloadVideos'] == True:
    doDownloadVideos = True
else:
    doDownloadVideos = False
if options['downloadThumbnails'] == 1 or options['downloadThumbnails'] == True:
    doDownloadThumbnails = True
else:
    doDownloadThumbnails = False
if options['downloadSubtitles'] == 1 or options['downloadSubtitles'] == True:
    doDownloadSubtitles = True
else:
    doDownloadSubtitles = False
if options['downloadInfo'] == 1 or options['downloadInfo'] == True:
    doDownloadInfo = True
else:
    doDownloadInfo = False




print('Starting workers...')

queue = Queue()

workers = []
for id in range(numberOfWorkers):
    worker = Worker(queue, saveDir, id, doDownloadThumbnails, doDownloadSubtitles, doDownloadInfo, doDownloadVideos, doMassChannelDownload, subtitlesLang)
    # Setting daemon to True will let the main thread exit even though the workers are blocking
    worker.daemon = True
    workers.append(worker)
    worker.start()
    

for link in mass:
    queue.put(link)

queue.join()

print('All work completed!')



for worker in workers:
    worker.exit()


resultsText = f"""Results
{successfulDownloads}/{len(mass)} videos successfully downloaded
{len(mass)-successfulDownloads} failed to download.
"""

messagebox.showinfo('Mass Youtube Downloader', 'Download complete.')
messagebox.showinfo('Mass Youtube Downloader', resultsText)

if problemedDownloads:
    print(problemedDownloads)
    failedDownloadsInfo = "Failed Downloads:"
    for dictInfo in problemedDownloads:
        failedDownloadsInfo += f"\n\nLink: {dictInfo['Link']}  \nError: {dictInfo['Error']}"
    
    messagebox.showwarning('Mass Youtube Downloader', failedDownloadsInfo)

if os.path.exists(f'{saveDir}\\logs.txt') == False:
    open(f'{saveDir}\\logs.txt', 'w').close()

with open(f'{saveDir}\\logs.txt', 'a') as f:
    f.write(f'\n\n\n======== {time.ctime()} ========\n')
    f.write(resultsText)
    if problemedDownloads:
        f.write(failedDownloadsInfo)
