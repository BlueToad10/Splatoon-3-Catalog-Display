import os, sys, random, pickle, pygame, tkinter
from pygame.locals import *
from tkinter import *
from tkinter.font import BOLD, Font
from PIL import Image
version = "1.4.2"
Title = f"Splatoon Progress Display {version}"
currentDirectory = os.getcwd()
assetsPath = rf"{currentDirectory}\assets"
pickleLand = rf"{assetsPath}\pickle"
imageDirectory = rf"{assetsPath}\images"
mainImagePath = rf"{imageDirectory}\main"

def terminate(): pygame.quit(); sys.exit()
def percentage(part=1, whole=1): return(int(100 * float(part)/float(whole)))#except: return 0
def load(fileName=""): return pickle.load(open(fileName, "rb"))
def pickleVar(baseDefinition, varName, rePickleBool=False):
    """Does a "try" statement, to load variable from a pickled file. or sets the base definition of the variable, pickling to file, and returning the definition"""
    try: var = load(rf"{pickleLand}\{varName}.pkl")
    except:
        var = baseDefinition
        with open(rf"{pickleLand}\{varName}.pkl", "wb") as p: pickle.dump(var, file=p)
    if rePickleBool == True:
        with open(rf"{pickleLand}\{varName}.pkl", "wb") as p: pickle.dump(var, file=p)
    return var
def dirList(path=""): 
    '''Loads all path objects from directory path'''
    newList = []
    for object in sorted(os.listdir(path), key=len):
        newList.append(rf"{path}\{object}")
    return newList
def removeCharactersList(string, StringList):
    for object in StringList:
        string = string.replace(object,"")
    return string

imagesDirectoryList = dirList(path=mainImagePath)
mainFontPath = rf"{assetsPath}\paintball_beta_2.ttf"
roundsFile = rf"{assetsPath}\rounds.txt"#For saving and loading
settingsList = []
with open(rf"{assetsPath}\settings.txt", "r") as f:
    for line in f:
        settingsList.append(line)
colorInvalidCharacters = ["(", ")", "\n"]

'''Multiplier value for different times 0-2                       list verion,            setting to 1x as default,          multiplierInt: id for setting the multiplier later on'''
regular, splatfest, closeout = 1, 1.2, 1.5; multipliers = [regular, splatfest, closeout]; multiplierInt = 0
multiplier = pickleVar(multipliers[0], "multiplier")
'''[CurrentLevel]: Used to track how many more levels till the max level, this variable is set by things that come after assigning it here. So anything is fine for this. But an example to make it easy is "100-77" or "MaxLevel-CurrentLevel".'''
'''[MaxLevels]: Varies from game to game, this will be 50 in splatoon 1, and 100 in splatoon 2 & 3. Set default here, and will be updated by settings file later.'''
'''[PointsForLevel]: Sets the points needed to level up. For use in simulating future rounds to guess counterObject. 9500 by default, may vary by game in the series.'''
CurrentLevel = pickleVar(78, "CurrentLevel")
maxLevels = 100; pointsForLevel = 9500
'''Setting values for round resaults #Defeat points, also used as disconnect points, always 0.'''
defeatP = 0; winP = 1700; loseP = 500; KOP = 2500; firstWinPoints = 7500
'''WinConditions for checking first win of the day when simulating future rounds.'''
WinConditions = ["winPoints", "knockoutPoints"]
WinConditionCodes = ["W", "KO"]
'''Max rounds for storing round objects. Lists for Rank options. And regularLevel Max and current'''
RankCounter = pickleVar(8, "rankCounter")
Ranks = ["C-", "C", "C+",    "B-", "B", "B+",    "A-", "A", "A+",    "S-", "S", "S+"]
'''Ranks in string form for DrawText display'''
regularLevelMax = 100
currentRegularLevel = pickleVar(77, "currentRegularLevel")
maxRounds = 300
'''loading any adjustments from Settings file.'''
for object in settingsList:
    splitline = object.split(" ")
    try:
        if object.startswith("defeatP "):            defeatP = int(splitline[1])
        if object.startswith("winP "):               winP = int(splitline[1])
        if object.startswith("loseP "):              loseP = int(splitline[1])
        if object.startswith("KOP "):                KOP = int(splitline[1])
        if object.startswith("pointsForLevel "):     pointsForLevel = int(splitline[1])
        if object.startswith("maxLevels "):          maxLevels = int(splitline[1])
        if object.startswith("CurrentLevel "):       CurrentLevel = int(splitline[1])

        if object.startswith("currentRegularLevel "): currentRegularLevel = int(splitline[1])
        if object.startswith("regularLevelMax "):     regularLevelMax = int(splitline[1])
        if object.startswith("maxRounds "):           maxRounds = int(splitline[1])

        if object.startswith("Ranks "):               Ranks = object.replace("Ranks ", "").split(" ")
        if object.startswith("WinConditions "):       WinConditions = object.replace("WinConditions ", "").split(" ")
        if object.startswith("WinConditionCodes "):   WinConditionCodes = object.replace("WinConditions ", "").split(" ")
    except: print("Error when setting points from Settings file.")

levelsNeeded = maxLevels-CurrentLevel
i = 0
for object in multipliers:
    if multiplier == object: multiplierInt = i
    i+=1

baseChance = pickleVar(False, "baseChance")
hundredLimit = pickleVar(True, "hundredLimit")
currentWeapon = pickleVar("", "currentWeapon")
currentSubWeapon = pickleVar("", "currentSubWeapon")
currentSpecial = pickleVar("", "currentSpecial")

WINDOWSIZEX, WINDOWSIZEY = 498+40, 606+40+30
WINDOWSIZE =   (WINDOWSIZEX, WINDOWSIZEY)
extraX, extraY = 20, 20
FPS = 60

MainWindow = tkinter.Tk(className=Title)##### for new window ↓ ↓ ↓ ↓
img = tkinter.PhotoImage(file=rf"{assetsPath}\S3CD.ico")
MainWindow.iconphoto(False, img)
'''Main TKinter Window'''
MainWindow.geometry(str(WINDOWSIZEX*2) + "x" + str(WINDOWSIZEY))
MainWindow['background']='#262626'
'''Pygame Embed portion'''
embed = tkinter.Frame(MainWindow, width = WINDOWSIZEX+1, height = WINDOWSIZEY+1)
embed.place(x = 0) #packs window to the left
embed['background']='#000000'
'''Button portion'''
buttonwin = tkinter.Frame(MainWindow, width = WINDOWSIZEX, height = WINDOWSIZEY)
buttonwin.place(x = WINDOWSIZEX)
buttonwin['background']='#262626'
'''Connecting Pygame to Embed'''
os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
os.environ['SDL_VIDEODRIVER'] = 'windib'

'''Setting up PyGame basics'''
WindowSurface = pygame.display.set_mode(WINDOWSIZE)
pygame.init()
pygame.mixer.init()
MainWindow.update()
WindowSurface = pygame.display.set_mode(WINDOWSIZE)
LEFT = 1; RIGHT = 3
mainClock = pygame.time.Clock()
mainFont = pygame.font.Font(mainFontPath, 49)
fontSizes = {49: mainFont}

greenRect = (44+extraX, 172+extraY, 268, 50)
pinkRect  = (327+extraX, 172+extraY, 119, 50)
boRect    = (160+extraX, 230+extraY, 254, 46)
levelRect = (45+extraX, 56+extraY, 162, 50)
rankRect  = (222+extraX, 56+extraY, 228, 50)
surfaceSettingsNamesList = ["greenRect", "pinkRect", "boRect", "levelRect", "rankRect"]
for object in settingsList:
    if object.startswith("surface:"):
        splitObject = object.split(":")[1].replace("\n","").split(" ")
        listObject = (int(splitObject[1])+extraX, int(splitObject[2])+extraY, int(splitObject[3]), int(splitObject[4]))
        if splitObject[0] == "greenRect": greenRect = listObject
        if splitObject[0] == "pinkRect":  pinkRect  = listObject
        if splitObject[0] == "boRect":    boRect    = listObject
        if splitObject[0] == "levelRect": levelRect = listObject
        if splitObject[0] == "rankRect":  rankRect  = listObject

GreenSurface = WindowSurface.subsurface(greenRect)
PinkSurface  = WindowSurface.subsurface(pinkRect)
BOSurface    = WindowSurface.subsurface(boRect)
LevelSurface = WindowSurface.subsurface(levelRect)
RankSurface  = WindowSurface.subsurface(rankRect)

backgroundColor =  0,177,64#0, 71, 187
greenBackgroundColor = 90,255,90
pinkBackgroundColor = 191,0,255
levelBackgroundColor = 66,237,56
rankBackgroundColor = 255,118,0
for object in settingsList:# f.write to create base file
    settingsObject = object
    try:
        if "background" in object.lower():
            splitline = removeCharactersList(object, colorInvalidCharacters).split(" ")[1]
            splitline = splitline.split(",")
            i=0
            for object in splitline:
                splitline[i] = int(object); i+=1
            if len(splitline) == 4: colorSplitline = splitline[0], splitline[1], splitline[2], splitline[3]
            else: colorSplitline = splitline[0], splitline[1], splitline[2]
            if settingsObject.startswith("backgroundColor "): backgroundColor      = colorSplitline
            if settingsObject.startswith("greenbackground "): greenBackgroundColor = colorSplitline
            if settingsObject.startswith("pinkbackground "):  pinkBackgroundColor  = colorSplitline
            if settingsObject.startswith("levelbackground "): levelBackgroundColor = colorSplitline
            if settingsObject.startswith("rankbackground "):  rankBackgroundColor  = colorSplitline
    except: pass

def drawText(text, textcolour, surface, x, y, Mx=WINDOWSIZEX, My=WINDOWSIZEY, centerBool=True, centerCords=None, fontSize = 49):
    if fontSize == 49: font = mainFont
    elif fontSize in fontSizes: font = fontSizes[fontSize]
    else:
        font = pygame.font.Font(mainFontPath, fontSize)
        fontSizes[fontSize] = font
    words = [word.split('. ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = (Mx, My)
    y = y
    pos = x, y
    for line in words:
        for word in line:
            word_surface = font.render(word, True, textcolour)
            word_shadow = font.render(word, True, (0,0,0))
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            if centerBool == True: text_rect = word_surface.get_rect(center=(x+word_width//2,y+word_height//2))
            else: text_rect = (x,y)
            if not centerCords == None: text_rect = word_surface.get_rect(center=centerCords)
            surface.blit(word_shadow, (text_rect[0]+1,text_rect[1]+1))
            surface.blit(word_shadow, (text_rect[0]+2,text_rect[1]+2))
            surface.blit(word_surface, text_rect)
            x += word_width + space
        x = pos[0]
        y += word_height
def getDirectoryImageList(directory, getnames=False):#directory. list = return list
    directoryList = []
    namesList = []
    for object in sorted(os.listdir(str(directory)), key=len): 
        if ".png" in object:
            directoryList.append(pygame.image.load(rf"{directory}\{str(object)}").convert_alpha())
            namesList.append(object)
    if getnames == True:
        return directoryList, namesList
    else:
        return directoryList
def getImagesAndOptions(path="", splitStr="SplitThis"):
    images, names = getDirectoryImageList(path, True)
    options = []
    for object in names:
        options.append(object.split(splitStr)[1])
    return images, options
def openImageForMerge(image, sizeRect=(52,52)):
    image = Image.open(image)
    image = image.convert("RGBA")
    if not sizeRect == None: image = image.resize(sizeRect)
    return image
def mergeImages(imageBase, imageLayer, imageBaseRect=(52,52), imageLayerRect=(52,52), overlayX=0, overlayY=0):
    abilityImage = openImageForMerge(imageBase)#it bugs me that merge image requires the image file to be opened directly
    abilityBackImage = openImageForMerge(imageLayer, sizeRect=imageLayerRect)
    abilityBackImage.paste(abilityImage, (overlayX, overlayY), mask=abilityImage)
    return abilityBackImage
def mergeLoadedImages(imageBase, imageLayer, overlayX=0, overlayY=0):
    newImage = imageBase
    newImage.blit(imageLayer, (overlayX, overlayY))
    return newImage
def colorImage(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

class ImageId():
    def __init__(self, object, name):
        self.object = object
        self.name = name
def createGearList(imagesList, optionsList, sizeRect=(75,75), backgroundImage=None, backImgPos=(0,0)):
    newList = []
    i=0
    for object in imagesList:
        if not backgroundImage == None:
            newImage = backgroundImage.copy()
            newImage.blit(pygame.transform.scale(object, sizeRect), backImgPos)
        else:
            newImage = pygame.transform.scale(object, sizeRect)
        newList.append(ImageId(newImage, optionsList[i])); i+=1
    return newList

def abilityIcons(imagePathList, nameList, baseImagePath):
    mainList = []; smallList = []; i=-1
    for object in imagePathList:
        i+=1
        image = mergeImages(object, baseImagePath)
        mode, size, data = image.mode, image.size, image.tobytes() 
        image = pygame.image.fromstring(data, size, mode).convert_alpha()
        mainList.append(ImageId(image, nameList[i]))
        smallList.append(ImageId(pygame.transform.smoothscale(image, (42, 42)), nameList[i]))
    return mainList, smallList

imagesList = getDirectoryImageList(rf"{mainImagePath}")

weaponImages, weaponOptions = getImagesAndOptions(path=rf"{imageDirectory}\weapons", splitStr="Weapon_Main_")
subWeaponImages, subWeaponOptions = getImagesAndOptions(path=rf"{imageDirectory}\subweapons", splitStr="Weapon_Sub_")
specialImages, specialOptions = getImagesAndOptions(path=rf"{imageDirectory}\specials", splitStr="Weapon_Special_")

def dropshadow(imageList, color=(0,0,0,0), bordersize=4):
    newList = []
    for object in imageList:
        newImage = object.copy()
        baseImage = newImage
        colorImage(newImage, color)
        baseImage = mergeLoadedImages(baseImage, newImage, overlayX=0, overlayY=bordersize)
        baseImage = mergeLoadedImages(baseImage, newImage, overlayX=bordersize, overlayY=0)
        baseImage = mergeLoadedImages(baseImage, newImage, overlayX=bordersize, overlayY=bordersize)
        baseImage = mergeLoadedImages(baseImage, object, overlayX=0, overlayY=0)
        newList.append(baseImage)
    return newList
weaponImages = dropshadow(weaponImages, color=(0,0,0,0), bordersize=8)

SSBackground = pygame.transform.scale(imagesList[5], (42,42))

weaponsList   = createGearList(weaponImages,    weaponOptions,    sizeRect=(75,75))
subWeaponList = createGearList(subWeaponImages, subWeaponOptions, sizeRect=(34,34), backgroundImage=SSBackground, backImgPos=(4,4))
specialList   = createGearList(specialImages,   specialOptions,   sizeRect=(34,34), backgroundImage=SSBackground, backImgPos=(4,4))

abilityImagesList = []
abilityOptions = [] 
for object in os.listdir(rf"{imageDirectory}\abilities"): 
    if ".png" in object:
        abilityImagesList.append(rf"{imageDirectory}\abilities\{object}")
        abilityOptions.append(object.replace(".png",""))
abilityOptions.sort()
abilityImages, abilityImagesSmall             = abilityIcons(abilityImagesList, abilityOptions, imagesDirectoryList[1])
abilityImagesGold, abilityImagesSmallGold     = abilityIcons(abilityImagesList, abilityOptions, imagesDirectoryList[2])
abilityImagesSilver, abilityImagesSmallSilver = abilityIcons(abilityImagesList, abilityOptions, imagesDirectoryList[3])
abilityImagesBronze, abilityImagesSmallBronze = abilityIcons(abilityImagesList, abilityOptions, imagesDirectoryList[4])

class imageObject(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.sizex, self.sizey = self.image.get_width(), self.image.get_height()
        self.speed = 1
    def moveRight(self):
        self.rect.x += self.speed
        if self.rect.x >= self.x+self.sizex/2: self.rect.x = self.x
    def moveLeft(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.x-self.sizex/2: self.rect.x = self.x
    def moveUp(self):
        self.rect.y -= self.speed
        if self.rect.y <= self.y-self.sizey/2: self.rect.y = self.y
    def moveDown(self):
        self.rect.y += self.speed
        if self.rect.y >= self.y+self.sizey/2: self.rect.y = self.y
    def update(self, offsetx=0, offsety=0): self.rect.x, self.rect.y = self.x+offsetx, self.y+offsety

''' Need to eventually figure out settings file for lists. Probably in a full revised version'''
image_List      = pygame.sprite.Group()

darkGreen_List  = pygame.sprite.Group()
lightGreen_List = pygame.sprite.Group()
darkPink_List   = pygame.sprite.Group()
lightPink_List  = pygame.sprite.Group()
bo_List         = pygame.sprite.Group()

level_List  = pygame.sprite.Group()
rank_List  = pygame.sprite.Group()

fillSurfaces = ["main", "level", "rank", "green", "pink"]#, "bo"
drawLists = ["mainList", "levelList", "rankList", "greenListLight", "greenListDark", "pinkListLight", "pinkListDark", "boList"]

mainImage = imageObject(imagesList[0], x=0+extraX, y=0+extraY)
image_List.add(mainImage)

#scrolling images
'''Need to figure out out to script this out in Settings file for any adjustments.'''
flip1  = pygame.transform.flip(imagesList[8], True, False) 
flip2  = pygame.transform.flip(imagesList[8], True, False) 

scale1 = pygame.transform.scale(imagesList[8], (1124/1.2,57))
scale2 = pygame.transform.scale(imagesList[9], (994/1.2,75)) 
scale3 = pygame.transform.scale(imagesList[8], (1124/1.5,57)) 
scale4 = pygame.transform.scale(imagesList[9], (994/1.5,75)) 

flip3  = pygame.transform.flip(scale1, True, False)
flip4  = pygame.transform.flip(scale2, True, False)

darkGreenGroup  = [imagesList[8],flip1,flip3,scale1,scale3]
lightGreenGroup = [imagesList[9],flip2,flip4,scale2,scale4]

greenLeft, greenRight = [], []

for object in darkGreenGroup:
    objectA = imageObject(object, x=0, y=25+random.randint(-10,10))
    objectB = imageObject(object, x=-object.get_width()/2, y=25+random.randint(-10,10))
    darkGreen_List.add(objectA); darkGreen_List.add(objectB)
    greenLeft.append(objectA);   greenRight.append(objectB)
    
for object in lightGreenGroup:
    objectA = imageObject(object, x=0, y=10+random.randint(-10,10))
    objectB = imageObject(object, x=-object.get_width()/2, y=10+random.randint(-10,10))
    lightGreen_List.add(objectA); lightGreen_List.add(objectB)
    greenLeft.append(objectA);    greenRight.append(objectB)

'''Need to figure out settings file for doing images'''
greenDots = imageObject(imagesList[10], x=0, y=0)
darkGreen_List.add(greenDots)
darkPink = imageObject(imagesList[12], x=0, y=0)#-172/2
lightPink = imageObject(imagesList[11], x=0, y=-10)#-300/2
darkPink_List.add(darkPink)
lightPink_List.add(lightPink)

boObject = imageObject(imagesList[13], x=0, y=0)
bo_List.add(boObject)


levelPattern = imageObject(imagesList[6], x=0, y=0)
level_List.add(levelPattern)
rankPattern = imageObject(imagesList[7], x=-(imagesList[7].get_width()/2)+222, y=0)
rank_List.add(rankPattern)
levelPattern.speed = 0.5

'''Setting up Current weapon and abilities. Will have to figure out which abilities have been in what position when winning the most and check background accordingly. Might also do Silver and Bronze, but I'll just work on regular and gold for now.'''
currentWeaponImage= imageObject(pygame.transform.scale(weaponImages[random.randint(0,len(weaponImages)-1)], (75,75)), x=267, y=322+extraY)#277+12  414-92
currentSubWeaponImage= imageObject(subWeaponList[random.randint(0,len(subWeaponList)-1)].object, x=379, y=342+extraY)#277+12+90    418-76
currentSpecialImage= imageObject(specialList[random.randint(0,len(specialList)-1)].object, x=429, y=342+extraY)#277+12+140

slotsY=398#418-20
'''headGearMain, headGearFirst, headGearSecond, headGearThird'''
headGearMain   = imageObject(abilityImages[random.randint(0,len(abilityImages)-1)].object, x=277, y=slotsY+extraY)
headGearFirst  = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=335, y=404+extraY)#277+58  
headGearSecond = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=382, y=404+extraY)#277+58+47
headGearThird  = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=429, y=404+extraY)#277+58+47*2
headGearIcons = [headGearMain, headGearFirst, headGearSecond, headGearThird]
'''torsoGearMain, torsoGearFirst, torsoGearSecond, torsoGearThird'''
torsoGearMain   = imageObject(abilityImages[random.randint(0,len(abilityImages)-1)].object, x=277, y=454+extraY)#slotsY+56
torsoGearFirst  = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=335, y=460+extraY)#slotsY+6+56
torsoGearSecond = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=382, y=460+extraY)
torsoGearThird  = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=429, y=460+extraY)
torsoGearIcons = [torsoGearMain, torsoGearFirst, torsoGearSecond, torsoGearThird]
'''footGearMain, footGearFirst, footGearSecond, footGearThird'''
footGearMain   = imageObject(abilityImages[random.randint(0,len(abilityImages)-1)].object, x=277, y=516+extraY)#slotsY+56*2
footGearFirst  = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=335, y=516+extraY)#slotsY+6+56*2
footGearSecond = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=382, y=516+extraY)
footGearThird  = imageObject(abilityImagesSmall[random.randint(0,len(abilityImages)-1)].object, x=429, y=516+extraY)
footGearIcons = [footGearMain, footGearFirst, footGearSecond, footGearThird]

gearNameList   = ["mainweapon",       "subweapon",           "special",
                  "headmain",         "headfirst",           "headsecond",           "headthird",
                  "torsomain",        "torsofirst",          "torsosecond",          "torsothird",
                  "footmain",         "footfirst",           "footsecond",           "footthird"]
gearObjectList = [currentWeaponImage, currentSubWeaponImage, currentSpecialImage,
                  headGearMain,       headGearFirst,         headGearSecond,         headGearThird,
                  torsoGearMain,      torsoGearFirst,        torsoGearSecond,        torsoGearThird,
                  footGearMain,       footGearFirst,         footGearSecond,         footGearThird,]
'''Add to list from settings file'''
for object in settingsList:
    splitObjectList = object.split(" ")
    if splitObjectList[0] == "gear":
        i=-1
        for object in gearNameList:
            i+=1
            if splitObjectList[1] == object:
                gearObject = gearObjectList[i]
                if len(splitObjectList) > 2:
                    try:
                        gearObject.x = int(splitObjectList[2])+extraX
                        gearObject.y = int(splitObjectList[3])+extraY
                        gearObject.update()
                    except: pass
                image_List.add(gearObject)

allGearIcons = [headGearIcons, torsoGearIcons, footGearIcons]

class pointsOutcomeObject():
    def __init__(self, name, points, codename=""):
        self.name = name
        if codename == "": self.codename = self.name
        else: self.codename = codename
        self.points = points
        self.roundsCounter = 0; self.percentage = 0
        self.range = []

counterObjectList = []
class counterObject():#for tracking outcome types
    def __init__(self, outcome, counter=0):
        self.outcome = outcome
        self.counter = counter

class RoundObject():#outcome codename
    def __init__(self, outcome, abilitiesList=[]):
        self.outcome = outcome
        self.abilitiesList = abilitiesList#need to remove and just use counters

def simulateTillLevelGoal(levelsNeeded=levelsNeeded, multiplier=multiplier, chance=[counterObject("W", 38), counterObject("L", 38),counterObject("D", 10),counterObject("KO", 8)]):#always equels 100
    totalPoints, rounds = 0, 0
    '''Setting point objects with defaults, to combine all the variables into single objects'''
    pointsGroup = [pointsOutcomeObject("winPoints", winP*multiplier, codename="W"), pointsOutcomeObject("losePoints", loseP*multiplier, codename="L"), pointsOutcomeObject("defeatPoints", defeatP, codename="D"), pointsOutcomeObject("knockoutPoints", KOP+winP, codename="KO")]
    '''Getting value of previous rounds to divide into 100% range'''
    chanceTotal = 0
    for object in chance: 
        chanceTotal += object.counter
    for object in pointsGroup:
        i=0
        pointsObject = object
        pointsCodeName = object.codename
        for object in chance:
            if pointsCodeName == object.outcome:
                if i >= len(chance): break
                pointsObject.percentage = percentage(object.counter, chanceTotal); i+=1
    '''Setting range lists, with iters 1 to 100. Example: [0,1,2,3,4], [5,6,7,8,9,10] to randomly pick a number and checking the lists for it. This mainly works because it does "-=" for the percentage value as it adds to the list.'''
    for i in range(100):
        for object in pointsGroup:
            if object.percentage > 0: object.range.append(i+1); object.percentage -= 1; break

    battletime, lobbytime = 3, 2;   lastDay = 0
    timeperround = battletime + lobbytime
    '''Simulating how many points per round, based on a 1 in 100 toss, checking what outcome it was, and assigning specified points.'''
    while True:
        if totalPoints > pointsForLevel*levelsNeeded or levelsNeeded == 0: break
        toss = random.randint(1,100)#1-12
        rounds += 1
        if rounds > 2500: break
        outcomeName = ""
        for object in pointsGroup:
            if toss in object.range: 
                totalPoints += object.points; object.roundsCounter += 1; outcomeName += object.name; break#D11%#L6%#W1%#doesn't need percentvalue
           
        days = int((timeperround*rounds/60)/8)
        if not lastDay == days and outcomeName in WinConditions: lastDay = days; totalPoints += firstWinPoints
    '''Returning the counterObject'''
    for object in pointsGroup:
        if object.name == "winPoints": wins = object.roundsCounter
        if object.name == "losePoints": losses = object.roundsCounter
        if object.name == "defeatPoints": defeats = object.roundsCounter
        if object.name == "knockoutPoints": kos = object.roundsCounter
    '''Also setting up percentages again for display'''
    for object in pointsGroup:
        i=0
        pointsObject = object
        pointsCodeName = object.codename
        for object in chance:
            if pointsCodeName == object.outcome:
                if i >= len(chance): break
                pointsObject.percentage = percentage(object.counter, chanceTotal); i+=1
    return maxLevels-levelsNeeded, rf"+{'{:,}'.format(int(totalPoints))}p", int(float(str(timeperround*rounds/60)[:5])), rounds, wins, losses, defeats, kos, pointsGroup
 
lastHundredSwitch = False
def getStats(loops=50, levelsNeeded=levelsNeeded, multiplier=multiplier, baseChance=True):
    global percentList, calculateList, lastHundredSwitch, percentList2
    calculateList = []; calculateHours = []; closestList = []; calculateRounds = []; evenCloserList = []
    for i in range(loops):
        if baseChance == True: calculateList.append(simulateTillLevelGoal(levelsNeeded, multiplier))
        elif lastHundredSwitch == False: calculateList.append(simulateTillLevelGoal(levelsNeeded, multiplier, chance=percentList2))
        else: 
            lastHudredList = []
            i=0
            for object in percentList2.reverse():
                lastHudredList.append(object); i+=1
                if i == 100: break
            calculateList.append(simulateTillLevelGoal(levelsNeeded, multiplier, chance=lastHudredList))
    for object in calculateList:
        calculateHours.append(object[2])
    average = sum(calculateHours) / len(calculateHours)
    closest = min(calculateHours, key=lambda x:abs(x-average))
    for object in calculateList:
        if object[2] == closest: closestList.append(object)

    for object in closestList:
        calculateRounds.append(object[3])
    average = sum(calculateRounds) / len(calculateRounds)
    closest = min(calculateRounds, key=lambda x:abs(x-average))
    for object in closestList:
        if object[3] == closest: evenCloserList.append(object)
    if len(evenCloserList) > 0: closestList = evenCloserList

    random.shuffle(closestList)
    return closestList[0]

def percentValues(list):
    '''W, L, D, KO = 0, 0, 0, 0'''
    counterObjectList = []
    for object in list:
        if not type(object) == str:
            if type(object.outcome) == str: 
                outcome = object.outcome
                exists = False
                for object in counterObjectList:
                    if outcome == object.outcome: object.counter += 1; exists = True; break
                if exists == False:
                    newOutcome = counterObject(outcome)
                    counterObjectList.append(newOutcome); newOutcome.counter += 1
        else:
            outcome = object
            exists = False
            for object in counterObjectList:
                if outcome == object.outcome: object.counter += 1; exists = True; break
            if exists == False:
                newOutcome = counterObject(outcome)
                counterObjectList.append(newOutcome); newOutcome.counter += 1
    '''I would convert all counterObject from list into return list, but I need to know the names of counterObject when setting buttons and displays'''
    returnList = []
    returnList = counterObjectList
    return returnList
    '''[A, B, C]'''

percentList = []
for i in range(40): percentList.append(RoundObject("KO"))
for i in range(30): percentList.append(RoundObject("W"))
for i in range(20): percentList.append(RoundObject("L"))
for i in range(10): percentList.append(RoundObject("D"))

percentList = pickleVar(percentList, "percentList", True)

percentListX = percentList.copy()
random.shuffle(percentListX)
percentList2 = percentValues(percentList)

currentHeadGear  = pickleVar(["64px-S3_Ability_Ink_Saver_(Main)",  "64px-S3_Ability_Ink_Resistance_Up", "64px-S3_Ability_Swim_Speed_Up", "64px-S3_Ability_Ink_Recovery_Up"], "currentHeadGear", True)#do I actually need repickle
currentTorsoGear = pickleVar(["64px-S3_Ability_Ink_Saver_(Sub)",   "64px-S3_Ability_Quick_Respawn",     "64px-S3_Ability_Run_Speed_Up",  "64px-S3_Ability_Quick_Super_Jump"], "currentTorsoGear", True)
currentFootGear  = pickleVar(["64px-S3_Ability_Special_Charge_Up", "64px-S3_Ability_Sub_Power_Up",      "64px-S3_Ability_Special_Saver", "64px-S3_Ability_Sub_Resistance_Up"], "currentFootGear", True)
allCurrentGear   = pickleVar([currentHeadGear, currentTorsoGear, currentFootGear], "allCurrentGear", True)

def saveCurrentGear():
    with open(rf"{pickleLand}\currentHeadGear.pkl", "wb") as p: pickle.dump(currentHeadGear, file=p)
    with open(rf"{pickleLand}\currentTorsoGear.pkl", "wb") as p: pickle.dump(currentTorsoGear, file=p)
    with open(rf"{pickleLand}\currentFootGear.pkl", "wb") as p: pickle.dump(currentFootGear, file=p)
    with open(rf"{pickleLand}\allCurrentGear.pkl", "wb") as p: pickle.dump(allCurrentGear, file=p)

HeadGearMainList=[]; TorsoGearMainList=[]; FootGearMainList=[]
def doAllAbilities():
    global percentList, HeadGearMainList, TorsoGearMainList, FootGearMainList, allCurrentGear
    HeadGearMainList=[]
    TorsoGearMainList=[]
    FootGearMainList=[]
    for object in percentList:
        if len(object.abilitiesList) > 0 and object.outcome in WinConditionCodes:
            HeadGearMainList.append(object.abilitiesList[0])
            TorsoGearMainList.append(object.abilitiesList[1])
            FootGearMainList.append(object.abilitiesList[2])
    allGearOutcomeList = [HeadGearMainList, TorsoGearMainList, FootGearMainList]
    SlotReturnsList = []
    for object in allGearOutcomeList:
        gearOutcomeList = object
        if len(gearOutcomeList) > 0:
            for i in range(4):
                newSlotList=[]
                for object in gearOutcomeList:
                    newSlotList.append(object[i])
                SlotReturnsList.append(newSlotList)

    GoldSlotReturnsList = []
    SilverSlotReturnsList = []
    BronzeSlotReturnsList = []
    i=0
    for object in SlotReturnsList:
        goldObject = object
        bestObject = max(set(goldObject), key=goldObject.count)
        GoldSlotReturnsList.append(bestObject)
        try:
            silverObject = []
            for object in goldObject:
                if not object == bestObject: silverObject.append(object)
            bestObject = max(set(silverObject), key=silverObject.count)
            SilverSlotReturnsList.append(bestObject)
        except:pass
        try:
            bronzeObject = []
            for object in silverObject:
                if not object == bestObject: bronzeObject.append(object)
            bestObject = max(set(bronzeObject), key=bronzeObject.count)
            BronzeSlotReturnsList.append(bestObject)
        except:pass
    i=0
    returnId = 0
    for object in allGearIcons:
        mainlist = object
        idx=0
        for object in mainlist:
            iconObject = object
            newIcon = None
            if idx == 0:#main
                if len(GoldSlotReturnsList) > returnId and allCurrentGear[i][idx] == GoldSlotReturnsList[returnId]:
                    for object in abilityImagesGold:
                        if object.name == GoldSlotReturnsList[returnId]: newIcon = object.object
                elif len(SilverSlotReturnsList) > returnId and allCurrentGear[i][idx] == SilverSlotReturnsList[returnId]:
                    for object in abilityImagesSilver:
                        if object.name == SilverSlotReturnsList[returnId]: newIcon = object.object
                elif len(BronzeSlotReturnsList) > returnId and allCurrentGear[i][idx] == BronzeSlotReturnsList[returnId]:
                    for object in abilityImagesBronze:
                        if object.name == BronzeSlotReturnsList[returnId]: newIcon = object.object
                else:
                    for object in abilityImages:
                        if object.name == allCurrentGear[i][idx]: newIcon = object.object
            else:#Small
                if len(GoldSlotReturnsList) > returnId and allCurrentGear[i][idx] == GoldSlotReturnsList[returnId]:
                    for object in abilityImagesSmallGold:
                        if object.name == GoldSlotReturnsList[returnId]: newIcon = object.object
                elif len(SilverSlotReturnsList) > returnId and allCurrentGear[i][idx] == SilverSlotReturnsList[returnId]:
                    for object in abilityImagesSmallSilver:
                        if object.name == SilverSlotReturnsList[returnId]: newIcon = object.object
                elif len(BronzeSlotReturnsList) > returnId and allCurrentGear[i][idx] == BronzeSlotReturnsList[returnId]:
                    for object in abilityImagesSmallBronze:
                        if object.name == BronzeSlotReturnsList[returnId]: newIcon = object.object
                else:
                    for object in abilityImagesSmall:
                        if object.name == allCurrentGear[i][idx]: newIcon = object.object
            idx+=1
            returnId+=1
            try: 
                if not newIcon == None: iconObject.image = newIcon
                else: iconObject.image = pygame.transform.scale(imagesList[1], (42, 42))
            except: iconObject.image = pygame.transform.scale(imagesList[1], (42, 42))
        i+=1
    saveCurrentGear()

KOAbilityPoints = 65
WinAbilityPoints = 35
LoseAbilityPoints = -40
DefeatAbilityPoints = -60
abilityCountersList = [[[],[],[]],[[],[],[]],[[],[],[]]]
def makeRound(type):
    global percentList, percentListX, percentList2, lastType, allCurrentGear, abilityCountersList
    newObject = RoundObject(type, allCurrentGear)#need to do counters rather than lists, although will also need to update values when rotating round
    percentList.append(newObject)

    if type == "KO": roundAbilityPoints = KOAbilityPoints
    if type == "W": roundAbilityPoints = WinAbilityPoints
    if type == "L": roundAbilityPoints = LoseAbilityPoints
    if type == "D": roundAbilityPoints = DefeatAbilityPoints
    '''#lastType = type
    ix = 0
    for object in allCurrentGear:#[currentHeadGear, currentTorsoGear, currentFootGear]
        gearListObject = object
        print(type(gearListObject))#lists for each slot, counterObjects for each list
        iy = 0
        for object in gearListObject:
            gearObject = object
            print(gearObject)
            exists = False
            for object in abilityCountersList[ix][iy]:#counterObject():#outcome, counter=0
                if object.outcome in gearObject: exists = True; abilityCounter = object
            if exists == False:
                abilityCounter = counterObject(gearObject, 0)
                abilityCountersList[ix][iy].append(abilityCounter)
            abilityCounter.counter += roundAbilityPoints
    #get best counts for each slot, Gold -> Silver -> Bronze
    #make lists based on counters, if tied == Gold: add to Gold list, ect'''
    

    if hundredLimit == True:
        while True:
            if len(percentList) > maxRounds: percentList.pop(0)
            else: break

    percentList2 = percentValues(percentList)
    with open(rf"{pickleLand}\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p)
    tkMake()

def checkCounter(counter, counterMax, addition=0, counterMin=1):
    counter += addition
    if counter > counterMax: return int(counterMin)
    if counter < counterMin: return int(counterMax)
    return counter

def multiplierButton():
    global multiplierInt, multiplier, multipliers
    multiplierInt = checkCounter(multiplierInt, len(multipliers)-1, addition=1, counterMin=0)
    multiplier = multipliers[multiplierInt]
    with open(rf"{pickleLand}\multiplier.pkl", "wb") as p: pickle.dump(multiplier, file=p)

def baseChanceButton():
    global baseChance
    baseChance = not baseChance
    tkMake()
    with open(rf"{pickleLand}\baseChance.pkl", "wb") as p: pickle.dump(baseChance, file=p)

def level(value):
    global CurrentLevel, levelsNeeded
    CurrentLevel = checkCounter(CurrentLevel, maxLevels, addition=value)
    levelsNeeded = maxLevels-CurrentLevel
    with open(rf"{pickleLand}\CurrentLevel.pkl", "wb") as p: pickle.dump(CurrentLevel, file=p)
def rLevel(value):
    global currentRegularLevel
    currentRegularLevel = checkCounter(currentRegularLevel, regularLevelMax, addition=value)
    with open(rf"{pickleLand}\currentRegularLevel.pkl", "wb") as p: pickle.dump(currentRegularLevel, file=p)
def rankLevel(value):
    global RankCounter
    RankCounter = checkCounter(RankCounter, len(Ranks)-1, addition=value)
    with open(rf"{pickleLand}\rankCounter.pkl", "wb") as p: pickle.dump(RankCounter, file=p)

def rotateRoundId(pos,id):
    '''if   pos == "W": percentList[id] = "L"'''
    global percentList, percentList2
    i=0
    newOutcome = ""
    for object in percentList2:
        nextIter = i+1
        if nextIter >= len(percentList2): nextIter = 0; i = -1
        if pos.outcome == object.outcome: newOutcome = percentList2[nextIter].outcome
        i += 1
    percentList[id].outcome = newOutcome
    percentList2 = percentValues(percentList)
    with open(rf"{pickleLand}\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p)
    tkMake()

backgroundsMove = pickleVar(False, "backgroundsMove")

def backgroundsMoveButton():
    global backgroundsMove
    backgroundsMove = not backgroundsMove
    tkMake()
    with open(rf"{pickleLand}\backgroundsMove.pkl", "wb") as p: pickle.dump(backgroundsMove, file=p)

def saveRounds():
    global percentList; i=0
    with open(roundsFile, "w+") as f:
        for object in percentList:
            if i == len(percentList)-1: f.write(object.outcome)
            else: f.write(object.outcome + ", "); i += 1
    tkMake()

def loadRounds():
    global percentList
    percentList = []
    with open(roundsFile, "r") as f:
        for line in f:
            for object in line.split(","):
                percentList.append(RoundObject(object.replace(" ","")))
    tkMake()


def resetRounds():
    global percentList, percentList2, currentHeadGear, currentTorsoGear, currentFootGear, allCurrentGear
    currentHeadGear = [abilityOptions[0], abilityOptions[0], abilityOptions[0], abilityOptions[0]]
    currentTorsoGear = [abilityOptions[0], abilityOptions[0], abilityOptions[0], abilityOptions[0]]
    currentFootGear = [abilityOptions[0], abilityOptions[0], abilityOptions[0], abilityOptions[0]]
    allCurrentGear = [currentHeadGear, currentTorsoGear, currentFootGear]
    percentList = []
    for i in range(2): percentList.append(RoundObject("KO"))
    for i in range(2): percentList.append(RoundObject("D"))
    for i in range(3): percentList.append(RoundObject("L"))
    for i in range(4): percentList.append(RoundObject("W"))
    percentList2 = percentValues(percentList)
    with open(rf"{pickleLand}\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p),     p.close()
    tkMake()

Tkfont = Font(size=16, weight=BOLD)
label1= tkinter.Label(buttonwin, text=rf"x", font=Tkfont, fg='white', bg='#262626')
label2= tkinter.Label(buttonwin, text=rf"x", font=Tkfont, fg='white', bg='#262626')
label3= tkinter.Label(buttonwin, text=rf"x", font=Tkfont, fg='white', bg='#262626')
label4= tkinter.Label(buttonwin, text=rf"x", font=Tkfont, fg='white', bg='#262626')
for object in percentList2:
    if object.counter > 999: text = "999+"
    else: text = object.counter
    if object.outcome == "KO": label1.configure(text=rf"{text}")
    if object.outcome == "W": label2.configure(text=rf"{text}")
    if object.outcome == "L": label3.configure(text=rf"{text}")
    if object.outcome == "D": label4.configure(text=rf"{text}")
label1.place(x=125,y=0); label2.place(x=125,y=25);  label3.place(x=295,y=0);  label4.place(x=295,y=25)

ButtonImages = [tkinter.PhotoImage(file=imagesDirectoryList[14]), tkinter.PhotoImage(file=imagesDirectoryList[15]), tkinter.PhotoImage(file=imagesDirectoryList[16]), tkinter.PhotoImage(file=imagesDirectoryList[17])]
roundImages = {"KO":tkinter.PhotoImage(file=imagesDirectoryList[18]), "W":tkinter.PhotoImage(file=imagesDirectoryList[19]), "L":tkinter.PhotoImage(file=imagesDirectoryList[20]), "D":tkinter.PhotoImage(file=imagesDirectoryList[21])}
ButtonImages2 = [tkinter.PhotoImage(file=imagesDirectoryList[22]), tkinter.PhotoImage(file=imagesDirectoryList[23]), tkinter.PhotoImage(file=imagesDirectoryList[24]), tkinter.PhotoImage(file=imagesDirectoryList[25]), tkinter.PhotoImage(file=imagesDirectoryList[26]), tkinter.PhotoImage(file=imagesDirectoryList[27])]
ButtonImages3 = [tkinter.PhotoImage(file=imagesDirectoryList[28]), tkinter.PhotoImage(file=imagesDirectoryList[31]), tkinter.PhotoImage(file=imagesDirectoryList[32]), tkinter.PhotoImage(file=imagesDirectoryList[33]), tkinter.PhotoImage(file=imagesDirectoryList[34])]

ChanceButtonImages = [tkinter.PhotoImage(file=imagesDirectoryList[29]), tkinter.PhotoImage(file=imagesDirectoryList[30])]

tkinter.Button(buttonwin, command=lambda: makeRound("KO"), height=50, width=50, bg="dim grey", image=ButtonImages[0]).place(x=10,y=0)
tkinter.Button(buttonwin, command=lambda: makeRound("W"), height=50, width=50, bg="dim grey", image=ButtonImages[1]).place(x=70,y=0)
tkinter.Button(buttonwin, command=lambda: makeRound("L"), height=50, width=50, bg="dim grey", image=ButtonImages[2]).place(x=180,y=0)
tkinter.Button(buttonwin, command=lambda: makeRound("D"), height=50, width=50, bg="dim grey", image=ButtonImages[3]).place(x=240,y=0)

tkinter.Button(buttonwin, command=lambda: rLevel(1), height=25, width=50, bg="dim grey", image=ButtonImages2[0]).place(x=0,y=WINDOWSIZEY-56)
tkinter.Button(buttonwin, command=lambda: rLevel(-1), height=25, width=50, bg="dim grey", image=ButtonImages2[1]).place(x=0,y=WINDOWSIZEY-30)

tkinter.Button(buttonwin, command=lambda: rankLevel(1), height=25, width=50, bg="dim grey", image=ButtonImages2[2]).place(x=60,y=WINDOWSIZEY-56)
tkinter.Button(buttonwin, command=lambda: rankLevel(-1), height=25, width=50, bg="dim grey", image=ButtonImages2[3]).place(x=60,y=WINDOWSIZEY-30)

tkinter.Button(buttonwin, command=lambda: level(1), height=25, width=50, bg="dim grey", image=ButtonImages2[4]).place(x=120,y=WINDOWSIZEY-56)
tkinter.Button(buttonwin, command=lambda: level(-1), height=25, width=50, bg="dim grey", image=ButtonImages2[5]).place(x=120,y=WINDOWSIZEY-30)

tkinter.Button(buttonwin, command=multiplierButton, height=50, width=50, bg="dim grey", image=ButtonImages3[0]).place(x=180,y=WINDOWSIZEY-56)

if   baseChance == True:  chanceButtonImage = ChanceButtonImages[1]#grey
elif baseChance == False: chanceButtonImage = ChanceButtonImages[0]#color
ChanceButton = tkinter.Button(buttonwin, command=baseChanceButton, height=50, width=50, bg="dim grey", image=chanceButtonImage)
ChanceButton.place(x=240,y=WINDOWSIZEY-56)

ScrollButton = tkinter.Button(buttonwin, command=backgroundsMoveButton, height=25, width=50, bg="dim grey", image=ButtonImages3[1])
ScrollButton.place(x=WINDOWSIZEX-60*4,y=WINDOWSIZEY-30)

saveRoundsButton = tkinter.Button(buttonwin, command=saveRounds, height=50, width=50, bg="dim grey", image=ButtonImages3[2])
loadRoundsButton = tkinter.Button(buttonwin, command=loadRounds, height=50, width=50, bg="dim grey", image=ButtonImages3[3])
saveRoundsButton.place(x=WINDOWSIZEX-60*2,y=WINDOWSIZEY-56);   loadRoundsButton.place(x=WINDOWSIZEX-60*1,y=WINDOWSIZEY-56)

tkinter.Button(buttonwin, command=lambda: resetRounds(), height=25, width=50, bg="dim grey", image=ButtonImages3[4]).place(x=WINDOWSIZEX-60*3,y=WINDOWSIZEY-30)

tkframe = tkinter.Frame(buttonwin, width=WINDOWSIZEX, height=9*60)
tkframe['background']='#262626'
tkframe.place(x=0,y=70)

class roundbutton():
    def __init__(self, id, y, image):
        self.id = id
        self.button = tkinter.Button(tkframe, command=lambda: self.command(), width=(WINDOWSIZEX-30-80)/1.5, height=50, bg="dim grey", image=image)
        self.button.place(x=10,y=(y*60))
    def command(self): rotateRoundId(percentList[self.id],self.id)

roundButtons = []
for i in range(9):
    id=len(percentList)-1-i
    image = roundImages[percentList[id].outcome]
    roundButtons.append(roundbutton(id,i, image))

class gearLists():
    def __init__(self, title="Head Main", x=WINDOWSIZEX-160, y=60, listX=abilityOptions, color="#262626"):
        self.value_inside = tkinter.StringVar(buttonwin)
        self.title = title
        self.value_inside.set(self.title) 
        self.list = listX
        self.Droplist = tkinter.OptionMenu(buttonwin, self.value_inside, *self.list) 
        self.Droplist.config(font=buttonFont, fg="white", bg=color, borderwidth=0, highlightthickness=1)
        self.Droplist.place(x=x,y=y)

def getGearLists(droplistList, geartype):
    i=0
    for object in droplistList:
        gearObject = object.value_inside.get()
        if gearObject in abilityOptions: geartype[i] = gearObject
        object.value_inside.set(object.title)
        i+=1
    return geartype

def isNewGear(oldGear, newGear, name):
    if not newGear in ["Weapon", "Sub", "Special"]:
        oldGear = newGear
        with open(rf"{pickleLand}\{name}.pkl", "wb") as p: pickle.dump(oldGear, file=p)
    return oldGear
def updateGear():
    global currentHeadGear, currentTorsoGear, currentFootGear, allCurrentGear, currentWeapon, currentSubWeapon, currentSpecial
    currentWeapon    = isNewGear(currentWeapon,    weaponDroplist.value_inside.get(),    "currentWeapon"); weaponDroplist.value_inside.set(weaponDroplist.title)
    currentSubWeapon = isNewGear(currentSubWeapon, subWeaponDropList.value_inside.get(), "currentSubWeapon"); subWeaponDropList.value_inside.set(subWeaponDropList.title)
    currentSpecial   = isNewGear(currentSpecial,   specialDroplist.value_inside.get(),   "currentSpecial"); specialDroplist.value_inside.set(specialDroplist.title)
    currentHeadGear = getGearLists(headGearDropLists, currentHeadGear)
    currentTorsoGear = getGearLists(torsoGearDropLists, currentTorsoGear)
    currentFootGear = getGearLists(footGearDropLists, currentFootGear)
    allCurrentGear = [currentHeadGear, currentTorsoGear, currentFootGear]
    tkMake()

buttonFont = Font(size=9, weight=BOLD)
OffsetX = -70; OffsetY = 20
tkinter.Button(buttonwin, text=" Update Gear ", command=lambda: updateGear(), font=buttonFont, fg="white", bg="#262626", borderwidth=2, highlightthickness=1).place(x=WINDOWSIZEX-90, y=50+OffsetY)#WINDOWSIZEX-120,y=15

weaponDroplist    = gearLists("Weapon", WINDOWSIZEX-160+OffsetX, 50+30+OffsetY, listX=weaponOptions, color="#804438")#ff886f
subWeaponDropList   = gearLists("Sub", WINDOWSIZEX-140+OffsetX, 50+60+OffsetY, listX=subWeaponOptions)
specialDroplist    = gearLists("Special", WINDOWSIZEX-150+OffsetX, 50+90+OffsetY, listX=specialOptions)

droplistY=90+OffsetY
headGearDroplistMain   = gearLists("Head Main", WINDOWSIZEX-160+OffsetX, 100+droplistY, color="#3d4880")#7387f0
headGearDroplistFirst  = gearLists("Head 1st", WINDOWSIZEX-140+OffsetX, 130+droplistY)
headGearDroplistSecond = gearLists("Head 2nd", WINDOWSIZEX-140+OffsetX, 160+droplistY)
headGearDroplistThird  = gearLists("Head 3rd", WINDOWSIZEX-140+OffsetX, 190+droplistY)
headGearDropLists = [headGearDroplistMain, headGearDroplistFirst, headGearDroplistSecond, headGearDroplistThird]

torsoGearDroplistMain   = gearLists("Troso Main", WINDOWSIZEX-160+OffsetX, 100+140+droplistY, color="#458074")#68c0ae
torsoGearDroplistFirst  = gearLists("Troso 1st", WINDOWSIZEX-140+OffsetX, 130+140+droplistY)
torsoGearDroplistSecond = gearLists("Troso 2nd", WINDOWSIZEX-140+OffsetX, 160+140+droplistY)
torsoGearDroplistThird  = gearLists("Troso 3rd", WINDOWSIZEX-140+OffsetX, 190+140+droplistY)
torsoGearDropLists = [torsoGearDroplistMain, torsoGearDroplistFirst, torsoGearDroplistSecond, torsoGearDroplistThird]

footGearDroplistMain   = gearLists("Foot Main", WINDOWSIZEX-160+OffsetX, 100+(140*2)+droplistY, color="#534480")#987ce8
footGearDroplistFirst  = gearLists("Foot 1st", WINDOWSIZEX-140+OffsetX, 130+(140*2)+droplistY)
footGearDroplistSecond = gearLists("Foot 2nd", WINDOWSIZEX-140+OffsetX, 160+(140*2)+droplistY)
footGearDroplistThird  = gearLists("Foot 3rd", WINDOWSIZEX-140+OffsetX, 190+(140*2)+droplistY)
footGearDropLists = [footGearDroplistMain, footGearDroplistFirst, footGearDroplistSecond, footGearDroplistThird]

def tkMake():
    global currentWeapon, currentSubWeapon, currentSpecial
    '''need to set these specifically, will probably have to allow modifications to the tk window'''
    labelcounterObject = []
    for object in percentList2:
        if object.counter > 999: text = "999+"
        else: text = object.counter
        if not object.outcome in labelcounterObject: labelcounterObject.append(object.outcome)
        if object.outcome == "KO": label1.configure(text=rf"{text}")
        if object.outcome == "W": label2.configure(text=rf"{text}")
        if object.outcome == "L": label3.configure(text=rf"{text}")
        if object.outcome == "D": label4.configure(text=rf"{text}")
    if not "W" in labelcounterObject: label1.configure(text=rf"0")
    if not "L" in labelcounterObject: label2.configure(text=rf"0")
    if not "D" in labelcounterObject: label3.configure(text=rf"0")
    if not "KO" in labelcounterObject: label4.configure(text=rf"0")
    if   baseChance == True:  chanceButtonImage = ChanceButtonImages[1]#grey
    elif baseChance == False: chanceButtonImage = ChanceButtonImages[0]#color
    ChanceButton.configure(image=chanceButtonImage)
    for i in range(9):
        id=len(percentList)-1-i
        image = roundImages[percentList[id].outcome]
        roundButtons.append(roundbutton(id,i, image))
        roundButtons[i].button.configure(image=image)
    try:
        doAllAbilities()
    except:
        for object in allGearIcons:
            for object in object:
                object.image = pygame.transform.scale(imagesList[1], (42, 42))
    for object in weaponsList:
        if object.name == currentWeapon:
            currentWeaponImage.image = object.object
    for object in subWeaponList:
        if object.name == currentSubWeapon:
            currentSubWeaponImage.image = object.object
    for object in specialList:
        if object.name == currentSpecial:
            currentSpecialImage.image = object.object

def noBackground(list):
    if len(list) == 4 and list[3] == 0: return True
    else: return False

pointsVar = 0; multiplierVar = 1.0; hoursVar = 0; roundsVar = 0
varList = [    "{CurrentLevel}", "{pointsNeeded}", "{multiplier}", "{hours}", "{rounds}",    "{regularLevel}",   "{rank}"]
varObjectList = [CurrentLevel,     pointsVar,     multiplierVar,  hoursVar,  roundsVar, currentRegularLevel, Ranks[RankCounter]]
class textObject():
    def __init__(self, text, color=(255,255,255), surface=WindowSurface, x=0, y=0, center=True, size=49):
        self.text = text
        self.color = color
        self.surface = surface
        self.size = size
        self.x, self.y = int(x), int(y)
        if self.surface == WindowSurface: self.x += extraX
        self.center = center
    def draw(self, nameList, variableList):
        global extraX, extraY
        string = self.text
        i=-1
        for object in nameList:
            i+=1
            if object in string:
                string = string.replace(object, rf"{variableList[i]}")
        y=self.y
        if self.surface == WindowSurface: y = self.y+extraY
        if self.center == True:
            drawText(  rf"{string}",         self.color, self.surface, 0, 0, centerCords=(self.x, y), centerBool=True, fontSize=self.size)
        else: drawText(rf"{string}",         self.color, self.surface, self.x, y, centerBool=False,   fontSize=self.size)

'''could probably setup lists with surfaces to varify settings'''
surfacesNamesList = ["WindowSurface", "GreenSurface", "PinkSurface", "BOSurface", "LevelSurface", "RankSurface"]
surfacesList = [     WindowSurface,    GreenSurface,   PinkSurface,   BOSurface,   LevelSurface,   RankSurface]
textGroup = []
averagesTextGroup = []
roundsPrediction = []
textGroupNames = ["group:text", "group:averages", "group:rounds"]
textGroups = [   textGroup,    averagesTextGroup, roundsPrediction]
for object in settingsList:
    if object.startswith("text "):
        textInput = object.split('"')[1]
        object = object.replace(textInput,"String")

        splitline = object.replace('\n', '').split(" ")
        splitline[1] = splitline[1].replace('"', '')
        try:
            colorVar = splitline.split("(")[1].split(")")[0].split(",")
            colorVar = int(colorVar)[0], int(colorVar)[1], int(colorVar)[2]
        except: colorVar = 255,255,255
        surfaceVar = WindowSurface
        size=49
        textGroupObject = textGroup
        for object in splitline:
            splitObject = object
            if "size:" in splitObject:
                try: size = int(splitObject.split(":")[1])
                except: pass
            if "group:" in splitObject:
                i=0
                for object in textGroupNames:
                    if object == splitObject:
                        textGroupObject = textGroups[i]
                    i+=1
            if splitObject in surfacesNamesList:
                i=0
                for object in surfacesNamesList:
                    if splitObject == object: surfaceVar = surfacesList[i]
                    i+=1
        if "center" in splitline or "centre" in splitline:
            textGroupObject.append(textObject(textInput, color=(colorVar), surface=surfaceVar, x=splitline[2], y=splitline[3], center=True, size=size))
        else:textGroupObject.append(textObject(textInput, color=(colorVar), surface=surfaceVar, x=splitline[2], y=splitline[3], center=False, size=size))

tkMake()
tkframe.update()
MainWindow.update()
statsObject = getStats(50, levelsNeeded, multiplier, baseChance)
tick, down = 60, 0
while True:
    if tick == 60:
        pointsVar = statsObject[1]
        multiplierVar = multiplier*1.0
        hoursVar = statsObject[2]
        roundsVar = statsObject[3]
        statsObject = getStats(1, levelsNeeded, multiplier, baseChance)
        tick = 0
    varObjectList = [CurrentLevel, pointsVar, multiplierVar, hoursVar, roundsVar, currentRegularLevel, Ranks[RankCounter]]
    try:#close everything is the mainwindow is closed
        if MainWindow.winfo_exists(): 
            tkframe.update()
            MainWindow.update()
    except: terminate()
    tick += 1
    mainClock.tick(FPS)
    '''need to setup draw order in settings file'''
    for object in settingsList:#would like to set all this in object form so I can add and remove anything from the settings file
        settingsObject = object
        if settingsObject.startswith("fillSurface:"):
            splitObject = settingsObject.split(":")[1].replace("\n","").replace(" ","")
            if splitObject in fillSurfaces:
                if splitObject == "main":
                    if not noBackground(backgroundColor): WindowSurface.fill(backgroundColor)
                if splitObject == "level":
                    if not noBackground(levelBackgroundColor): LevelSurface.fill(levelBackgroundColor)
                if splitObject == "rank":
                    if not noBackground(rankBackgroundColor): RankSurface.fill(rankBackgroundColor)
                if splitObject == "green":
                    if not noBackground(greenBackgroundColor): GreenSurface.fill(greenBackgroundColor)
                if splitObject == "pink":
                    if not noBackground(pinkBackgroundColor): PinkSurface.fill(pinkBackgroundColor)
        if settingsObject.startswith("drawList:"):
            splitObject = settingsObject.split(":")[1].replace("\n","")
            if splitObject in drawLists:
                if splitObject == "mainList": image_List.draw(WindowSurface)
                if splitObject == "levelList": level_List.draw(LevelSurface)
                if splitObject == "rankList": rank_List.draw(RankSurface)
                if splitObject == "greenListLight": lightGreen_List.draw(GreenSurface)
                if splitObject == "greenListDark": darkGreen_List.draw(GreenSurface)
                if splitObject == "pinkListLight":lightPink_List.draw(PinkSurface)
                if splitObject == "pinkListDark": darkPink_List.draw(PinkSurface)
                if splitObject == "boList": bo_List.draw(BOSurface)

    for object in textGroup:
        object.draw(varList, varObjectList)

    if baseChance == False:
        knockoutPoints,   winPoints,   losePoints,   defeatPoints = 0,0,0,0
        for object in statsObject[8]:#pointsOutcomeObject
            if object.name == "knockoutPoints": knockoutPoints = object.percentage
            if object.name == "winPoints": winPoints = object.percentage
            if object.name == "losePoints": losePoints = object.percentage
            if object.name == "defeatPoints": defeatPoints = object.percentage
        averagesNamesList = ["{knockoutPoints}", "{winPoints}", "{losePoints}", "{defeatPoints}"]
        averagesList = [      knockoutPoints,   winPoints,   losePoints,   defeatPoints]
        for object in averagesTextGroup:
            object.draw(averagesNamesList, averagesList)

    roundsPredictionNamesList = ["{knockoutRound}", "{winRound}", "{loseRound}", "{defeatRound}"]
    roundsPredictionList = [      statsObject[7],   statsObject[4],   statsObject[5],   statsObject[6]]
    for object in roundsPrediction:
        object.draw(roundsPredictionNamesList, roundsPredictionList)

    pygame.display.update()
    for event in pygame.event.get():#just so it doesn't freeze
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE: terminate()
    if tick % 2 == 0:
        if tick % 4 == 0 and backgroundsMove == True:
            lightPink.moveUp()
            darkPink.moveLeft()
            greenDots.moveLeft()
            levelPattern.moveLeft()

            rankPattern.moveLeft()
        if backgroundsMove == True:
            darkPink.moveUp()
            lightPink.moveLeft()
            boObject.moveUp()

            levelPattern.moveUp()
            for object in greenLeft:   object.moveLeft()
            for object in greenRight:  object.moveRight()