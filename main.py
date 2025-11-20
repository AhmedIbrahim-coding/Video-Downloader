import customtkinter as ctk
from pytube import YouTube  
from get_info import video

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DownTube")
        self.geometry("500x200")
        self.resizable(False, False)
        self.video_link = None
        
        # Link entry
        self.linkEntry = ctk.CTkEntry(self,
                                       width=450,
                                       height=30,
                                       placeholder_text="Enter the video link here...",
                                       corner_radius=3,
                                       font=("Arial", 14))
        self.linkEntry.pack(pady=20)

        # start download button
        self.download_button = ctk.CTkButton(self,
                                             text="Download",
                                             width=80,
                                             height=30,
                                             corner_radius=3,
                                             font=("Arial", 14),
                                             command=self.check_excistance)
        self.download_button.pack(pady=10)

        # create a variable to hold error text
        self.error_text = None

    def check_excistance(self):
        # remove previous error text if exists
        if(self.error_text):
            self.error_text.destroy()

        # check if the link is valid
        try:
            self.video_link = YouTube(self.linkEntry.get())
            self.error_text = None # keep the error_text as None if successful
            self.download_options()
        except Exception:
            # display error message
            self.error_text = ctk.CTkLabel(self,
                                           text="Invalid URL. Please try again.",
                                           text_color="red",
                                           font=("Arial", 12))
            self.error_text.place(relx=0.5, y=150, anchor='center')
    
    def download_options(self):
        window = self.download_window = ctk.CTkToplevel(self)
        window.title("Download Options")
        window.geometry("720x360")
        window.resizable(False, False)
        window.grab_set()  # Make this window modal
        window.focus_set()

        # write a temorary lable to show that the download is being prepared
        label = ctk.CTkLabel(window, text="Preparing download....", font=("Arial", 32))
        label.place(relx=0.5, rely=0.5, anchor='center')
        
        new_video = video(self.video_link.watch_url) # crate a new video object and give it the url

        video_info = new_video.getInformations()
        print(video_info['title'])


if __name__ == "__main__":
    app = App()
    app.mainloop()