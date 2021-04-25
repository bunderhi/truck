import time
from adafruit_magtag.magtag import MagTag

magtag = MagTag()

magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=3,
)
runstate = 'ready'
position = 'center'
magtag.set_text(runstate)

button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
button_tones = (1047, 1318, 1568, 2093)

while True:
    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            print("Button %c pressed" % chr((ord("A") + i)))
            if i == 0:
                if runstate == 'ready':
                    runstate = 'running'
                elif runstate == 'running':
                    runstate = 'ready'
                magtag.set_text(runstate)
            if i == 1:
                if runstate == 'running':
                    position = 'left'
                    magtag.set_text(position)
                else:
                    break
            if i == 2:
                if runstate == 'running':
                    position = 'center'
                    magtag.set_text(position)
                else:
                    break
            if i == 3:
                if runstate == 'running':
                    position = 'right'
                    magtag.set_text(position)
                else:
                    break
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(button_colors[i])
            magtag.peripherals.play_tone(button_tones[i], 0.25)
            break
        else:
            magtag.peripherals.neopixel_disable = True
        time.sleep(0.01)