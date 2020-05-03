import guiControl
import hardwareInterface
import zynaddOscControl
import sinthModel

import time

eventDispatcher = hardwareInterface.InputEventDispatcher()
zynaddControl = zynaddOscControl.ZynAddSubFxOscControl()
guiRenderControl = guiControl.GuiControl()
appModel = sinthModel.SinthModel()

def sinthChange(sinthData):
    part = sinthData[0]
    fullPresetPath = sinthData[1]
    zynaddControl.loadPart(part, fullPresetPath)

def guiChange(viewModel):
    guiRenderControl.render(viewModel)

def rotLeft(tick):
    appModel.cpPrevOptActiveConfig()

def rotRight(tick):
    appModel.cpNextOptActiveConfig()

def rotBtnDown(tick):
    appModel.cpNextPartConfig()

def rightUp(tick):
    appModel.pcSelectNextPart()

def leftUp(tick):
    appModel.pcSelectPrevPart()


eventDispatcher.onRotLeft += rotLeft
eventDispatcher.onRotRight += rotRight
eventDispatcher.onRotBtnDown += rotBtnDown
eventDispatcher.onRightUp += rightUp
eventDispatcher.onLeftUp += leftUp

appModel.onChangeView += guiChange
appModel.onChangePreset += sinthChange

guiRenderControl.render(appModel)

try:
    time.sleep(20000000)
except KeyboardInterrupt:  
    print ("keyboard exit")
  
except:  
    print ("Other error or exception occurred!")
  
finally:  
    print ("se terminó")