import customtkinter as ctk
from videoInfo import video
from tkinter import filedialog  # --- ADD THIS ---
from pathlib import Path      # --- ADD THIS ---

# creating the main window
root = ctk.CTk()
root.geometry("800x240")
root.title("DownTube")

lable_statment = None

def downOptions(link):
    newVideo = video(link)
    newVideo.getInfo()

    # creating a new child window for downloading options
    downWindow = ctk.CTkToplevel(root)
    downWindow.geometry("720x360")
    downWindow.title("Download Options")
    downWindow.grab_set()
    downWindow.transient(root)
    downWindow.resizable(False, False)

    # a frame that containes the video image & title
    topFrame = ctk.CTkFrame(downWindow, width=700, height=220, fg_color="#141414")
    topFrame.pack(padx=10,pady=10)
    
    #    We'll use the Downloads folder as the default.
    downWindow.chosen_directory = Path.home() / "Downloads"

    # 2. Create a frame to hold the directory widgets
    dir_frame = ctk.CTkFrame(downWindow, width=700, height=40)
    dir_frame.pack(padx=10, pady=0) # Pack it right below the topFrame

    # 3. Create a label to show the currently selected path
    dir_label_text = f"Save to: {downWindow.chosen_directory}"
    dir_label = ctk.CTkLabel(dir_frame, text=dir_label_text, font=("Arial", 12))
    dir_label.place(x=10, y=8) # Positioned inside the new frame

    # 4. Define the function that the "Select Folder" button will call
    def select_directory_command():
        """Opens the dialog and updates the path"""
        chosen_path = filedialog.askdirectory(initialdir=downWindow.chosen_directory)
        
        if chosen_path: # Only update if the user didn't cancel
            # Update the variable stored in the window
            downWindow.chosen_directory = Path(chosen_path)
            
            # Update the label's text
            new_text = f"Save to: {downWindow.chosen_directory}"
            dir_label.configure(text=new_text)

    # 5. Create the "Select Folder" button
    select_button = ctk.CTkButton(
        dir_frame,
        text="Select Folder",
        width=100,
        font=("arial", 12),
        command=select_directory_command  # Link to our new function
    )
    select_button.place(x=590, y=5) # Positioned inside the new frame

    # We use a 'lambda' to pass the chosen directory to the Download function
    startDown = ctk.CTkButton(
        downWindow,
        text="Start",
        height=30,
        width=80,
        font=("arial", 15),
        command=lambda: newVideo.Download(downWindow.chosen_directory)
    )
    startDown.place(x=600, y=300)

    # display the video's title
    titleText = newVideo.title
    if len(titleText) > 32:
        titleText = titleText[0:33] + "....."
    
    textLabel = ctk.CTkLabel(topFrame, text=titleText, font=("Arial", 20))
    textLabel.place(x= 340, y= 20)

    # display the video's thumbnail
    pil_image = ctk.CTkImage(light_image=newVideo.image, dark_image=newVideo.image, size=(320, 180))
    image_label = ctk.CTkLabel(topFrame, image=pil_image, text="")
    image_label.place(x=10, y=20)
    
    # The old comment was here: # the directory specifing
    # We added the code for it above.


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
    except Exception as e: # It's good practice to catch the specific error
        print(f"An error occurred: {e}") # For debugging
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