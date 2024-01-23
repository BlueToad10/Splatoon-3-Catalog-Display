import random, time

regular, splatfest, closeout = 1, 1.2, 1.5
multipliers = [regular, splatfest, closeout]

#need to make a thing for anarchy battle rules

###################      0-1
multiplier = multipliers[0]
levelsNeeded = 100#-77
####################

def percentage(part, whole):
    try: Percentage = 100 * float(part)/float(whole)
    except: Percentage = 0
    return int(Percentage)

def calculate(returnBool=False, levelsNeeded=levelsNeeded, multiplier=multiplier, chance=[42,42,16]):#always equels 100
    total=0
    rounds=0
    disconnect, lose, win = 0, 800*multiplier, 1400*multiplier
    disconnects, losses, wins = 0, 0, 0
    chanceTotal = chance[0] + chance[1] + chance[2]#should get accurate 100%
    winPercent = percentage(chance[0], chanceTotal)
    losePercent = percentage(chance[1], chanceTotal)
    disconnectPercent = percentage(chance[2], chanceTotal)#->100#percentage(chance[2], 100)+winPercent+losePercent
    chancePercent = winPercent+losePercent+disconnectPercent
    #print(f"{chanceTotal}: {winPercent}, {losePercent}, {disconnectPercent}.     {chancePercent}")
    winRange = []
    loseRange = []
    disconnectRange = []
    for i in range(100):
        if winPercent > 0: 
            winRange.append(i+1)
            winPercent -= 1
        elif losePercent > 0:
            loseRange.append(i+1)
            losePercent -= 1
        elif disconnectPercent > 0:
            disconnectRange.append(i+1)
            disconnectPercent -= 1
    #print(f"{chanceTotal}: {winPercent}, {losePercent}, {disconnectPercent}.     {chancePercent}")
    
    battletime,lobbytime = 3, 2
    timeperround = battletime + lobbytime
    while True:
        toss = random.randint(1,100)#1-12
        rounds += 1
        if toss in disconnectRange:#11
            total += disconnect
            disconnects += 1
            
        elif toss in loseRange:#6
            total += lose
            losses += 1
        elif toss in winRange:#1#doesn't need percentvalue
            total += win
            wins += 1
        if len(disconnectRange) == 100: 
            disconnects = 3.14159265
            total = 9500*levelsNeeded+9
        if total > 9500*levelsNeeded: break
    if not returnBool == True:
        print(f"Lvl {100-levelsNeeded}->100,  +{'{:,}'.format(int(total))}p in  {int(float(str(timeperround*rounds/60)[:5]))}H   {rounds}:  {wins}W  {losses}L  {disconnects}D  x{multiplier}")
        time.sleep(1)
        total=0
        rounds=0
        disconnect, lose, win = 0, 800*multiplier, 1400*multiplier
        disconnects, losses, wins = 0, 0, 0
    if returnBool == True:
        return 100-levelsNeeded, f"+{'{:,}'.format(int(total))}p", int(float(str(timeperround*rounds/60)[:5])), rounds, wins, losses, disconnects, multiplier
    
import random, sys, pygame, os, pickle, tkinter
from pygame.locals import *
from PIL import ImageTk, Image
from tkinter.font import BOLD, Font 
version = "1.2"

def load(fileName):
    pickleFile = open(fileName, "rb")
    pickleObj = pickle.load(pickleFile)
    return pickleObj

regular, splatfest, closeout = 1, 1.2, 1.5
multipliers = [regular, splatfest, closeout]
#need to make a thing for anarchy battle rules maybe

###################      0-2
multiplier = multipliers[0]
levelsNeededA = 78
####################
multiplierInt = 0

currentDirectory = os.getcwd() #print(currentDirectory)

multiplier = load(f"{currentDirectory}\stuff\\pickle\\multiplier.pkl")
levelsNeededA = load(f"{currentDirectory}\stuff\\pickle\\levelsNeededA.pkl")
if multiplier == multipliers[0]: multiplierInt = 0
if multiplier == multipliers[1]: multiplierInt = 1
if multiplier == multipliers[2]: multiplierInt = 2

#with open(f"stuff\\pickle\\multiplier.pkl", "wb") as p: pickle.dump(multiplier, file=p),     p.close()
#with open(f"stuff\\pickle\\levelsNeededA.pkl", "wb") as p: pickle.dump(levelsNeededA, file=p),     p.close()

levelsNeeded = 100-levelsNeededA

roundsUp=False
baseChance = False
baseChance = load(f"{currentDirectory}\stuff\\pickle\\baseChance.pkl")
#with open(f"stuff\\pickle\\baseChance.pkl", "wb") as p: pickle.dump(baseChance, file=p),     p.close()


WINDOWSIZEX = 498+40
WINDOWSIZEY = 606+40
WINDOWSIZE = (WINDOWSIZEX, WINDOWSIZEY)
FPS = 60
Title = f"S3 Catalog Display {version}"
tkTitle = f"S3 Turf Rounds Log"
extraX = 20
extraY = 20
LEFT = 1
RIGHT = 3

def terminate():
    pygame.quit()
    sys.exit()

pygame.init()
pygame.mixer.init()
WindowSurface = pygame.display.set_mode(WINDOWSIZE)
GreenSurface = WindowSurface.subsurface((44, 172, 268+extraX, 50+extraY))
PinkSurface = WindowSurface.subsurface((327, 172, 119+extraX, 50+extraY))
BOSurface = WindowSurface.subsurface((180, 250, 255+extraX, 46+extraY))

icon = pygame.image.load(rf'S3CD.png').convert_alpha()
icon = pygame.transform.scale(icon,(32,32))
pygame.display.set_icon(icon)
pygame.display.set_icon(icon)
pygame.display.set_caption(Title)
mainClock = pygame.time.Clock()
#pygame.mouse.set_visible(False)

def drawText(text, textcolour, surface, x, y, Mx=WINDOWSIZEX, My=WINDOWSIZEY, centerBool=True, centerCords=None, fontSize = 49):
    font = pygame.font.Font('stuff\paintball_beta_2.ttf', fontSize)
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

imageDirectory = f"{currentDirectory}\stuff"
def getDirectoryImageList(directory):#directory. list = return list
    directoryList = []
    print(directory)
    for object in sorted(os.listdir(str(directory)), key=len): 
        if ".png" in object:
            directoryList.append(pygame.image.load(f"{directory}\\{str(object)}").convert_alpha())
    return directoryList

levelImages = getDirectoryImageList(f"{imageDirectory}")

class imageObject(pygame.sprite.Sprite):
    def __init__(self, image, x=0, y=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x, self.y = x, y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.sizex, self.sizey = self.image.get_width(), self.image.get_height()

    def moveRight(self):
        self.rect.x += 1
        if self.rect.x >= self.x+self.sizex/2: self.rect.x = self.x

    def moveLeft(self):
        self.rect.x -= 1
        if self.rect.x <= self.x-self.sizex/2: self.rect.x = self.x

    def moveUp(self):
        self.rect.y -= 1
        if self.rect.y <= self.y-self.sizey/2: self.rect.y = self.y
    def moveDown(self):
        self.rect.y += 1
        if self.rect.y >= self.y+self.sizey/2: self.rect.y = self.y

image_List = pygame.sprite.Group()
darkGreen_List = pygame.sprite.Group()
lightGreen_List = pygame.sprite.Group()
darkPink_List = pygame.sprite.Group()
lightPink_List = pygame.sprite.Group()
bo_List = pygame.sprite.Group()

mainImage = imageObject(levelImages[0], x=0+extraX, y=0+extraY)
image_List.add(mainImage)


flip1 = pygame.transform.flip(levelImages[1], True, False) 
flip2 = pygame.transform.flip(levelImages[2], True, False) 
scale1 = pygame.transform.scale(levelImages[1], (1124/1.2,57))
scale2 = pygame.transform.scale(levelImages[2], (994/1.2,75)) 
scale3 = pygame.transform.scale(levelImages[1], (1124/1.5,57)) 
scale4 = pygame.transform.scale(levelImages[2], (994/1.5,75)) 
flip3 = pygame.transform.flip(scale1, True, False)
flip4 = pygame.transform.flip(scale2, True, False)
darkGreenGroup = [levelImages[1],flip1,flip3,scale1,scale3]
lightGreenGroup = [levelImages[2],flip2,flip4,scale2,scale4]
greenLeft = []
greenRight = []

for object in darkGreenGroup:
    objectA = imageObject(object, x=0, y=25+random.randint(-10,10))
    objectB = imageObject(object, x=-object.get_width()/2, y=25+random.randint(-10,10))
    darkGreen_List.add(objectA)
    darkGreen_List.add(objectB)
    greenLeft.append(objectA)
    greenRight.append(objectB)
    
for object in lightGreenGroup:
    objectA = imageObject(object, x=0, y=10+random.randint(-10,10))
    objectB = imageObject(object, x=-object.get_width()/2, y=10+random.randint(-10,10))
    lightGreen_List.add(objectA)
    lightGreen_List.add(objectB)
    greenLeft.append(objectA)
    greenRight.append(objectB)

greenDots = imageObject(levelImages[5], x=0, y=0)
darkGreen_List.add(greenDots)
darkPink = imageObject(levelImages[4], x=0, y=0)#-172/2
lightPink = imageObject(levelImages[3], x=0, y=-10)#-300/2
darkPink_List.add(darkPink)
lightPink_List.add(lightPink)

boObject = imageObject(levelImages[6], x=0, y=0)
bo_List.add(boObject)

tick = 0
down = 0

def getStats(loops=50, levelsNeeded=levelsNeeded, multiplier=multiplier, roundsUp=False, baseChance=True):
    global percentList, calculateList
    calculateList = []
    calculateHours = []
    closestList = []
    calculateRounds = []
    evenCloserList = []
    maxHours = 0#print(calculate(True, levelsNeeded, multiplier), percentValues(percentList))
    for i in range(loops):
        if baseChance == True: calculateList.append(calculate(True, levelsNeeded, multiplier))
        else: calculateList.append(calculate(True, levelsNeeded, multiplier, chance=percentList2))#percentValues(percentList)
    for object in calculateList:
        calculateHours.append(object[2])
    average = sum(calculateHours) / len(calculateHours)
    closest = min(calculateHours, key=lambda x:abs(x-average))
    for object in calculateList:
        if object[2] == closest: closestList.append(object)

    if roundsUp == True:
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
    W, L, D = 0, 0, 0
    for object in percentList:
        if object == "W": W += 1
        if object == "L": L += 1
        if object == "D": D += 1
    return [W, L, D]

percentList = []
for i in range(42):#42-60
    percentList.append("W")
for i in range(42):#42-30
    percentList.append("L")
for i in range(16):#16-10
    percentList.append("D")

percentList = load(f"{currentDirectory}\stuff\\pickle\\percentList.pkl")
with open(f"stuff\\pickle\\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p),     p.close()

percentListX = percentList.copy()
random.shuffle(percentListX)
percentList2 = percentValues(percentList)




def makeRound(type):
    global percentList, percentListX, percentList2, lastType
    percentList.append(type)
    lastType = type
    while True:
        if len(percentList) > 100: percentList.pop(0)
        else: break

    percentListX = percentList.copy()
    percentList2 = percentValues(percentList)
    with open(f"stuff\\pickle\\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p),     p.close()
    tkMake()

def forceRound(type):
    global percentList, percentListX, percentList2, lastType, lastLastType
    percentListX = percentList.copy()
    i=0
    broken=False
    for object in percentListX:
        if not object == type and not object == lastType:
            if not percentList[i] == type and not percentList[i] == lastType:
                percentList[i] = type
                broken=True
                break
        i += 1
    i=0
    if broken == False:
        for object in percentListX:
            if not object == type and not percentList[i] == type:
                print(f"{percentList[i]} -> {type}")
                percentList[i] = type
                broken=True
                break
            i += 1
    #if not lastLastType == type: lastLastType
    while True:
        if len(percentList) > 100: percentList.pop(0)
        else: break

    percentListX = percentList.copy()
    percentList2 = percentValues(percentList)
    with open(f"stuff\\pickle\\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p),     p.close()
    tkMake()

def multiplierButton():
    global multiplierInt, multiplier, multipliers
    multiplierInt += 1
    if multiplierInt > len(multipliers)-1: multiplierInt = 0
    multiplier = multipliers[multiplierInt]
    with open(f"stuff\\pickle\\multiplier.pkl", "wb") as p: pickle.dump(multiplier, file=p),     p.close()

def baseChanceButton():
    global baseChance
    if baseChance == True: baseChance = False
    elif baseChance == False: baseChance = True
    tkMake()
    with open(f"stuff\\pickle\\baseChance.pkl", "wb") as p: pickle.dump(baseChance, file=p),     p.close()

def averageButton():
    global roundsUp
    if roundsUp == True: roundsUp = False
    else: roundsUp = True
    tkMake()

def level(value):
    global levelsNeededA
    print(levelsNeededA)
    levelsNeededA += value
    if levelsNeededA > 100: levelsNeededA = 1
    if levelsNeededA < 1: levelsNeededA = 100
    levelsNeeded = 100-levelsNeededA
    with open(f"stuff\\pickle\\levelsNeededA.pkl", "wb") as p: pickle.dump(levelsNeededA, file=p),     p.close()

def rotateRoundId(pos,id):
    global percentList, percentList2
    if pos == "W": percentList[id] = "L"
    elif pos == "L": percentList[id] = "D"
    elif pos == "D": percentList[id] = "W"
    percentList2 = percentValues(percentList)
    with open(f"stuff\\pickle\\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p),     p.close()
    tkMake()

lastType = "W"
lastLastType = "W"

##### for new window
MainWindow = tkinter.Tk(className=tkTitle)
#MainWindow.iconbitmap("S3CD.ico")

img = tkinter.PhotoImage(file="S3CD.ico")
MainWindow.tk.call('wm', 'iconphoto', MainWindow._w, img)

MainWindow.geometry(str(WINDOWSIZEX) + "x" + str(WINDOWSIZEY+30))
MainWindow['background']='#262626'

ButtonImages = [tkinter.PhotoImage(file="stuff\\10.png"), tkinter.PhotoImage(file="stuff\\11.png"), tkinter.PhotoImage(file="stuff\\12.png")]
ButtonImages2 = [tkinter.PhotoImage(file="stuff\\13.png"), tkinter.PhotoImage(file="stuff\\14.png"), tkinter.PhotoImage(file="stuff\\12.png")]
roundImages = [tkinter.PhotoImage(file="stuff\\7.png"), tkinter.PhotoImage(file="stuff\\8.png"), tkinter.PhotoImage(file="stuff\\9.png")]
ButtonImages3 = [tkinter.PhotoImage(file="stuff\\15.png"), tkinter.PhotoImage(file="stuff\\16.png"), tkinter.PhotoImage(file="stuff\\17.png"), tkinter.PhotoImage(file="stuff\\18.png")]
GreyButtonImages = [tkinter.PhotoImage(file="stuff\\19.png"), tkinter.PhotoImage(file="stuff\\20.png")]
Tkfont = Font(size=16, weight=BOLD)

label1= tkinter.Label(MainWindow, text=f"{percentList2[0]}", font=Tkfont, fg='white', bg='#262626')
label1.place(x=285,y=20)
label2= tkinter.Label(MainWindow, text=f"{percentList2[1]}", font=Tkfont, fg='white', bg='#262626')
label2.place(x=385,y=20)
label3= tkinter.Label(MainWindow, text=f"{percentList2[2]}", font=Tkfont, fg='white', bg='#262626')
label3.place(x=485,y=20)

tkinter.Button(MainWindow, command=lambda: makeRound("W"), height=50, width=50, bg="grey", image=ButtonImages[0]).place(x=0,y=0)
tkinter.Button(MainWindow, command=lambda: makeRound("L"), height=50, width=50, bg="grey", image=ButtonImages[1]).place(x=60,y=0)
tkinter.Button(MainWindow, command=lambda: makeRound("D"), height=50, width=50, bg="grey", image=ButtonImages[2]).place(x=120,y=0)

tkinter.Button(MainWindow, command=lambda: forceRound("W"), height=50, width=50, bg="grey", image=ButtonImages2[0]).place(x=230,y=0)
tkinter.Button(MainWindow, command=lambda: forceRound("L"), height=50, width=50, bg="grey", image=ButtonImages2[1]).place(x=330,y=0)
tkinter.Button(MainWindow, command=lambda: forceRound("D"), height=50, width=50, bg="grey", image=ButtonImages2[2]).place(x=430,y=0)

#button = tkinter.Button(MainWindow, height=50, width=50, bg="grey", image=ButtonImages3[3])
#button.place(x=0,y=WINDOWSIZEY-26)
tkinter.Button(MainWindow, command=multiplierButton, height=50, width=50, bg="grey", image=ButtonImages3[0]).place(x=60,y=WINDOWSIZEY-26)

if roundsUp == True: button1Image = ButtonImages3[1]
elif roundsUp == False: button1Image = GreyButtonImages[0]
if baseChance == True: button2Image = GreyButtonImages[1]
elif baseChance == False: button2Image = ButtonImages3[2]

button1 = tkinter.Button(MainWindow, command=averageButton, height=50, width=50, bg="grey", image=button1Image)
button1.place(x=120,y=WINDOWSIZEY-26)
button2 = tkinter.Button(MainWindow, command=baseChanceButton, height=50, width=50, bg="grey", image=button2Image)
button2.place(x=180,y=WINDOWSIZEY-26)

tkframe = tkinter.Frame(MainWindow, width=WINDOWSIZEX, height=9*60)
tkframe['background']='#262626'
tkframe.place(x=0,y=70)


class roundbutton():
    def __init__(self, id, y, image):
        self.id = id
        tkinter.Button(tkframe, command=lambda: self.command(), width=WINDOWSIZEX-30, height=50, bg="grey", image=image).place(x=10,y=(y*60))
    def command(self):
        rotateRoundId(percentList[self.id],self.id)

def tkMake():
    global label1, label2, label3, button1, button2
    global roundsUp, baseChance, percentList, idList
    for widgets in tkframe.winfo_children():
        widgets.destroy()
    label1.destroy()
    label2.destroy()
    label3.destroy()
    label1= tkinter.Label(MainWindow, text=f"{percentList2[0]}", font=Tkfont, fg='white', bg='#262626')
    label1.place(x=285,y=20)
    label2= tkinter.Label(MainWindow, text=f"{percentList2[1]}", font=Tkfont, fg='white', bg='#262626')
    label2.place(x=385,y=20)
    label3= tkinter.Label(MainWindow, text=f"{percentList2[2]}", font=Tkfont, fg='white', bg='#262626')
    label3.place(x=485,y=20)

    button1.destroy()
    button2.destroy()
    if roundsUp == True: button1Image = ButtonImages3[1]
    elif roundsUp == False: button1Image = GreyButtonImages[0]
    if baseChance == True: button2Image = ButtonImages3[2]
    elif baseChance == False: button2Image = GreyButtonImages[1]

    button1 = tkinter.Button(MainWindow, command=averageButton, height=50, width=50, bg="grey", image=button1Image)
    button1.place(x=120,y=WINDOWSIZEY-26)
    button2 = tkinter.Button(MainWindow, command=baseChanceButton, height=50, width=50, bg="grey", image=button2Image)
    button2.place(x=180,y=WINDOWSIZEY-26)
    idList = []
    for i in range(9):
        id=len(percentList)-1-i
        if percentList[id] == "W": image = roundImages[0]
        if percentList[id] == "L": image = roundImages[1]
        if percentList[id] == "D": image = roundImages[2]
        roundbutton(id,i, image)#tkinter.Button(tkframe, command=lambda: rotateRoundId(percentList[id],i), width=WINDOWSIZEX-30, height=50, bg="grey", image=image).place(x=10,y=(i*60))

tkMake()
tkframe.update()
MainWindow.update()
roundSwitch = True

statsObject = getStats(50, levelsNeeded, multiplier)
#print(statsObject)

resetSwitches = [0,0,0]
while True:
    tick += 1
    mainClock.tick(FPS)
    
    if tick % 2 == 0:
        WindowSurface.fill((0,255,0))
        bo_List.draw(BOSurface)
        PinkSurface.fill((191,0,255))
        GreenSurface.fill((90,255,90))
        lightPink_List.draw(PinkSurface)
        darkPink_List.draw(PinkSurface)

        lightGreen_List.draw(GreenSurface)
        darkGreen_List.draw(GreenSurface)
        image_List.draw(WindowSurface)
        drawText(f"{levelsNeededA}", (255,255,255), WindowSurface, 220+extraX, 113+extraY, centerCords=(276, 141+extraY))

        drawText(f"{statsObject[1]}", (255,255,255), GreenSurface, 0, 0, centerCords=(268/2, 23))
        drawText(f"x{statsObject[7]*1.0}", (255,255,255), PinkSurface, 342+extraX, 168+extraY, centerCords=(119/2, 23))

        drawText(f"{statsObject[2]} Hours", (255,255,255), BOSurface, 187+extraX, 223+extraY, centerCords=(255/2, 20))

        drawText(f"{statsObject[3]}", (255,255,255), WindowSurface, 100+extraX, 278+extraY, centerCords=(335/2, 306+extraY))#+28y

        if baseChance == False:
            drawText(f"{percentList2[0]}", (255,255,255), WindowSurface, 42+extraX, 354+extraY, centerCords=(60+extraX, 366+extraY), fontSize=25)
            drawText(f"{percentList2[1]}", (255,255,255), WindowSurface, 416+extraX, 354+extraY, centerCords=(436+extraX, 366+extraY), fontSize=25)
            drawText(f"{percentList2[2]}", (255,255,255), WindowSurface, 56+extraX, 515+extraY, centerCords=(76+extraX, 528+extraY), fontSize=25)

        drawText(f"{statsObject[4]}", (255,255,255), WindowSurface, 103+extraX, 388+extraY, centerCords=(155, 416+extraY))
        drawText(f"{statsObject[5]}", (255,255,255), WindowSurface, 290+extraX, 388+extraY, centerCords=(344, 416+extraY))

        drawText(f"{statsObject[6]}", (255,255,255), WindowSurface, 212+extraX, 440+extraY, centerCords=(244+extraX, 468+extraY))

    pygame.display.update()
    if roundSwitch == True:
        try:
            tkframe.update()
            MainWindow.update()
        except:
            if not roundSwitch == False:
                roundSwitch = False
                MainWindow.quit()
    pygame.display.set_caption(f"{Title} | FPS: {int(mainClock.get_fps())}")

    GreenSurface = WindowSurface.subsurface((44+extraX, 172+extraY, 268, 50))
    PinkSurface = WindowSurface.subsurface((327+extraX, 172+extraY, 119, 50))
    BOSurface = WindowSurface.subsurface((160+extraX, 230+extraY, 255, 46))
    mainImage.rect.y = 0+extraY
    if tick % 2 == 0:
        if tick % 4 == 0:
            lightPink.moveUp()
            darkPink.moveLeft()
            greenDots.moveLeft()
        if tick % 5 == 0:
            if down < 2: extraY += 1
            elif down > 3: extraY -= 1

        darkPink.moveUp()
        lightPink.moveLeft()
        boObject.moveUp()

        for object in greenLeft:
            object.moveLeft()
        for object in greenRight:
            object.moveRight()
    #try:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: terminate()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:terminate()
            if event.key == ord("q"): resetSwitches[0] = 1
            if event.key == ord("w"): resetSwitches[1] = 1
            if event.key == ord("e"): resetSwitches[2] = 1
            #if event.key == ord("l"):
            #    if roundSwitch == True:
            #        roundSwitch = False
            #        MainWindow.quit()
            #    elif roundSwitch == False:
            #        roundSwitch = True
            #        tkMake()
            #        tkframe.update()#roundWindow()
            if event.key == ord("p"):
                if baseChance == True: baseChance = False
                elif baseChance == False: baseChance = True
                with open(f"stuff\\pickle\\baseChance.pkl", "wb") as p: pickle.dump(baseChance, file=p),     p.close()
            if event.key == ord("m"):
                multiplierInt += 1
                if multiplierInt > len(multipliers)-1: multiplierInt = 0
                multiplier = multipliers[multiplierInt]
                with open(f"stuff\\pickle\\multiplier.pkl", "wb") as p: pickle.dump(multiplier, file=p),     p.close()
            if event.key == ord("n"):
                if roundsUp == True: roundsUp = False
                else: roundsUp = True
        if event.type == pygame.KEYUP:
            if event.key == ord("q"): resetSwitches[0] = 0
            if event.key == ord("w"): resetSwitches[1] = 0
            if event.key == ord("e"): resetSwitches[2] = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT:
                levelsNeededA += 1
                if levelsNeededA > 100: levelsNeededA = 1
            if event.button == RIGHT:
                levelsNeededA -= 1
                if levelsNeededA < 1: levelsNeededA = 100
            levelsNeeded = 100-levelsNeededA
            with open(f"stuff\\pickle\\levelsNeededA.pkl", "wb") as p: pickle.dump(levelsNeededA, file=p),     p.close()
    if resetSwitches == [1,1,1]:
        resetSwitches = [0,0,0]
        if len(percentList) > 10:
            for i in range(len(percentList)-10):
                percentList.pop(0)
                percentList2 = percentValues(percentList)
                with open(f"stuff\\pickle\\percentList.pkl", "wb") as p: pickle.dump(percentList, file=p),     p.close()
    #except: pass #invaled key
    if tick == 60:
        statsObject = getStats(1, levelsNeeded, multiplier, roundsUp, baseChance)
        goal = random.randint(1,200)
        tick = 0
        down += 1
        if down == 6: down = 0