import customtkinter as ctk
from get_info import video

def download_options(url, main_window):
    window = ctk.CTkToplevel(main_window)
    window.title("Download Options")
    window.geometry("720x360")
    window.resizable(False, False)
    window.grab_set()  # Make this window modal
    window.focus_set()

    # write a temorary lable to show that the download is being prepared
    label = ctk.CTkLabel(window, text="Preparing download....", font=("Arial", 32))
    label.place(relx=0.5, rely=0.5, anchor='center')

    newVideo = video(url)
    info = newVideo.getInformations()
    label.destroy()  # remove the temporary label
    # show video title
    titleText = ctk.CTkLabel(window, text=info['title'])
    titleText.pack(pady=20)