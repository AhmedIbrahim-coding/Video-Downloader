import yt_dlp
import requests
from PIL import Image
from io import BytesIO

class video:
    def __init__(self, url):
        self.url = url
        self.info = None
    
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
