import random

from PIL import Image,ImageDraw

from kivy.app import App
from kivy.uix.screenmanager import Screen
import math
class PhotoFiltersApp(App):
    pass

class Display(Screen):
    def display_images(self):
        pass
    def load_img(self):
        self.ids.img.source=self.ids.v.text

    def calc_dif(pxla, pxlb, n):
        sum_a = pxla[0] + pxla[1] + pxla[2]
        sum_b = pxlb[0] + pxlb[1] + pxlb[2]
        if abs(sum_a - sum_b) > n:
            return True
        else:
            return False

    def pointillism(self, name):
        image = self.ids.v.text
        img = Image.open(image)
        width,height=img.size
        pixels = img.load()
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        for i in range(50000):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            size = random.randint(3, 5)
            ellipsebox = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
            del draw
        canvas.save(name + " pointillism.jpg")

        self.ids.img.source = name + " pointillism.jpg"

    def line_drawing(self, name,n):
        image = self.ids.v.text
        img = Image.open(image)
        width, height = img.size
        pixel = img.load()
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        pixel_2 = canvas.load()
        for y in range(height - 1):
            for x in range(width - 1):
                if calc_dif(pixel[x, y], pixel[x, y + 1], n) or calc_dif(pixel[x, y], pixel[x - 1, y], n):
                    pixel_2[x, y] = (0, 0, 0)

        canvas.save(name + " line_drawing.jpg")
        self.ids.img.source = name + "line_drawing.jpg"

    line_drawing("lebowski", 50)



PhotoFiltersApp().run()