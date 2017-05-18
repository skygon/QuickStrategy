import pyautogui

# Some settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5

#Positions maps
posMap = {}

# Helper functions
def addPosMap(name, x, y):
    posMap[name] = {}
    posMap[name]['x'] = x
    posMap[name]['y'] = y

def moveTo(name, delay = 0.1):
    pyautogui.moveTo(posMap[name]['x'], posMap[name]['y'], delay)

# move to position indicated by name and click on it. default is left click
def click(name, bton = 'left'):
    moveTo(name)
    pyautogui.click(button = bton)
# add postions map
addPosMap("File", 22, 24)



#========================TEST===================================
w,h = pyautogui.size()
print w, h

cx, cy = pyautogui.position()
print cx, cy

#pyautogui.moveTo(0,0,0.1) #This will trige the fail-safe mode and exit the process.

#move to file menu and left click
click("File", 'right')


#pyautogui.dragTo(300,300,1)
