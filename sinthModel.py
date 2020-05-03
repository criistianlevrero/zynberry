import os
from events import Events

BASE_PATH = '/usr/share/zynaddsubfx/banks/'
PARTS_NUMBER = 4

class SinthModel(Events):

    __events__ = ('onChangeView', 'onChangePreset', 'onLoadProgram')

    def __init__(self):
        self.appModel = {
            'partConfig' : {
                'active' : True,
                'view' : 'partConfig',
                'partSelector' : {
                    'options' : [x for x in range(PARTS_NUMBER)],
                    'selected' : 0
                },
                'parts' : self.__initializeParts(PARTS_NUMBER)
            },
            'programSelector' : {
                'active' : False,
                'view' : 'programSelector'
            }
        }
    
    def __initializeParts(self, numberOfPats):
        parts = []
        banks = self.__loadBanks()
        ptresets = self.__loadPresets(banks[0])
        for x in range(0, numberOfPats):
            parts.append({
                'bank':{
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
    
    def __loadBanks (self):
        banksPath = BASE_PATH
        return sorted(os.listdir(banksPath))
    
    def __loadPresets (self, path):
        presetsPath = BASE_PATH + path
        presetsList = sorted(os.listdir(presetsPath))
        filteredPresets = [x for x in presetsList if not x.startswith('.')]
        return (filteredPresets)
    
    def getCurrentViewModel(self):
        for model in self.appModel:
            if self.appModel[model]['active']:
                return self.appModel[model]
    
    #PartConfig Model controller
    def __pcGetPartsModel(self):
        return self.appModel['partConfig']

    def pcGetPartSelectorModel(self):
        return self.appModel['partConfig']['partSelector']

    def pcSelectNextPart(self):
        return self.__pcSelectPrevNextPart(1)

    def pcSelectPrevPart(self):
        return self.__pcSelectPrevNextPart(-1)
    
    def __pcSelectPrevNextPart(self, positions):
        selector = self.pcGetPartSelectorModel()
        current = selector['selected']
        listLenght = len(selector['options'])
        selector['selected'] = (current + positions) % listLenght
        self.onChangeView(self)
        return current
    
    def pcGetCurrentPartModel(self):
        current = self.pcGetPartSelectorModel()['selected']
        return self.appModel['partConfig']['parts'][current]
    
    def __pcGetCurrentBank(self):
        currentBankOptions = self.pcGetCurrentPartModel()['bank']['options']
        currentBankSelected = self.pcGetCurrentPartModel()['bank']['selected']
        return currentBankOptions[currentBankSelected]
    
    def __pcGetCurrentPreset(self):
        currentPresetOptions = self.pcGetCurrentPartModel()['preset']['options']
        currentPresetSelected = self.pcGetCurrentPartModel()['preset']['selected']
        return currentPresetOptions[currentPresetSelected]

    def __pcBankPresetNextPrev(self, bankPreset, positions):
        currentBankPreset = self.pcGetCurrentPartModel()
        current = currentBankPreset[bankPreset]
        listLenght = len(current['options'])
        current['selected'] = (current['selected'] + positions) % listLenght
        self.__cpReloadPresetList()
        self.__cpProgramChangedEvent()
        self.onChangeView(self)
        return current['selected']
    
    def __cpReloadPresetList(self):
        bank = self.__pcGetCurrentBank()
        self.pcGetCurrentPartModel()['preset']['options'] = self.__loadPresets(bank)

    def cpBankPrev(self):
        return self.__pcBankPresetNextPrev('bank', -1)
    
    def cpBankNext(self):
        return self.__pcBankPresetNextPrev('bank', 1)
    
    def cpPresetPrev(self):
        self.__cpProgramChangedEvent()
        return self.__pcBankPresetNextPrev('preset', -1)
    
    def cpPresetNext(self):
        self.__cpProgramChangedEvent()
        return self.__pcBankPresetNextPrev('preset', 1)

    def __cpProgramChangedEvent(self):
        currentPart = self.pcGetPartSelectorModel()['selected']
        currentBank = self.__pcGetCurrentBank()
        currentPreset = self.__pcGetCurrentPreset()
        presetFullPath = BASE_PATH + currentBank + '/' + currentPreset
        self.onChangePreset((currentPart, presetFullPath))
    
    def cpNextPartConfig(self):
        partModel = self.pcGetCurrentPartModel()
        for partConfig in partModel:
            partModel[partConfig]['active'] = partModel[partConfig]['active'] != True
        self.onChangeView(self)
    
    def __getActivePartConfig(self):
        partModel = self.pcGetCurrentPartModel()
        for partConfig in partModel:
            if partModel[partConfig]['active']:
                return partConfig

    def cpNextOptActiveConfig(self):
        activePart = self.__getActivePartConfig()
        if activePart == 'bank':
            self.cpBankNext()
        if activePart == 'preset':
            self.cpPresetNext()
    
    def cpPrevOptActiveConfig(self):
        activePart = self.__getActivePartConfig()
        if activePart == 'bank':
            self.cpBankPrev()
        if activePart == 'preset':
            self.cpPresetPrev()