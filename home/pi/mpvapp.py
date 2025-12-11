from gpiozero import Button
from signal import pause
import mpv

# Installing python-mpv on Raspberry Pi:
#   sudo apt install python3-mpv

# Overridde Button class
class MyButton(Button):
    def __init__(self, pin, **kwargs):
        super().__init__(pin, **kwargs)
        self._was_held = False
        self.when_held = self._on_held
        self.when_released = self._on_released
    
    def _on_held(self):
        self._was_held = True

    def _on_released(self):
        if not self._was_held:
            self.on_short_press()
        else:
            self.on_long_press()
        self._was_held = False  # Reset for next press

    def on_short_press(self):
        pass  # To be overridden

    def on_long_press(self):
        pass  # To be overridden

###############################################################
# Configuration Section
###############################################################
# Define GPIO pins for buttons (not physical pin numbers)
FWD_BUTTON_PIN = 20
REV_BUTTON_PIN = 21

# Define long press hold time in seconds
LONG_PRESS_TIME_IN_SEC = 1.5
BOUNCE_TIME_IN_SEC = 0.05

###############################################################
# Player and Event Handlers
###############################################################
def log_messages(loglevel, component, message):
    print(f"[{component}] {message}")

player = mpv.MPV(config=True,
                 log_handler=log_messages, 
                 loglevel='debug')

# Handler functions for button presses. Modify as needed.
def fwd_short_press():
    print("FWD Short press detected")

def fwd_long_press():
    print("FWD Long press detected")
    player.command('playlist-next')

def rev_short_press():
    print("REV Short press detected")

def rev_long_press():
    print("REV Long press detected")
    player.command('playlist-prev')

###############################################################
# Main Program
###############################################################
# Create the buttons
fwd_button = MyButton(FWD_BUTTON_PIN, bounce_time=BOUNCE_TIME_IN_SEC, hold_time=LONG_PRESS_TIME_IN_SEC)
rev_button = MyButton(REV_BUTTON_PIN, bounce_time=BOUNCE_TIME_IN_SEC, hold_time=LONG_PRESS_TIME_IN_SEC)
fwd_button.on_long_press = fwd_long_press
rev_button.on_long_press = rev_long_press
fwd_button.on_short_press = fwd_short_press
rev_button.on_short_press = rev_short_press

# Start mpv
print("Playing videos from ~/simpsonstv")
player.play('~/simpsons')

print("pausing for button presses...")
pause()
