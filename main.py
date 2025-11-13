import customtkinter as ctk    # using customtkinter to create a UI app
from videoInfo import video

# creating the main window
root = ctk.CTk()
root.geometry("800x240")
root.title("DownTube")


lable_statment = None   # the statement of the video (none is an initial value)

def downOptions(link):
    newVideo = video(link)
    newVideo.getInfo()

    # creating a new child window for downloading options
    downWindow = ctk.CTkToplevel(root)
    downWindow.geometry("720x360")
    downWindow.title("Download Options")
    downWindow.grab_set()
    downWindow.transient(root)
    
    # display the video's title
    titleText = newVideo.title
    if len(titleText) > 32:
        titleText = titleText[0:33] + "....."
    
    textLabel = ctk.CTkLabel(downWindow, text=titleText, font=("Arial", 20))
    textLabel.place(x= 370, y= 20)

    
    # display the video's thumbnail
    pil_image = ctk.CTkImage(light_image=newVideo.image, dark_image=newVideo.image, size=(320, 180))
    image_label = ctk.CTkLabel(downWindow, image=pil_image, text="")
    image_label.place(x=30, y=20)




def PrepareDownload():
    # store the url
    link = linkEntry.get()


    # call the statement variable as global
    global lable_statment


    # remove anything inside the statement variable
    if lable_statment:
        lable_statment.destroy()
        lable_statment = None


    # check the existance of the url
    try:
        downOptions(link)
    except Exception:
        # put a lable inside statement variable
        lable_statment = ctk.CTkLabel(root, text="Not found!", font=ctk.CTkFont(size=15), text_color="red")
        lable_statment.pack()


# the entry place that takes the video link
linkEntry = ctk.CTkEntry(root, placeholder_text="Put the link here....", width=720, height=35, font=ctk.CTkFont(size=15))
linkEntry.pack(pady=20, padx=20)

# creating a button to start preparing to download the video
downBut = ctk.CTkButton(root, text="Download", font=ctk.CTkFont(family="Arial", size=12, weight="bold"), width=80, height=30, command=PrepareDownload)
downBut.pack(pady=30)

# keep appearing the window
root.mainloop()