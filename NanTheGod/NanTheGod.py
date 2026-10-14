import pyautogui as pag
import time
import keyboard

pag.FAILSAFE = False
x, y = pag.resolution()


pag.moveTo(x * .09, y * .98, duration=1)
pag.click()
pag.typewrite("Discord", .12)
pag.press("enter")

time.sleep(1)

pag.moveTo(x * .0188, y * .045, duration=1)
pag.click()

time.sleep(.5)

pag.moveTo(x * .1, y * .1, duration=.5)
pag.click()

time.sleep(.5)

pag.moveTo(x * .3, y * .05, duration=.5)
pag.click()

time.sleep(.5)

pag.moveTo(x * .3, y * .11, duration=.5)
pag.click()

time.sleep(.5)

pag.typewrite("nandex", .2)

time.sleep(.2)

pag.moveTo(x * .23, y * .2, duration=.5)
pag.click()

time.sleep(1)

pag.moveTo(x * .23, y * .93, duration=.5)
pag.click()

time.sleep(.5)

pag.typewrite("You are the GOAT", .1)

time.sleep(.2)

pag.press("enter")