# -*- coding: utf-8 -*-

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

import os

from PIL import ImageFont

class GuiControl:
    
    def __init__(self):

        #oled I2C
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)

        #icon codes
        self.iconCodeLibrary = {
            'folder': u"\uf07c",
            'activeBullet': u"\uf111",
            'inactiveBullet': u"\uf10c"
        }

        #icon font
        def make_font(name, size):
            font_path = os.path.abspath(os.path.join(
                os.path.dirname(__file__), name))
            return ImageFont.truetype(font_path, size)

        self.fontAwesome = make_font("fontawesome.ttf", 11)

    def renderBullet(self, position, viewModel, pilInstance):
        if viewModel:
            pilInstance.text(position, self.iconCodeLibrary['activeBullet'], font=self.fontAwesome, fill="white")
        else:
            pilInstance.text(position, self.iconCodeLibrary['inactiveBullet'], font=self.fontAwesome, fill="white")

    def render(self, viewModel):

        with canvas(self.device) as draw:

            draw.rectangle(self.device.bounding_box, outline="white", fill="black")

            #path
            self.renderBullet((5, 10), viewModel['path']['active'], draw)
            draw.text((15, 10), str(viewModel['path']['options'][viewModel['path']['selected']]), fill="white")

            #preset
            self.renderBullet((5, 25), viewModel['preset']['active'], draw)
            draw.text((15, 25), str(viewModel['preset']['options'][viewModel['preset']['selected']]), fill="white")

            #part
            self.renderBullet((5, 40), viewModel['part']['active'], draw)
            draw.text((15, 40), str(viewModel['part']['options'][viewModel['part']['selected']]), fill="white")