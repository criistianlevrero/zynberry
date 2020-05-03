import os

BASE_PATH = '/usr/share/zynaddsubfx/banks/'

class SinthModel:
    def __init__(self):
        self.appModel = {
            'partConfig' : {
                'active':True,
                'partSelector' : {
                    'active':True,
                    'options':[0,1,2,3],
                    'selected':0
                },
                'parts' : self.initializeParts(4)
            }
        }
    
    def initializeParts(self, numberOfPats):
        parts = []
        banks = self.loadBanks()
        ptresets = self.loadPresets(banks[0])
        for x in range(0, numberOfPats):
            parts.append({
                'path':{
                    'active' : True,
                    'options' : banks,
                    'selected' : 0
                },
                'preset':{
                    'active' : False,
                    'options' : ptresets,
                    'selected' : 0
                },
            })
        return(parts)
    
    def loadBanks (self):
        banksPath = BASE_PATH
        return sorted(os.listdir(banksPath))
    
    def loadPresets (self, path):
        presetsPath = BASE_PATH + path
        return sorted(os.listdir(presetsPath))