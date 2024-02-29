"""
Created by A_Aphid (Youtube) / AboveAphid0 (Old Github) / AboveAphid (Github).
"""

import scrapetube, json, os
from pytube import YouTube

class pytubeFix():

    # Allows you to download the subtitles as a text file with neatened data like what .generate_srt_captions() should do however it doesn't work.
    class CaptionFix():
        def __init__(self) -> None:
            pass
        
        
        def downloadCaptions(self, json_captions, outpath=os.getcwd() + '\\subtitles.txt', encodinsg='utf8'):
            allDump = json_captions['events'] # List of all caption's dicts

            fileContents = ""
            i = 1 # Index of current subtitle
            for piece in allDump:
                start = piece['tStartMs']
                startTimestamp = self.convertMilliToTime(start)
                dur = piece['dDurationMs']
                end = start + dur
                endTimestamp = self.convertMilliToTime(end)
                text = ''

                # Goes through all the captions dicts and deciphers them
                for dictOfCap in piece['segs']: 
                    for encoding in dictOfCap.keys(): # Loops through all the possible encodings included and adds the text
                        
                        text += dictOfCap[encoding]
                        
                
                
                fileContents += f"{i}\n" + f"{startTimestamp} --> {endTimestamp} \n{text}\n\n"
                i += 1

            with open(outpath, 'wb') as f:
                f.write(fileContents.encode())


        def convertMilliToTime(self, millis):
            seconds=int(millis/1000)%60
            excessMilli = str(round(millis/1000%60 - seconds, 3))[2:]
            minutes=int(millis/(1000*60))%60
            hours=int(millis/(1000*60*60))%24
            
            es = self.addZeros(excessMilli, 3, False)
            ms = self.addZeros(hours, 2)
            ss = self.addZeros(seconds, 2)
            hs = self.addZeros(hours, 2)
            timestamp = f'{hs}:{ms}:{ss},{es}'
            return timestamp
        
        # Neatens the info. E.g. 1:32:1 to: 01:32:01 (Though does it on num at a time)
        def addZeros(self, num, amt, before=True):
            if len(str(num)) < amt:
                zeros = "0" * (amt - len(str(num)))
                if before:
                    return f'{zeros}{num}'
                else:
                    return f'{num}{zeros}'
            return str(num)
    
    # Gets all the videos in a channel and returns their object or link
    class ChannelVideoGetter():
        def __init__(self, channel_url=None, channel_id=None, channel_username=None):
            self.channel_url = channel_url
            self.channel_id = channel_id
            self.channel_username = channel_username



            

        def getVideoObjects(self):
            if self.channel_url:
                videos = scrapetube.get_channel(channel_url=self.channel_url)
            elif self.channel_id:
                videos = scrapetube.get_channel(channel_id=self.channel_id)
            elif self.channel_username:
                videos = scrapetube.get_channel(channel_username=self.channel_username)

            videosWithObj = []
            for video in videos:
                videoID = video['videoId']

                videoLink = f"https://www.youtube.com/watch?v={videoID}"

                yt = YouTube(videoLink)

                videosWithObj.append(yt)

            return videosWithObj
        
        def getVideoLinks(self):
            if self.channel_url:
                videos = scrapetube.get_channel(channel_url=self.channel_url)
            elif self.channel_id:
                videos = scrapetube.get_channel(channel_id=self.channel_id)
            elif self.channel_username:
                videos = scrapetube.get_channel(channel_username=self.channel_username)

            videosWithLinks = []
            for video in videos:
                videoID = video['videoId']

                videoLink = f"https://www.youtube.com/watch?v={videoID}"

                videosWithLinks.append(videoLink)

            return videosWithLinks



if __name__ == "__main__":
    fix = pytubeFix()
    with open('.\\captions\\YouTube Rewind 2019- For the Record - #YouTubeRewind-Captions.json', 'rb') as f:
        jsonStuff = json.load(f)


    capFix = fix.CaptionFix()

    capFix.downloadCaptions(jsonStuff)#, encoding='utf8')