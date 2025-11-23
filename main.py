import customtkinter as ctk
from get_info import video
import threading
from PIL import Image
from tkinter import filedialog
import os

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DownTube")
        self.geometry("500x200")
        self.resizable(False, False)
        self.video_link = None
        self.video_info = None
        self.download_location = os.path.join(os.path.expanduser("~"), "Downloads")
        
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

        # We just get the text here. The validation happens in the thread now.
        self.video_link = self.linkEntry.get()
        
        # Check if the link is empty
        if(not self.video_link):
            self.main_error_massage("Please enter a video link.")
            return
        # 1. Open the window immediately
        self.download_options()
        self.error_text = None 
    
    def download_options(self):
        window = self.download_window = ctk.CTkToplevel(self)
        window.title("Download Options")
        window.geometry("720x360")
        window.resizable(False, False)
        window.grab_set()  # Make this window modal
        window.focus_set()

        # write a temorary lable to show that the download is being prepared
        self.temp_label_massage = ctk.CTkLabel(window, text="Preparing download....", font=("Arial", 32))
        self.temp_label_massage.place(relx=0.5, rely=0.5, anchor='center')
        
        new_video = video(self.video_link) # crate a new video object
        
        # 2. Start the thread (Fixed the tuple syntax here too)
        threading.Thread(target=self.fetch_video_info, args=(new_video,)).start()


    def fetch_video_info(self, video_obj):
            try:
                # 1. Get the info
                video_info = video_obj.getInformations()
                
                # 2. CHECK: Is it actually a video?
                is_live = video_info.get('is_live', False)
                duration = video_info.get('duration')

                if not duration and not is_live:
                    raise Exception("Link is a Page, not a Video")

                # 3. If we passed the check, save it and update GUI
                self.video_info = video_info
                self.after(0, self.display_video_info, video_obj)
            except Exception:
                # 4. Display the error on the main screen
                self.after(0, self.handle_error)

    def handle_error(self):
        # This function runs on the Main Thread when triggered by the background thread
        self.main_error_massage("Invalid URL. Please try again.")
        
        if self.download_window:
            self.download_window.destroy()

    def main_error_massage(self, massage):
            # display error message
            self.error_text = ctk.CTkLabel(self,
                                           text=massage,
                                           text_color="red",
                                           font=("Arial", 12))
            self.error_text.place(relx=0.5, y=150, anchor='center')

    def display_video_info(self, video_obj):
        # create a local reference to the download window
        window = self.download_window

        # Clear previous widgets
        for widget in window.winfo_children():
            widget.destroy()

        # create a frame to hold title and thumbnail
        top_frame = ctk.CTkFrame(window, width=700, height=200, fg_color="#1A1A1A", corner_radius=3)
        top_frame.pack(pady=10)

        # display video thumbnail
        video_thmb = video_obj.GetImage()
        image = ctk.CTkImage(light_image= video_thmb,
                             dark_image= video_thmb,
                             size=(320, 180))
        thumbnail_label = ctk.CTkLabel(top_frame, image=image, text="")
        thumbnail_label.place(x=10, y=10)

        # display video title
        title = self.video_info['title']
        if len(title) > 33:
            title = title[:30] + " ..."
        video_title = ctk.CTkLabel(top_frame,
                                    text=title,
                                    font=("Arial", 20))
        video_title.place(x=350, y=20)

        # display video duration
        pil_duration_icon = Image.open("Duration_icon.png")
        duration_icon = ctk.CTkImage(light_image= pil_duration_icon,
                                     dark_image= pil_duration_icon,
                                     size=(20, 20))
        duration_icon_label = ctk.CTkLabel(top_frame, image=duration_icon, text="")
        duration_icon_label.place(x=350, y=70)

        video_obj.getDuration()
        duration_label = ctk.CTkLabel(top_frame,
                                      text=video_obj.duration,
                                      font=("Arial", 13))
        duration_label.place(x=375, y=70)

        # display video file size
        pil_size_icon = Image.open("Size_icon.png")
        size_icon = ctk.CTkImage(light_image= pil_size_icon,
                                 dark_image= pil_size_icon,
                                 size=(20, 20))
        size_icon_label = ctk.CTkLabel(top_frame, image=size_icon, text="")
        size_icon_label.place(x=350, y=100)

        video_obj.getSize()
        size_label = ctk.CTkLabel(top_frame,
                                  text=video_obj.size,
                                  font=("Arial", 13))
        size_label.place(x=375, y=100)

        # display video quality
        pil_display_icon = Image.open("Display_icon.png")
        display_icon = ctk.CTkImage(light_image= pil_display_icon,
                                    dark_image= pil_display_icon,
                                    size=(20, 20))
        display_icon_label = ctk.CTkLabel(top_frame, image=display_icon, text="")
        display_icon_label.place(x=350, y=130)

        quality_label = ctk.CTkLabel(top_frame,
                                     text=f"{video_obj.width}x{video_obj.height}" if video_obj.height and video_obj.width else "Unknown Quality",
                                     font=("Arial", 13))
        quality_label.place(x=375, y=130)


        # Choose download location path and button_browse
        location_frame = ctk.CTkFrame(window, width=400, 
                                      height=32, 
                                      fg_color="#1A1A1A", 
                                      corner_radius=1)
        location_frame.place(x=10, y=230)

        # display location icon
        pil_location_icon = Image.open("Location_icon.png")
        location_icon = ctk.CTkImage(light_image= pil_location_icon,
                                     dark_image= pil_location_icon,
                                     size=(25, 25))
        location_icon_label = ctk.CTkLabel(location_frame, image=location_icon, text="")
        location_icon_label.place(x=5, y=1.5)

        # display current download location & make it accessible for other methods
        self.location_label = ctk.CTkLabel(location_frame, text=self.download_location, font=("Arial", 14))
        self.location_label.place(x=32, y=2)

        choose_location_button = ctk.CTkButton(window,
                                               text="Browse",
                                               width=80,
                                               height=30,
                                               corner_radius=1,
                                               font=("Arial", 14),
                                               command=self.choose_location)
        choose_location_button.place(x=410, y=231)

        # Download button
        self.start_download_button = ctk.CTkButton(window,
                                              text="Start",
                                              width=100,
                                              height=30,
                                              corner_radius=3,
                                              font=("Arial", 16),
                                              command=lambda: self.DownloadVideo(video_obj))
        self.start_download_button.place(x=600, y=310)

    def choose_location(self):
        # get the download path from the user
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            # set the download locatoin variable
            self.download_location = folder_selected
            self.location_label.configure(text=self.download_location)

    def DownloadVideo(self, video_obj):
        # Remove the start download button
        if hasattr(self, 'start_download_button'):
            self.start_download_button.destroy()
        
        # Create a ProgressBar in place of the button
        self.progress_bar = ctk.CTkProgressBar(self.download_window, width=400)
        self.progress_bar.place(x=150, y=310)
        
        # Create a label to display the percentage
        self.progress_label = ctk.CTkLabel(self.download_window, text="0%", font=("Arial", 14))
        self.progress_label.place(x=360, y=315)

        # Store the last progress value to avoid jitter
        self.last_progress = 0

        # Start the download in a separate thread
        thread = threading.Thread(target=video_obj.downloadVideo, args=(self.download_location,))
        thread.start()

        # Start updating the ProgressBar
        self.update_progress_bar(video_obj)

    def update_progress_bar(self, video_obj):
        # Prevent updating if the ProgressBar or Toplevel has been destroyed
        if not hasattr(self, 'progress_bar') or not self.progress_bar.winfo_exists():
            return

        # Update the value while preventing backward movement
        current_value = video_obj.progress / 100
        current_value = max(current_value, getattr(self, 'last_progress', 0))
        self.progress_bar.set(current_value)
        self.last_progress = current_value

        # Update the percentage label
        if hasattr(self, 'progress_label') and self.progress_label.winfo_exists():
            self.progress_label.configure(text=f"{int(current_value*100)}%")

        # Continue updating every 20 milliseconds until it reaches 100%
        if current_value < 1:
            self.after(20, self.update_progress_bar, video_obj)
        else:
            self.progress_bar.destroy()
            done_label = ctk.CTkLabel(self.download_window, text="--Done--", text_color="green", font=("Arial", 14))
            done_label.place(relx=0.5, y=310, anchor='center')

            
if __name__ == "__main__":
    app = App()
    app.mainloop()