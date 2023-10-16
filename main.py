import random

from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from kivy.app import App
from kivy.uix.screenmanager import Screen
import math
class PhotoFiltersApp(App):
    pass

class Display(Screen):
    def display_images(self):


    def pointillism(self,name):
        image = Image.open(name)
        width, height = image.size
        pixels = image.load()
        canvas = Image.new("RGB", (image.size[0], image.size[1]), "white")
        for i in range(50000):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            size = random.randint(3, 5)
            ellipsebox = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
            del draw
        canvas.save(name + " pointillism.jpg")
        cat_name = name + " pointillism.jpg"

        self.ids.image.source= cat_name



PhotoFiltersApp().run()