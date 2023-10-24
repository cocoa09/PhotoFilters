import random
from PIL import Image, ImageDraw
from PIL import Image, ImageChops
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
import math


class PhotoFiltersApp(App):
    pass


class Display(Screen, Widget):
    coordinates = []
    count = 0

    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.coordinates.append(int(x))
        self.coordinates.append(int(y))
        if len(self.coordinates) > 4:
            self.coordinates = self.coordinates[2:]
        touch.push()
        touch.apply_transform_2d(self.to_local)
        ret = super(RelativeLayout, self).on_touch_down(touch)
        touch.pop()
        return ret

    def on_touch_up(self, touch):
        x, y = touch.x, touch.y
        self.coordinates.append(int(x))
        self.coordinates.append(int(y))
        if len(self.coordinates) > 6:
            self.coordinates = self.coordinates[2:]
        touch.push()
        touch.apply_transform_2d(self.to_local)
        ret = super(RelativeLayout, self).on_touch_up(touch)
        touch.pop()
        return ret

    def display_images(self):
        pass

    def load_img(self):
        self.ids.img.source = self.ids.v.text

    def calc_dif(self, pxla, pxlb, n):
        sum_a = pxla[0] + pxla[1] + pxla[2]
        sum_b = pxlb[0] + pxlb[1] + pxlb[2]
        if abs(sum_a - sum_b) > n:
            return True
        else:
            return False

    def pointillism(self):
        image = self.ids.img.source
        img = Image.open(image)
        width, height = img.size
        pixels = img.load()
        img_size=width*height
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        for i in range(width*height//2):
            x = random.randint(0, width - 1)
            y = random.randint(0, height - 1)
            if img_size >= 400000:
                size = random.randint(6, 10)
            else:
                size = random.randint(3,5)
            ellipsebox = [(x, y), (x + size, y + size)]
            draw = ImageDraw.Draw(canvas)
            draw.ellipse(ellipsebox, fill=(pixels[x, y][0], pixels[x, y][1], pixels[x, y][2]))
        del draw
        canvas.save(image + " pointillism.jpg")
        self.ids.img.source = image + " pointillism.jpg"

    def line_drawing(self):
        image = self.ids.img.source
        img = Image.open(image)
        width, height = img.size
        pixel = img.load()
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        pixel_2 = canvas.load()
        for y in range(height - 1):
            for x in range(width - 1):
                if self.calc_dif(pixel[x, y], pixel[x, y + 1], 50) or self.calc_dif(pixel[x, y], pixel[x - 1, y], 50):
                    pixel_2[x, y] = (0, 0, 0)

        canvas.save(image + " line_drawing.jpg")
        self.ids.img.source = image + " line_drawing.jpg"

    def pixelate(self, x, y, width, height, n):
        image = self.ids.v.text
        img = Image.open(image)
        pixels = img.load()
        canvas=img
        wb = width // n
        hb = height // n
        for bx in range(1, n + 1):
            if bx == n:
                x_endbox = x + width
            else:
                x_endbox = x + (wb * bx)
            xstartbox = x + (wb * (bx - 1))
            for by in range(1, n + 1):
                if by == n:
                    y_endbox = y + height
                else:
                    y_endbox = y + (hb * by)
                ystartbox = y + (hb * (by - 1))
                m_pixel = pixels[xstartbox + wb / 2, ystartbox + hb / 2]
                for xx in range(xstartbox, x_endbox):
                    for yy in range(ystartbox, y_endbox):
                        pixels[xx, yy] = (m_pixel)
        canvas.save(image+ " pixelate.jpg")

    def invert(self):
        image = self.ids.img.source
        img = Image.open(image)
        canvas = ImageChops.invert(img)

        canvas.save(image + " inverted.jpg")
        self.ids.img.source = image + " inverted.jpg"

    def sepia(self):
        image = self.ids.img.source
        img = Image.open(image)
        pixels = img.load()
        canvas=img
        for y in range(img.size[1]):
            for x in range(img.size[0]):
                red = pixels[x, y][0]
                green = pixels[x, y][1]
                blue = pixels[x, y][2]
                red = int(red * .393 + green * 0.769 + blue * 0.189)
                green = int(red * .349 + green * 0.686 + blue * 0.168)
                blue = int(red * .272 + green * 0.534 + blue * 0.131)
                pixels[x, y] = (red, green, blue)
        canvas.save(image + " sepia.jpg")
        self.ids.img.source = image + " sepia.jpg"

    def distance_halo(self):
        image = self.ids.img.source
        img = Image.open(image)
        width, height = img.size
        img_size=width*height
        pixels = img.load()
        targetX = width / 2
        targetY = height / 2

        canvas=img
        for y in range(height):
            for x in range(width):
                d = math.sqrt((targetX - x) * (targetX - x) + (targetY - y) * (targetY - y))
                if img_size < 25000:
                    modifier=.5
                elif img_size < 100000:
                    modifier=1
                elif img_size < 400000:
                    modifier=3
                else:
                    modifier=4

                q = d / (modifier)

                if ((pixels[x, y][0] - q) < 0):
                    red = 0
                else:
                    red = int(pixels[x, y][0] - q)

                if ((pixels[x, y][1] - q) < 0):
                    green = 0
                else:
                    green = int(pixels[x, y][1] - q)

                if ((pixels[x, y][2] - q) < 0):
                    blue = 0
                else:
                    blue = int(pixels[x, y][2] - q)

                pixels[x, y] = (red, green, blue)
        canvas.save(image + " halo.jpg")
        self.ids.img.source = image + " halo.jpg"


PhotoFiltersApp().run()
