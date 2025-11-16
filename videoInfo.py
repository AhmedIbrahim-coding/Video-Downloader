import yt_dlp
import requests
import io
from PIL import Image
from pathlib import Path

class video:
    def __init__(self,url):
        self.url = url
        self.title = None  # Initialize title
        self.image = None  # Initialize image

    def getInfo(self):
        with yt_dlp.YoutubeDL({}) as extractor:
            info = extractor.extract_info(self.url, download=False)

            # store the title in a new variable
            self.title = info.get('title')

            # store the image in a new variable
            video_Thumbnail_url = info.get('thumbnail') # store the image's url
            imageData = requests.get(video_Thumbnail_url).content  # download the image data
            imageFile = io.BytesIO(imageData) # store it in the memory
            pil_image = Image.open(imageFile) # convert it into a pillow image
            self.image = pil_image # store it in a variable

    # --- MODIFIED METHOD ---
    def Download(self, save_directory):
        pass