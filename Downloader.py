import yt_dlp

class downloader:
    def __init__(self, location, video):
        self.location = location
        self.video = video

        self.progress = None
        self.downloaded = None

        self.video_total = video.total_size_bytes
        self.audio_total = 0

        self.downloaded_video = 0
        self.dowlnoaded_audio = 0

    def download_video(self):
        # get the video object that already determined above
        video = self.video

        # prepare the options 
        opt = {
            "no_warnings": True,
            "quiet": True,
            "outtmpl": f"{self.location}/%(title)s.%(ext)s",
            "format": f"bestvideo[width={video.width}][height={video.height}][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "merge_output_format": "mp4",
            "progress_hooks": [self.progress_Hook],
        }

        with yt_dlp.YoutubeDL(opt) as downloader:
            downloader.download(video.url)

    def progress_Hook(self, d):
        # get the statu and store it
        statu = d.get('status')

        if statu == 'downloading':
            # get the information and fomat about the statu
            info = d.get('info_dict', {})
            fmt = d.get('format_id', "")

            # check if it's downloading audio or not
            is_audio = ("audio" in fmt) or ("m4a" in fmt)

            # get the downloaded and the full size of the current format file
            downloaded = d.get('downloaded_bytes', 0)
            total = info.get('filesize') or info.get('filesize_approx') or 0

            # if the file format is audio, set the audio_total as total that we got in the previous line
            if is_audio and self.audio_total == 0 and total > 0: # just one time 
                self.audio_total = total

            # if the file format is audio, increase the downloaded_audio, if it's not, increase the downloaded_video
            if is_audio:
                self.dowlnoaded_audio = downloaded
            else:
                self.downloaded_video = downloaded

            # store the full downloaded from the video and the audio
            total_downloaded = self.downloaded_video + self.dowlnoaded_audio

            # update the progress value if the full downloaded > 0 
            if total_downloaded > 0:
                self.progress = (total_downloaded/ self.video_total) * 100

        else:
            # if the statu is merging the audio and video or finished, set the progress to 100
            self.progress = 100
        