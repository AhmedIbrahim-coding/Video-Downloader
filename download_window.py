import customtkinter as ctk
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