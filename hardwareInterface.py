import pigpio
from events import Events
import time

LEFT = 27
RIGHT = 22
ROTARY_LEFT = 4
ROTARY_RIGHT = 17
ROTARY_BTN = 18

INPUT_PINS =  [LEFT, RIGHT, ROTARY_LEFT, ROTARY_RIGHT, ROTARY_BTN]

class InputEventDispatcher:
    class __InputEventDispatcher(Events):

        __events__ = ('onAny', 'onRotLeft', 'onRotRight', 'onRotBtnDown', 'onRotBtnUp', 'onLeftDown', 'onLeftUp', 'onRightDown', 'onRightUp')

        def __init__(self):
            
            pi = pigpio.pi()
            debounce = 100

            for pin in INPUT_PINS:
                pi.set_mode(pin, pigpio.INPUT)
                pi.set_pull_up_down(pin, pigpio.PUD_DOWN)
                pi.callback(pin, pigpio.EITHER_EDGE, self.allEventsCallback)
                pi.set_glitch_filter(pin, debounce)

            self.rotRightOpen = 0
            self.rotLeftOpen = 0


        def allEventsCallback(self, gpio, level, tick):

            if gpio == ROTARY_LEFT or gpio == ROTARY_RIGHT:
                if gpio == ROTARY_LEFT:
                    self.rotLeftOpen = level
                if gpio == ROTARY_RIGHT:
                    self.rotRightOpen = level
                
                if self.rotLeftOpen == 1 and self.rotRightOpen == 1:
                    if gpio == ROTARY_LEFT:
                        self.onRotLeft(tick)
                        self.onAny(['onRotLeft', gpio, level, tick])
                    if gpio == ROTARY_RIGHT:
                        self.onRotRight(tick)
                        self.onAny(['onRotRight', gpio, level, tick])
            
            if gpio == ROTARY_BTN:
                if level == 1:
                    self.onRotBtnDown(tick)
                    self.onAny(['onRotBtnDown', gpio, level, tick])
                else:
                    self.onRotBtnUp(tick)
                    self.onAny(['onRotBtnUp', gpio, level, tick])
            
            if gpio == LEFT and level == 1:
                self.onLeftDown(tick)
                self.onAny(['onLeftDown', gpio, level, tick])
            
            if gpio == LEFT and level == 0:
                self.onLeftUp(tick)
                self.onAny(['onLeftUp', gpio, level, tick])
            
            if gpio == RIGHT and level == 1:
                    self.onRightDown(tick)
                    self.onAny(['onRightDown', gpio, level, tick])
            
            if gpio == RIGHT and level == 0:
                    self.onRightUp(tick)
                    self.onAny(['onRightUp', gpio, level, tick])

    instance = None
    def __init__(self):
        if not InputEventDispatcher.instance:
            InputEventDispatcher.instance = InputEventDispatcher.__InputEventDispatcher()
    def __getattr__(self, name):
        return getattr(self.instance, name)

