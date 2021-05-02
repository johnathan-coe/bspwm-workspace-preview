import tkinter as tk
from PIL import ImageGrab, ImageTk
import subprocess

class Previewer(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.previews = {"I": tk.Label(self), "II": tk.Label(self)}

        for i in self.previews:
            self.previews[i].pack()

    def update(self, name, image):
        thumb = image.resize((384, 216))
        
        img = ImageTk.PhotoImage(thumb)
        self.previews[name].image = img
        self.previews[name].configure(image=img)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.preview = Previewer(self)
        self.preview.pack(fill=tk.BOTH)

        self.update()
        self.mainloop()

    def update(self):
        """
        Take a screenshot of the current workspace
        """

        # Grab workspace number
        workspace = subprocess.check_output(["bspc", "query", "-D", "-d", "focused", "--names"]) 
        # Grab screenshot
        image = ImageGrab.grab()
        print(image)
        self.preview.update(workspace.strip().decode('utf-8'), image)

        self.after(1000, self.update)

if __name__ == "__main__":
    App()
