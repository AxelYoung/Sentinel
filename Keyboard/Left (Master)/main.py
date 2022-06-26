import keypad
import time
import board
import rotaryio
import usb_hid
import busio
import digitalio
import json

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_binascii import a2b_base64, b2a_base64
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

keyboard = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)

defaultLayer = "Default"

matrix = keypad.KeyMatrix(
    row_pins=(board.GP7, board.GP8, board.GP9, board.GP10),
    column_pins=(board.GP11, board.GP12, board.GP13, board.GP14, board.GP15),
    columns_to_anodes=True,
)

with open('keymap.json') as jsonFile:
    keymaps = json.load(jsonFile)
    masterKeymap = keymaps[defaultLayer]['master']
    slaveKeymap = keymaps[defaultLayer]['slave']

masterStates = [False] * 20
slaveStates = [False] * 20

pressedKeys = []
releasedKeys = []

uart = busio.UART(board.GP0, board.GP1, baudrate=256000)


button = digitalio.DigitalInOut(board.GP16)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
encoder = rotaryio.IncrementalEncoder(board.GP18, board.GP17)

def SetLayer(layer):
    global masterKeymap
    global slaveKeymap
    masterKeymap = keymaps[layer]['master']
    slaveKeymap = keymaps[layer]['slave']

def PressKey(key):
    if "id" in key:
        #pressedKeys.append(key['id'])
        keyboard.press(key['id'])
    elif "layer" in key:
        SetLayer(key['layer'])

def ReleaseKey(key):
    if "id" in key:
        #releasedKeys.append(key['id'])
        keyboard.release(key['id'])
    elif "layer" in key:
        SetLayer(defaultLayer)

'''
def ProcessKeys():
    for key in pressedKeys:
        keyboard.press(key)
        pressedKeys.pop(pressedKeys.index(key))
    for key in releasedKeys:
        keyboard.release(key)
        releasedKeys.pop(releasedKeys.index(key))
'''

buttonState = False
lastPosition = encoder.position

while True:
    event = matrix.events.get()
    if event:
        if event.pressed:
            keyPressed = masterKeymap[str(event.key_number)]
            PressKey(keyPressed)
        if event.released:
            keyReleased = masterKeymap[str(event.key_number)]
            ReleaseKey(keyReleased)
    dataCount = uart.in_waiting
    if dataCount > 0:
        dataTypeRaw = uart.readline()
        dataType = int.from_bytes(a2b_base64(dataTypeRaw), "little")
        if dataType == 0:
            data = uart.readline()
            index = int.from_bytes(a2b_base64(data), "little")
            if index > 14:
                index -= 1
            if slaveStates[index] is False:
                keyPressed = slaveKeymap[str(index)]
                PressKey(keyPressed)
            else:
                keyReleased = slaveKeymap[str(index)]
                ReleaseKey(keyReleased)
            slaveStates[index] = not slaveStates[index]
        elif dataType == 1:
            cc.send(ConsumerControlCode.MUTE)
        elif dataType == 2:
            cc.send(ConsumerControlCode.MUTE)
        elif dataType == 3:
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
        elif dataType == 4:
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)

    currentPosition = encoder.position
    positionChange = currentPosition - lastPosition
    if positionChange > 0:
        for _ in range(positionChange):
            cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif positionChange < 0:
        for _ in range(-positionChange):
            cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    lastPosition = currentPosition
    if not button.value and buttonState is False:
        buttonState = True
    if button.value and buttonState == True:
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        buttonState = False
