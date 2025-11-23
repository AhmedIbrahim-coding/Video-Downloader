import yt_dlp
import requests
from PIL import Image
from io import BytesIO

class video:
    def __init__(self, url):
        self.url = url
        self.info = None
        self.duration = None
        self.size = None
        self.quality = None
        self.height = None
        self.width = None
        self.progress = 0
    
    def getInformations(self):
        options = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'format': 'bestvideo+bestaudio'
        }
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(self.url, download=False)
            self.info = info
            # set video as the best quality based on height and width
            if self.info['height'] and self.info['width']:
                self.height = self.info['height']
                self.width = self.info['width']
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

    def getSize(self):
        # set an initial size of 0 bytes
        size_in_bytes = 0

        # git the size from the info dict
        size_in_bytes = self.info.get('filesize') or self.info.get('filesize_approx') or 0


        # convert size to MB or GB
        if size_in_bytes > 0:
            size_in_mb = size_in_bytes / (1024 * 1024)

            if size_in_mb > 1000:
                size_in_gb = size_in_mb / (1024)
                self.size = f"{size_in_gb:.2f} GB"
            else:
                self.size = f"{size_in_mb:.2f} MB"
        else:
            # if size could not be determined just set it to unknown
            self.size = " Unknown Size"

    def downloadVideo(self, download_path):

        options = {
            'outtmpl': f'{download_path}/%(title)s.%(ext)s',
            'format': 'best',
            'quiet': True,
            'no_warnings': True,
            'progress_hooks': [self.progress_hook],
        }

        with yt_dlp.YoutubeDL(options) as downloader:
            downloader.download([self.url])


    def progress_hook(self, d):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
            percent = downloaded / total * 100

            self.progress = percent