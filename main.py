import tkinter as tk
import subprocess
from PIL import Image, ImageGrab
from pynput import keyboard
import thumbs
import configparser

class Previewer(tk.Frame):
    def __init__(self, parent, ini):
        super().__init__(parent)
        self.conf = ini['Previewer']
        self.thumb_conf = ini['Thumbnail']

        workspaces = subprocess.check_output(["bspc", "query", "-D", "--names"]).decode('utf-8').split()

        fallback_bg = Image.new('RGB', (1, 1), self.conf['fallback-bg'])

        self.previews = {}
        for w in workspaces:
            # Label holding the image
            self.previews[w] = tk.Label(self)
            self.previews[w].pack(side=self.conf['side'])

            # Generate a thumbnail with a blank screenshot
            thumb = thumbs.generate(fallback_bg, w, self.thumb_conf)

            # Place on the label
            self.previews[w].image = thumb
            self.previews[w].configure(image=thumb)
            
    def update(self, name, image):
        img = thumbs.generate(image, name, self.thumb_conf)
        
        self.previews[name].image = img
        self.previews[name].configure(image=img)

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        ini = configparser.ConfigParser()
        ini.read('config.ini')

        # Config for this widget
        self.conf = ini['BWP']

        self.overrideredirect(True)
        self.geometry(f"+{self.conf['window-x']}+{self.conf['window-y']}")

        self.preview = Previewer(self, ini)
        self.preview.pack(fill=tk.BOTH)

        # Hide window until mod is pressed
        self.withdraw()
        
        # Start updating
        self.update()

    def update(self):
        # Grab desktop number
        workspace = subprocess.check_output(["bspc", "query", "-D", "-d", "focused", "--names"]).decode('utf-8').strip()

        # Grab screenshot
        image = ImageGrab.grab()

        # Update preview
        self.preview.update(workspace, image)

        # Schedule again after a second
        self.after(self.conf['update-interval'], self.update)

    def show(self, key):
        if key == keyboard.Key.cmd:
            self.deiconify()

    def hide(self, key):
        if key == keyboard.Key.cmd:
            self.withdraw()


if __name__ == "__main__":
    a = App()

    listener = keyboard.Listener(on_press=a.show, on_release=a.hide)
    listener.start()

    a.mainloop()
