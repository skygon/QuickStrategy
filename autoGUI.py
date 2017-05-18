import pyautogui

# Global settings
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
PAGE = 28  # tdx has 28 stocks in each page.
TOTAL = 3243 # All type A stocks

# Positions maps
posMap = {}
# hotkey maps
hotKey = {}
#hotKey["properties"] = ['winleft', 'altleft', 'p']
#========================Helper functions==================================
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

def menuOperator(direct, times):
    for i in range(times):
        pyautogui.press(direct)

    pyautogui.press('enter')

def pressHotKey(hkey):
    pass
        
#======================End of helper functions=============================

#============Begin position map=================
addPosMap("Detail", 1247, 516)
addPosMap("System", 43, 12)
addPosMap("export", 732, 459)
addPosMap("export_cancel", 828, 426)
#=======End of position map==========================


#========================Test position===================================
w,h = pyautogui.size()
print w, h

cx, cy = pyautogui.position()
print cx, cy

#=========================End of test position============================


#pyautogui.moveTo(0,0,0.1) #This will trige the fail-safe mode and exit the process.

#move to file menu and left click
#click("File", 'right')

#move to some file menu options. This is slow.
#menuOperator('down', 14) # to File -> properties

#pressHotKey("properties")


