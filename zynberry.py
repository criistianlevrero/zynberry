import guiControl
import hardwareInterface
import zynaddOscControl

import os

import time

BASE_PATH = '/usr/share/zynaddsubfx/banks/'

eventDispatcher = hardwareInterface.InputEventDispatcher()
zynaddControl = zynaddOscControl.ZynAddSubFxOscControl()
guiRenderControl = guiControl.GuiControl()


def setSinth():
    global guiOptions

    partNumber = guiOptions['part']['options'][guiOptions['part']['selected']]
    path = str(guiOptions['path']['options'][guiOptions['path']['selected']])
    preset = str(guiOptions['preset']['options'][guiOptions['preset']['selected']])

    fullPath = BASE_PATH + path +'/'+ preset

    zynaddControl.loadPart(partNumber, fullPath)


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
    
    guiRenderControl.render(guiOptions)


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
    guiRenderControl.render(guiOptions)


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
guiRenderControl.render(guiOptions)

try:
    time.sleep(20000000)
except KeyboardInterrupt:  
    print ("keyboard exit")
  
except:  
    print ("Other error or exception occurred!")
  
finally:  
    print ("se terminó")