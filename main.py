import random
from PIL import Image, ImageDraw
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
import math


class PhotoFiltersApp(App):
    pass


class Display(Screen,Widget):
    coordinates = []
    count = 0
    def on_touch_down(self, touch):
        x, y = touch.x, touch.y
        self.coordinates.append(int(x))
        self.coordinates.append(int(y))
        if len(self.coordinates) > 4:
            self.coordinates=self.coordinates[2:]
        touch.push()
        touch.apply_transform_2d(self.to_local)
        ret = super(RelativeLayout, self).on_touch_down(touch)
        touch.pop()
        return ret

    def on_touch_up(self, touch):
        x, y = touch.x, touch.y
        self.coordinates.append(int(x))
        self.coordinates.append(int(y))
        if len(self.coordinates)>6:
            self.coordinates=self.coordinates[2:]
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
        image = self.ids.v.text
        img = Image.open(image)
        width, height = img.size
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
        canvas.save(image + "pointillism.jpg")
        self.ids.img.source = image + "pointillism.jpg"

    def line_drawing(self):
        image = self.ids.v.text
        img = Image.open(image)
        width, height = img.size
        pixel = img.load()
        canvas = Image.new("RGB", (img.size[0], img.size[1]), "white")
        pixel_2 = canvas.load()
        for y in range(height - 1):
            for x in range(width - 1):
                if self.calc_dif(pixel[x, y], pixel[x, y + 1], 50) or self.calc_dif(pixel[x, y], pixel[x - 1, y], 50):
                    pixel_2[x, y] = (0, 0, 0)
        draw = ImageDraw.Draw(canvas)
        canvas.save(image+"line_drawing.jpg")
        self.ids.img.source = image + "line_drawing.jpg"

    def pixelate(self, name, x, y, width, height, n):
        image = self.ids.v.text
        img = Image.open(image)
        pixels = img.load()
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
        img.save(name + "pixelate.jpg")




PhotoFiltersApp().run()
