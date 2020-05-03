# -*- coding: utf-8 -*-

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

import os

from PIL import ImageFont

CONTRAST = 50

class GuiControl:
    
    def __init__(self):

        #oled I2C
        serial = i2c(port=1, address=0x3C)
        self.device = sh1106(serial)
        self.device.contrast(CONTRAST)

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

        partModel = viewModel.pcGetCurrentPartModel()
        partSelectorModel = viewModel.pcGetPartSelectorModel()

        with canvas(self.device) as draw:

            draw.rectangle(self.device.bounding_box, outline="white", fill="black")

            #bank
            self.renderBullet((5, 5), partModel['bank']['active'], draw)
            draw.text((15, 5), str(partModel['bank']['options'][partModel['bank']['selected']]), fill="white")

            #preset
            self.renderBullet((5, 20), partModel['preset']['active'], draw)
            draw.text((15, 20), str(partModel['preset']['options'][partModel['preset']['selected']]), fill="white")

            #part
            draw.text((5, 38), "Parte:" + str(partSelectorModel['selected'] + 1), fill="white")
            pos = 5
            for part in partSelectorModel['options']:
                partBullet = part == partSelectorModel['selected']
                self.renderBullet((pos, 49), partBullet, draw)
                pos += 10