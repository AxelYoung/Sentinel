import keypad
from adafruit_binascii import a2b_base64, b2a_base64
import busio
import board

class SlaveKeyboard:

    def __init__(self):
        self.uart = busio.UART(board.GP0, board.GP1, baudrate=256000)

        self.matrix = keypad.KeyMatrix(
            row_pins=(board.GP17, board.GP16, board.GP14, board.GP15),
            column_pins=(board.GP18, board.GP19, board.GP20, board.GP21, board.GP22),
        )

        self.isRunning = True

    def start(self):
        while self.isRunning:
            event = self.matrix.events.get()
            if event:
                if event.pressed or event.released:
                    self.uart.write(b2a_base64(event.key_number.to_bytes(3, "little", signed=False)))

# Create the keyboard
keyboard = SlaveKeyboard()

# Start the main loop
keyboard.start()
