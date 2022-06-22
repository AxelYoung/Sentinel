import keypad
import time
import board
import usb_hid
import busio
import digitalio
import json

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_binascii import a2b_base64, b2a_base64

keyboard = Keyboard(usb_hid.devices)

defaultKeymap = "Default"

matrix = keypad.KeyMatrix(
    row_pins=(board.GP7, board.GP8, board.GP9, board.GP10),
    column_pins=(board.GP11, board.GP12, board.GP13, board.GP14, board.GP15),
    columns_to_anodes=True,
)

with open('keymap.json') as jsonFile:
    keymaps = json.load(jsonFile)
    masterKeymap = keymaps[defaultKeymap]['master']
    slaveKeymap = keymaps[defaultKeymap]['slave']

masterStates = [False] * 20
slaveStates = [False] * 20

uart = busio.UART(board.GP0, board.GP1, baudrate=256000)

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    event = matrix.events.get()
    if event:
        if event.pressed:
            if "id" in masterKeymap[str(event.key_number)]:
                keyboard.press(masterKeymap[str(event.key_number)]['id'])
            elif "layer" in masterKeymap[str(event.key_number)]:
                masterKeymap = keymaps[masterKeymap[str(event.key_number)]['layer']]['master']
                slaveKeymap = keymaps[masterKeymap[str(event.key_number)]['layer']]['slave']
        if event.released:
            if "id" in masterKeymap[str(event.key_number)]:
                keyboard.release(masterKeymap[str(event.key_number)]['id'])
            elif "layer" in masterKeymap[str(event.key_number)]:
                masterKeymap = keymaps[defaultKeymap]['master']
                slaveKeymap = keymaps[defaultKeymap]['slave']
    dataCount = uart.in_waiting
    if dataCount > 0:
        data = uart.readline()
        index = int.from_bytes(a2b_base64(data), "little")
        if index > 14:
            index -= 1
        if slaveStates[index] is False:
            if "id" in slaveKeymap[str(index)]:
                keyboard.press(slaveKeymap[str(index)]['id'])
            elif "layer" in slaveKeymap[str(index)]:
                masterKeymap = keymaps[slaveKeymap[str(index)]['layer']]['master']
                slaveKeymap = keymaps[slaveKeymap[str(index)]['layer']]['slave']
        else:
            if "id" in slaveKeymap[str(index)]:
                keyboard.release(slaveKeymap[str(index)]['id'])
            elif "layer" in slaveKeymap[str(index)]:
                masterKeymap = keymaps[defaultKeymap]['master']
                slaveKeymap = keymaps[defaultKeymap]['slave']
        slaveStates[index] = not slaveStates[index]
