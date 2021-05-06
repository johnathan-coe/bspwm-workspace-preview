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

        # Falback to use until a screenshot is pulled from a workspace
        fallback_bg = Image.new('RGB', (1, 1), self.conf['fallback-bg'])

        # Get all workspaces
        workspaces = subprocess.check_output(["bspc", "query", "-D", "--names"], encoding='utf-8').split()

        # Create and pack a label for each workspace
        self.previews = {w: tk.Label(self) for w in workspaces}
        [p.pack(side=self.conf['side']) for p in self.previews.values()]
        
        # Put a placeholder in each label
        [self.update(w, fallback_bg) for w in workspaces]

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
        workspace = subprocess.check_output(["bspc", "query", "-D", "-d", "focused", "--names"], encoding='utf-8').strip()

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
