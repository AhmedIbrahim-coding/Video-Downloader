import yt_dlp

class video:
    def __init__(self, url):
        self.url = url
    
    def getInformations(self):
        with yt_dlp.YoutubeDL({}) as ydl:
            info = ydl.extract_info(self.url, download=False)
            return info