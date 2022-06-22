from asyncio import selector_events
from doctest import master
from glob import glob
from tkinter import *
import keyboard
import os
import json
from ctypes import windll

root = Tk()
root.title("Sentinel Configurator")
root.configure(background='grey')

width = 10
height = 4
keyCount = (width * height) - 2

keymaps = { }

keymap = { 
    'master': { }, 
    'slave': { }
}

conversionArray = [
    (0x00FF, 0x01),
    (0x00FC, 0x02),
    (0x001E, 0x04),
    (0x0030, 0x05),
    (0x002E, 0x06),
    (0x0020, 0x07),
    (0x0012, 0x08),
    (0x0021, 0x09),
    (0x0022, 0x0A),
    (0x0023, 0x0B),
    (0x0017, 0x0C),
    (0x0024, 0x0D),
    (0x0025, 0x0E),
    (0x0026, 0x0F),
    (0x0032, 0x10),
    (0x0031, 0x11),
    (0x0018, 0x12),
    (0x0019, 0x13),
    (0x0010, 0x14),
    (0x0013, 0x15),
    (0x001F, 0x16),
    (0x0014, 0x17),
    (0x0016, 0x18),
    (0x002F, 0x19),
    (0x0011, 0x1A),
    (0x002D, 0x1B),
    (0x0015, 0x1C),
    (0x002C, 0x1D),
    (0x0002, 0x1E),
    (0x0003, 0x1F),
    (0x0004, 0x20),
    (0x0005, 0x21),
    (0x0006, 0x22),
    (0x0007, 0x23),
    (0x0008, 0x24),
    (0x0009, 0x25),
    (0x000A, 0x26),
    (0x000B, 0x27),
    (0x001C, 0x28),
    (0x0001, 0x29),
    (0x000E, 0x2A),
    (0x000F, 0x2B),
    (0x0039, 0x2C),
    (0x000C, 0x2D),
    (0x000D, 0x2E),
    (0x001A, 0x2F),
    (0x001B, 0x30),
    (0x002B, 0x31),
    (0x002B, 0x32),
    (0x0027, 0x33),
    (0x0028, 0x34),
    (0x0029, 0x35),
    (0x0033, 0x36),
    (0x0034, 0x37),
    (0x0035, 0x38),
    (0x003A, 0x39),
    (0x003B, 0x3A),
    (0x003C, 0x3B),
    (0x003D, 0x3C),
    (0x003E, 0x3D),
    (0x003F, 0x3E),
    (0x0040, 0x3F),
    (0x0041, 0x40),
    (0x0042, 0x41),
    (0x0043, 0x42),
    (0x0044, 0x43),
    (0x0057, 0x44),
    (0x0058, 0x45),
    (0xE037, 0x46),
    (0x0046, 0x47),
    (0xE052, 0x49),
    (0xE047, 0x4A),
    (0xE049, 0x4B),
    (0xE053, 0x4C),
    (0xE04F, 0x4D),
    (0xE051, 0x4E),
    (0xE04D, 0x4F),
    (0xE04B, 0x50),
    (0xE050, 0x51),
    (0xE048, 0x52),
    (0x0045, 0x53),
    (0xE035, 0x54),
    (0x0037, 0x55),
    (0x004A, 0x56),
    (0x004E, 0x57),
    (0xE01C, 0x58),
    (0x004F, 0x59),
    (0x0050, 0x5A),
    (0x0051, 0x5B),
    (0x004B, 0x5C),
    (0x004C, 0x5D),
    (0x004D, 0x5E),
    (0x0047, 0x5F),
    (0x0048, 0x60),
    (0x0049, 0x61),
    (0x0052, 0x62),
    (0x0053, 0x63),
    (0x0056, 0x64),
    (0xE05D, 0x65),
    (0x0059, 0x67),
    (0x005D, 0x68),
    (0x005E, 0x69),
    (0x005F, 0x6A),
    (0x007E, 0x85),
    (0x0073, 0x87),
    (0x0070, 0x88),
    (0x007D, 0x89),
    (0x0079, 0x8A),
    (0x007B, 0x8B),
    (0x005C, 0x8C),
    (0x00F2, 0x90),
    (0x00F1, 0x91),
    (0x0078, 0x92),
    (0x0077, 0x93),
    (0x0076, 0x94),
    (0x001D, 0xE0),
    (0x002A, 0xE1),
    (0x0038, 0xE2),
    (0xE05B, 0xE3),
    (0xE01D, 0xE4),
    (0x0036, 0xE5),
    (0xE038, 0xE6),
    (0xE05C, 0xE7)
]

conversionMap = {}

defaultKeymap = 'Default'

masterButtons = []
slaveButtons = []

for conversion in conversionArray:
    conversionMap[str(conversion[0])] = conversion[1]

def CreateNewKeymap(name):
    for index in range(int(keyCount / 2)):
        keymap['master'][str(index)] = {} 
        keymap['slave'][str(index)] = {} 
        keymap['master'][str(index)]['name'] = ""
        keymap['slave'][str(index)]['name'] = ""
        
        keymaps[name] = keymap

if os.path.exists("keymap.json") == False:
    CreateNewKeymap(defaultKeymap)  
    with open("keymap.json", "x") as jsonFile:
        json.dump(keymaps, jsonFile)
else:
    with open("keymap.json") as jsonFile:
        keymaps = json.load(jsonFile)

def ChangeMasterKey(index, layer):
    if selectedLayer == '':
        input = keyboard.read_key()
        hexKey = conversionMap[str(keyboard.key_to_scan_codes(input)[0])]
        masterButtons[index].configure(text=input)
        keymaps[layer]['master'][str(index)]['name'] = input
        keymaps[layer]['master'][str(index)]['id'] = hexKey
        keymaps[layer]['master'][str(index)].pop('layer')
    else:
        masterButtons[index].configure(text=selectedLayer)
        keymaps[layer]['master'][str(index)]['name'] = selectedLayer
        keymaps[layer]['master'][str(index)]['layer'] = selectedLayer
        keymaps[layer]['master'][str(index)].pop('id')
        CreateLayerKey(selectedLayer)

def ChangeSlaveKey(index, layer):
    if selectedLayer == '':
        input = keyboard.read_key()
        hexKey = conversionMap[str(keyboard.key_to_scan_codes(input)[0])]
        slaveButtons[index].configure(text=input)
        keymaps[layer]['slave'][str(index)]['name'] = input
        keymaps[layer]['slave'][str(index)]['id'] = hexKey
        keymaps[layer]['slave'][str(index)].pop('layer')
    else:
        slaveButtons[index].configure(text=selectedLayer)
        keymaps[layer]['slave'][str(index)]['name'] = selectedLayer
        keymaps[layer]['slave'][str(index)]['layer'] = selectedLayer
        keymaps[layer]['slave'][str(index)].pop('id')
        CreateLayerKey(selectedLayer)

def SaveKeymap():
    with open('keymap.json', "w") as jsonFile:
        json.dump(keymaps, jsonFile)

def NewLayer():
    CreateNewKeymap(newLayerName.get())
    for button in layerButtons:
        button.destroy()
    layerButtons.clear()
    GenerateLayerButtons()

def GenerateKeyButtons(layer):

    masterIndex = -1
    slaveIndex = -1

    for button in slaveButtons:
        button.destroy()
    for button in masterButtons:
        button.destroy()
    slaveButtons.clear()
    masterButtons.clear()

    for y in range(0, height):
        for x in range(0, width):
            if (x != 4 or y != 3) and (x != 5 or y != 3):
                if x <= 4:
                    masterIndex += 1 
                    masterButtons.append(Button(root, text=keymaps[layer]['master'][str(masterIndex)]['name'], command=lambda a=masterIndex, b=layer: ChangeMasterKey(a, b), padx=20, pady=20))
                    masterButtons[masterIndex].grid(row=y, column=x, padx=10, pady=10)
                else:
                    slaveIndex += 1
                    slaveButtons.append(Button(root, text=keymaps[layer]['slave'][str(slaveIndex)]['name'], command=lambda a=slaveIndex, b=layer: ChangeSlaveKey(a, b), padx=20, pady=20))   
                    slaveButtons[slaveIndex].grid(row=y, column=x, padx=10, pady=10)

GenerateKeyButtons(defaultKeymap)

def GenerateSaveButton():
    saveButton = Button(root, text="Save Keymap", command=SaveKeymap, padx=20, pady=20)
    saveButton.grid(row=4, column=4, padx=10, pady=10, columnspan=2)

def DeleteLayer(layer):
    del keymaps[layer]
    GenerateLayerButtons()
    GenerateKeyButtons(defaultKeymap)

GenerateSaveButton()

layerButtons = []

newLayerName = Entry()

selectedLayer = ''

selectedLayerButtons = {}

def CreateLayerKey(layer):
    global selectedLayer
    if selectedLayer != layer:
        selectedLayer = layer
        selectedLayerButtons[layer].configure(bg="blue")
    else:
        selectedLayer = ''
        selectedLayerButtons[layer].configure(bg="white")

def GenerateLayerButtons():

    for button in layerButtons:
        button.destroy()
    layerButtons.clear()
    selectedLayerButtons.clear()

    for i in range(len(keymaps)):
        layer = Button(root, text=list(keymaps.keys())[i], padx=20, pady=20, command=lambda x=list(keymaps.keys())[i]: GenerateKeyButtons(x))
        layer.grid(row=5, column=i, padx=10, pady=10)
        layerButtons.append(layer)
        if i > 0:
            createLayerKey = Button(root, text="Create Layer Key", command=lambda a=list(keymaps.keys())[i]: CreateLayerKey(a), padx=20, pady=20)
            createLayerKey.grid(row=6, column=i, padx=10, pady=10)
            selectedLayerButtons[list(keymaps.keys())[i]] = createLayerKey
            layerButtons.append(createLayerKey)
            delete = Button(root, text="Delete Layer", padx=20, pady=10, command=lambda x=list(keymaps.keys())[i]: DeleteLayer(x))
            delete.grid(row=7, column=i, padx=10, pady=5)
            layerButtons.append(delete)

    newLayerButton = Button(root, text="New Layer", command=NewLayer, padx=20, pady=20)
    newLayerButton.grid(row=5, column=len(keymaps), padx=10, pady=10)
    layerButtons.append(newLayerButton)
    global newLayerName
    newLayerName = Entry(root)
    newLayerName.grid(row=6, column=len(keymaps), padx=10, pady=10)
    layerButtons.append(newLayerName)

GenerateLayerButtons()

root.mainloop()