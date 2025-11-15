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
        """
        Downloads the video to a specific directory.
        :param save_directory: A string or Path object for the save location.
        """
        
        # Ensure the directory exists before trying to download
        Path(save_directory).mkdir(parents=True, exist_ok=True)

        downOptions = {
            # 1. Set the filename template
            # %(title)s uses the video's title
            # %(ext)s uses the correct file extension (e.g., .mp4)
            'outtmpl': '%(title)s.%(ext)s',
            
            # 2. Set the download path
            # This tells yt-dlp to use your 'save_directory' as the base path
            'paths': {'home': str(save_directory)}
        }
        
        with yt_dlp.YoutubeDL(downOptions) as downloader:
            downloader.download([self.url])
            
        print(f"Successfully downloaded: {self.title}")
        print(f"Saved to: {save_directory}")