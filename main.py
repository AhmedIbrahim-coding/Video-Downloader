import customtkinter as ctk
from pytube import YouTube
from download_window import download_options


# creating the main window
main_window = ctk.CTk()
main_window.title("Youtube Downloader")
main_window.geometry("500x200")
main_window.resizable(False, False) # make it's not possible to resize the window


# creating an entry field to get the video link
linkEntry = ctk.CTkEntry(main_window, placeholder_text="Enter the url....", width=450, height=30,corner_radius=3, font=("Arial", 14))
linkEntry.pack(pady=20)

# function to prepare the download
def prepareDownload():
    errorText = None # create a variable to store error massages

    # ckeck if the video exists
    try:
        link = YouTube(linkEntry.get()) # ask the Youtube object to verify the link
        
        if errorText:  # if there was an error message before, remove it
            errorText.destroy()
            errorText = None

        download_options(link, main_window) # open the download options window

    except Exception:
        # if an error occurs, show an error message
        errorText = ctk.CTkLabel(main_window, text="Invalid URL. Please try again.", font=("Arial", 12), text_color="red")
        errorText.place(relx=0.5, y=150, anchor='center')


# creating a download button
downloadButton = ctk.CTkButton(main_window, text = "Download", width=80, height= 30, corner_radius=3, font=("Arial", 14), command=prepareDownload)
downloadButton.pack(pady=10)

# running the main loop
main_window.mainloop()