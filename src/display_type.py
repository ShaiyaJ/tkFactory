import tkinter as tk
from PIL import Image, ImageTk
from os.path import abspath

# from tkrender import UI

class DisplayType(ImageTk.PhotoImage):
    def __init__(self, path: str, scale: int =8):
        # Opening base image
        self.base_image = Image.open(abspath(path))

        # Scaling image based on `scale`
        self.base_image = self.base_image.resize(((8*scale),(8*scale)), Image.Resampling.NEAREST)

        # Producing final image
        ImageTk.PhotoImage.__init__(self, image=self.base_image)

    def rotate(path: str, deg: float =0, scale: int =8) -> ImageTk.PhotoImage:
        # Opening base image
        base_image = Image.open(abspath(path))

        # Scaling image based on `scale`
        base_image = base_image.resize(((8*scale),(8*scale)), Image.Resampling.NEAREST)

        # Rotating image based on `amount`
        base_image = base_image.rotate(deg)

        # Building object
        return ImageTk.PhotoImage(base_image)