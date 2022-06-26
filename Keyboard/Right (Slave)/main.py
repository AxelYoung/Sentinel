import keypad
from adafruit_binascii import a2b_base64, b2a_base64
import busio
import board
import rotaryio
import digitalio

class SlaveKeyboard:

    def __init__(self):
        self.uart = busio.UART(board.GP0, board.GP1, baudrate=256000)

        self.matrix = keypad.KeyMatrix(
            row_pins=(board.GP17, board.GP16, board.GP14, board.GP15),
            column_pins=(board.GP18, board.GP19, board.GP20, board.GP21, board.GP22),
        )

        self.button = digitalio.DigitalInOut(board.GP11)
        self.button.direction = digitalio.Direction.INPUT
        self.button.pull = digitalio.Pull.UP
        self.encoder = rotaryio.IncrementalEncoder(board.GP13, board.GP12)

        self.buttonState = False
        self.lastPosition = self.encoder.position
        self.isRunning = True
        keypressVal = 0
        self.keypress = b2a_base64(keypressVal.to_bytes(3, "little", signed=False))
        encoderButtonDownVal = 1
        self.encoderButtonDown = b2a_base64(encoderButtonDownVal.to_bytes(3, "little", signed=False))
        encoderButtonUpVal = 2
        self.encoderButtonUp = b2a_base64(encoderButtonUpVal.to_bytes(3, "little", signed=False))
        encoderDecrementVal = 3
        self.encoderDecrement = b2a_base64(encoderDecrementVal.to_bytes(3, "little", signed=False))
        encoderIncrementVal = 4
        self.encoderIncrement = b2a_base64(encoderIncrementVal.to_bytes(3, "little", signed=False))

    def start(self):
        while self.isRunning:
            event = self.matrix.events.get()
            if event:
                if event.pressed or event.released:
                    self.uart.write(self.keypress)
                    self.uart.write(b2a_base64(event.key_number.to_bytes(3, "little", signed=False)))
            if not self.button.value and self.buttonState is False:
                self.buttonState = True
                self.uart.write(self.encoderButtonDown)
            if self.button.value and self.buttonState == True:
                self.uart.write(self.encoderButtonUp)
                self.buttonState = False
            currentPosition = self.encoder.position
            positionChange = currentPosition - self.lastPosition
            if positionChange > 0:
                for _ in range(positionChange):
                    self.uart.write(self.encoderIncrement)
            elif positionChange < 0:
                for _ in range(-positionChange):
                    self.uart.write(self.encoderDecrement)
            self.lastPosition = currentPosition

# Create the keyboard
keyboard = SlaveKeyboard()

# Start the main loop
keyboard.start()
