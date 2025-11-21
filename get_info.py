import yt_dlp
import requests
from PIL import Image
from io import BytesIO

class video:
    def __init__(self, url):
        self.url = url
        self.info = None
        self.duration = None
    
    def getInformations(self):
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(self.url, download=False)
            self.info = info
            return self.info
    
    def GetImage(self):
        # gitting the image from the thumbnail url
        response = requests.get(self.info['thumbnail'])

        # store the image as bytes
        image_bytes = response.content

        # convert bytes to a PhotoImage
        image = Image.open(BytesIO(image_bytes))
        
        return image

    def getDuration(self):
        duration = self.info['duration']
        video_time = ""
        
        if duration < 60:
             # e.g. 0:45
            video_time = f"0:{duration:02d}"
            
        elif duration < 3600:
             # e.g. 12:05
            video_time = f"{duration//60}:{duration%60:02d}"
            
        else:
            # e.g. 2:05:30
            # The logic is the same, just cleaner to read
            hours = duration // 3600
            minutes = (duration % 3600) // 60
            seconds = duration % 60
            video_time = f"{hours}:{minutes:02d}:{seconds:02d}"

        self.duration = video_time