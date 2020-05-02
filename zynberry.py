# -*- coding: utf-8 -*-

from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import sh1106

from hardwareInterface import InputEventDispatcher

import time

from PIL import ImageFont

import os

import argparse

from pythonosc import osc_message_builder
from pythonosc import udp_client

eventDispatcher = InputEventDispatcher()

#OSC
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
                    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=6666,
                    help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

#oled I2C
serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

#icon codes
iconCodeLibrary = {
    'folder': u"\uf07c",
    'activeBullet': u"\uf111",
    'inactiveBullet': u"\uf10c"
}

#icon font
def make_font(name, size):
    font_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), name))
    return ImageFont.truetype(font_path, size)

fontAwesome = make_font("fontawesome.ttf", 11)


def render():
    global guiOptions

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")

        #path
        if guiOptions['path']['active']:
            draw.text((5, 10), iconCodeLibrary['activeBullet'], font=fontAwesome, fill="white")
        else:
            draw.text((5, 10), iconCodeLibrary['inactiveBullet'], font=fontAwesome, fill="white")
        draw.text((15, 10), str(guiOptions['path']['options'][guiOptions['path']['selected']]), fill="white")

        #preset
        if guiOptions['preset']['active']:
            draw.text((5, 25), iconCodeLibrary['activeBullet'], font=fontAwesome, fill="white")
        else:
            draw.text((5, 25), iconCodeLibrary['inactiveBullet'], font=fontAwesome, fill="white")
        draw.text((15, 25), str(guiOptions['preset']['options'][guiOptions['preset']['selected']]), fill="white")

        #part
        if guiOptions['part']['active']:
            draw.text((5, 40), iconCodeLibrary['activeBullet'], font=fontAwesome, fill="white")
        else:
            draw.text((5, 40), iconCodeLibrary['inactiveBullet'], font=fontAwesome, fill="white")
        draw.text((15, 40), str(guiOptions['part']['options'][guiOptions['part']['selected']]), fill="white")
        
def setSinth():
    global guiOptions

    partNumber = guiOptions['part']['options'][guiOptions['part']['selected']]
    path = str(guiOptions['path']['options'][guiOptions['path']['selected']])
    preset = str(guiOptions['preset']['options'][guiOptions['preset']['selected']])

    fullPath = BASE_PATH + path +'/'+ preset

    client.send_message("/load-part", [partNumber, fullPath])

BASE_PATH = '/usr/share/zynaddsubfx/banks/'

def loadPaths ():
    bassesPath = BASE_PATH
    return sorted(os.listdir(bassesPath))
    
def loadPresets (path):
    presetsPath = BASE_PATH + path
    return sorted(os.listdir(presetsPath))

guiOptions = {
    'path':{
        'active':True,
        'options':loadPaths(),
        'selected':0
    },
    'preset':{
        'active':False,
        'options':loadPresets(loadPaths()[0]),
        'selected':0
    },
    'part':{
        'active':False,
        'options':[0,1,2,3],
        'selected':0
    }
}


guiOptions['part']['options'][guiOptions['part']['selected']]

optionCounter = 0
def selectOption():
    global optionCounter, guiOptions

    if  optionCounter < len(guiOptions) - 1:
        optionCounter += 1
    else:
        optionCounter = 0
    
    for option in guiOptions:
        guiOptions[option]['active'] = False
    
    guiOptions[list(guiOptions.keys())[optionCounter]]['active'] = True
    
    render()


def changeOption(action):
    global optionCounter, guiOptions
    currentOptionName = list(guiOptions.keys())[optionCounter]
    currentOption = guiOptions[currentOptionName]
    
    if action == 'left':
        currentOption['selected'] -= 1
    
    if action == 'right':
        currentOption['selected'] += 1
    
    if currentOption['selected'] >= len(currentOption['options']):
        currentOption['selected'] = 0
    
    if currentOption['selected'] < 0:
        currentOption['selected'] = len(currentOption['options']) - 1

    if currentOptionName == 'path':
        guiOptions['preset']['options'] = loadPresets(loadPaths()[currentOption['selected']])
        guiOptions['preset']['selected'] = 0
    
    setSinth()
    render()


def rotLeft(tick):
    changeOption('left')

def rotRight(tick):
    changeOption('right')

def rotBtnDown(tick):
    selectOption()

eventDispatcher.onRotLeft += rotLeft
eventDispatcher.onRotRight += rotRight
eventDispatcher.onRotBtnDown += rotBtnDown

setSinth()
render()

try:
    time.sleep(20000000)
except KeyboardInterrupt:  
    print ("keyboard exit")
  
except:  
    print ("Other error or exception occurred!")
  
finally:  
    print ("se terminó")