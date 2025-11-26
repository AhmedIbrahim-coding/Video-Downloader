import yt_dlp

class downloader:
    def __init__(self, location, video):
        self.location = location
        self.video = video
        self.progress = None

    def download_video(self):
        # get the video object that already determined above
        video = self.video

        # prepare the options 
        opt = {
            "no_warnings": True,
            "quiet": True,
            "outtmpl": f"{self.location}/%(title)s.%(ext)s",
            "format": f"bestvideo[width={video.width}][height={video.height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "merge_output_format": "mp4"
        }

        with yt_dlp.YoutubeDL(opt) as downloader:
            downloader.download(video.url)