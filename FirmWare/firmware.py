import board
import busio
import time

from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners.direct import DirectPins
from kmk.keys import KC, Key
from kmk.extensions.RGB import RGB
from kmk.extensions.OLED import OLED
from kmk.extensions.oled import OledDisplayMode

class LedKey(Key):
    def __init__(self, key, led_index, hue=160, sat=255, val=255):
        self.key = key
        self.led_index = led_index
        self.hue = hue
        self.sat = sat
        self.val = val

    def on_press(self, keyboard, coord_int=None):
        keyboard.add_key(self.key)
        keyboard.rgb.set_hsv(self.hue, self.sat, self.val, self.led_index)
        keyboard.rgb.show()

    def on_release(self, keyboard, coord_int=None):
        keyboard.remove_key(self.key)
        keyboard.rgb.set_hsv(self.hue, self.sat, 0, self.led_index)
        keyboard.rgb.show()

keyboard = KMKKeyboard()

keyboard.matrix = DirectPins(
    pins=(
        board.D7,
        board.D8,
        board.D9,
        board.D10,
        board.D6,
        board.D2,
    ),
    value_when_pressed=False,
)

keyboard.keymap = [
    [
        LedKey(KC.A, 0),
        LedKey(KC.B, 1),
        LedKey(KC.C, 2),
        LedKey(KC.D, 3),
        LedKey(KC.E, 0),
        LedKey(KC.F, 1),
    ]
]

rgb = RGB(
    pixel_pin=board.D3,
    num_pixels=4,
    rgb_order=(1, 0, 2),
    hue_default=0,
    sat_default=255,
    val_default=30,
    val_limit=80,
)
keyboard.extensions.append(rgb)

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

oled = OLED(
    i2c=i2c,
    width=128,
    height=64,
    rotation=0,
    display_mode=OledDisplayMode.TEXT,
)
keyboard.extensions.append(oled)

@oled.draw
def draw(oled, keyboard):
    oled.clear()
    oled.text("RP2040 MACROPAD", 0, 0)
    oled.text("KMK READY", 0, 16)
    oled.show()

if __name__ == "__main__":
    keyboard.go()
