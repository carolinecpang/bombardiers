#################################################
# Bombardiers.py
#
# Your name: Caroline Pang
# Your andrew id: carolinp
#################################################
import math, copy, random
import sys
from cmu_112_graphics import *
from tkinter import *
from PIL import Image
 
class SplashScreenMode(Mode):
    def keyPressed(mode, event):
        mode.app.setActiveMode(mode.app.levelSelectMode)

    def redrawAll(mode, canvas):
        w, h = mode.width, mode.height
        canvas.create_image(w//2, h//2, image=ImageTk.PhotoImage(mode.app.bg))
        titleFont = "Arial 38 italic bold"
        canvas.create_text(mode.width//2-2, mode.height//2-2,\
            text="Welcome to Bombardiers", fill="goldenrod1", font=titleFont)
        canvas.create_text(mode.width//2-1, mode.height//2-1,\
            text="Welcome to Bombardiers", fill="goldenrod1", font=titleFont)
        canvas.create_text(mode.width//2, mode.height//2,\
            text="Welcome to Bombardiers", fill="white", font=titleFont)
        smallFont = "Arial 24 italic bold"
        canvas.create_text(mode.width//2, mode.height//2+50,\
            text="press any key to start", fill="white", font=smallFont)
 
class LevelSelectMode(Mode):
    def appStarted(mode):
        mode.margin = 30
        mode.cellHeight = mode.width//5
        # Level data
        mode.numLevels = 5
        mode.levelSelection = -1
        mode.levelHeight = mode.height*(1/3)
        # Game data
        mode.numGameModes = 3
        mode.gameModeSelection = -1
        mode.gameModeHeight = mode.height*(2/3)
        mode.gameModeNames = ["single player", 
                              "multiplayer",
                              "multiplayer + planets"]
        mode.gameModes = [mode.app.singlePlayerMode, 
                          mode.app.gameMode,
                          mode.app.multiplayerPlanetGameMode]
 
    def pointInGrid(mode, x, y):
        h = mode.cellHeight//2
        if (mode.margin <= x <= mode.width-mode.margin):
            if (mode.levelHeight-h <= y <= mode.levelHeight+h):
                return "levels"
            elif (mode.gameModeHeight-h <= y <= mode.gameModeHeight+h):
                return "game modes"
        return None
 
    def getCell(mode, x, y):
        # Returns cell and grid that x, y belongs to
        gridType = LevelSelectMode.pointInGrid(mode, x, y)
        if gridType == "levels":
            numCells = mode.numLevels
        elif gridType == "game modes":
            numCells = mode.numGameModes
        else:
            return (-1, -1)
        gridWidth  = mode.width - 2*mode.margin
        cellWidth  = gridWidth / numCells
        index = int((x - mode.margin) / cellWidth)
        return (gridType, index)
 
    def getCellBounds(mode, col, height, numCells):
        # Returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
        gridWidth  = mode.width - 2*mode.margin
        columnWidth = gridWidth / numCells
        rowHeight = mode.cellHeight
        x0 = mode.margin + col * columnWidth
        x1 = mode.margin + (col+1) * columnWidth
        y0 = height - mode.cellHeight//2
        y1 = height + mode.cellHeight//2
        return (x0, y0, x1, y1)
 
    def mousePressed(mode, event):
        gridType, index = LevelSelectMode.getCell(mode, event.x, event.y)
        # Select this col unless it is selected
        if gridType == "levels":
            if (mode.levelSelection == index):
                mode.levelSelection = -1
            else:
                mode.levelSelection = index
        else:
            if (mode.gameModeSelection == index):
                mode.gameModeSelection = -1
            else:
                mode.gameModeSelection = index

    def keyPressed(mode, event):
        print("EVENT", event.key)
        if event.key == "Return" or event.key == "Enter":
            if mode.levelSelection != -1 and mode.gameModeSelection != -1:
                mode.app.setActiveMode(mode.app.gameRulesMode)
                mode.app.gameRulesMode.getSelectedGameMode()
 
    def drawGrid(mode, canvas, numCells, height):
        for cell in range(numCells):
            (x0, y0, x1, y1) = LevelSelectMode.getCellBounds(mode, cell,\
                height, numCells)
            if numCells == mode.numLevels:
                selection = mode.levelSelection
            else:
                selection = mode.gameModeSelection
            fill = "red" if (selection == cell) else "light blue"
            canvas.create_rectangle(x0, y0, x1, y1, fill=fill,\
                outline="white", width=3)
 
    def drawHeaders(mode, canvas):
        font = "Arial 34 italic bold"
        canvas.create_text(mode.width//2-1, mode.height*(1/6)-1,\
                            text="SELECT A LEVEL", font=font,fill="goldenrod1")
        canvas.create_text(mode.width//2-2, mode.height*(1/6)-2,\
                            text="SELECT A LEVEL", font=font,fill="goldenrod1")
        canvas.create_text(mode.width//2, mode.height*(1/6),\
                            text="SELECT A LEVEL", font=font,fill="white")
        font = "Arial 34 italic bold"
        canvas.create_text(mode.width//2-2, mode.height//2-2,\
                        text="SELECT GAME MODE", font=font, fill="goldenrod1")
        canvas.create_text(mode.width//2-1, mode.height//2-1,\
                        text="SELECT GAME MODE", font=font, fill="goldenrod1")
        canvas.create_text(mode.width//2, mode.height//2,\
                        text="SELECT GAME MODE", font=font,fill="white")

    def redrawAll(mode, canvas):
        w, h = mode.width, mode.height
        canvas.create_image(w//2, h//2, image=ImageTk.PhotoImage(mode.app.bg))
        canvas.create_rectangle(15, 15, w - 15, h - 15, fill=None,\
            outline="goldenrod1", width=3)
        # draw grid of cells
        LevelSelectMode.drawGrid(mode, canvas, mode.numLevels, mode.levelHeight)
        LevelSelectMode.drawGrid(mode, canvas, mode.numGameModes, mode.gameModeHeight)
        
        LevelSelectMode.drawHeaders(mode, canvas)
        font = "Arial 22 italic bold"
        if mode.levelSelection != -1:
            canvas.create_text(mode.margin, mode.height*(5/6)-15, anchor="nw",\
                    text=f"Level: {mode.levelSelection+1}",\
                    font=font, fill="white")

        if mode.gameModeSelection != -1:
            canvas.create_text(mode.margin, mode.height*(5/6)+15, anchor="nw",\
                    text=f"Mode: {mode.gameModeNames[mode.gameModeSelection]}",\
                    font=font, fill="white")
        if mode.levelSelection != -1 and mode.gameModeSelection != -1:
            canvas.create_text(mode.margin, mode.height*(5/6)+45,\
                    anchor="nw", text="Press \"Enter\" to continue",\
                    font=font, fill="white")

class GameRulesMode(Mode):
    def appStarted(mode):
        mode.gameModeDescriptions = []
        GameRulesMode.addDescriptions(mode)
        GameRulesMode.getSelectedGameMode(mode)

        mode.generalRules = '''
        Your Mission: Use missiles to destroy the player's forcefield
        on the other side.

        Use left and right arrow keys or click anywhere on the screen
        to set the missile angle.

        Use up and down arrow keys to adjust the missile strength.

        If your forcefield is hit, it becoomes damaged and you can no
        longer fire missiles from that angle.
        
        Press "c" to expedite the missile fired
        Press "r" to reset game
        Press "R" to return to level selction'''
    
    def getSelectedGameMode(mode):
        mode.gameModes = mode.app.levelSelectMode.gameModes
        mode.gameModeIndex = mode.app.levelSelectMode.gameModeSelection
        mode.selectedGameMode = mode.gameModes[mode.gameModeIndex]
        mode.description = mode.gameModeDescriptions[mode.gameModeIndex]

    def addDescriptions(mode):
        singlePlayerDescription = '''
        Single Player:
        Fire missiles to defeat the CPU!
        Please wait a few seconds...
        
        Press "Enter" to continue'''
        multiplayerDescription = '''
        Multiplayer:
        Play against a friend! Switch turns firing missiles at the other
        player!
        
        Press "Enter" to continue'''
        multiplayerPlanetDescription = '''
        Multiplayer + Planets
        The original rules with an added challenge! Each player can now
        place their own planets. After firing a missile, each player
        can place one planet, adding up to three additional planets.
        Press "enter" to complete turn.
        
        Press "Enter" to continue'''
        mode.gameModeDescriptions.append(singlePlayerDescription)
        mode.gameModeDescriptions.append(multiplayerDescription)
        mode.gameModeDescriptions.append(multiplayerPlanetDescription)

    def keyPressed(mode, event):
        if event.key == "Return" or event.key == "Enter":
            mode.app.setActiveMode(mode.selectedGameMode)

    def drawHeader(mode, canvas):
        font = "Arial 34 italic bold"
        canvas.create_text(mode.width//2-2, mode.height*(1/6)-2,\
                        text="GAME MODE RULES", font=font, fill="goldenrod1")
        canvas.create_text(mode.width//2-1, mode.height*(1/6)-1,\
                        text="GAME MODE RULES", font=font, fill="goldenrod1")
        canvas.create_text(mode.width//2, mode.height*(1/6),\
                        text="GAME MODE RULES", font=font,fill="white")

    def redrawAll(mode, canvas):
        w, h = mode.width, mode.height
        canvas.create_image(w//2, h//2, image=ImageTk.PhotoImage(mode.app.bg))
        canvas.create_text
        canvas.create_rectangle(15, 15, w - 15, h - 15, fill=None,\
            outline="goldenrod1", width=3)
        font = "Arial 16 italic bold"
        GameRulesMode.drawHeader(mode, canvas)
        canvas.create_text(10, h*(1/6)+20, anchor="nw",\
            text=mode.generalRules, font=font, fill="white")
        canvas.create_text(10, h*(3/5)+45, anchor="nw",\
            text=mode.description, font=font, fill="light blue")

class Missile(object):
    @staticmethod
    def distance(x1, y1, x2, y2):
        return ((x1-x2)**2 + (y1-y2)**2)**0.5
 
    def __init__(self, mode, cx, cy, vx, vy, mass):
        self.mode = mode
        self.cx = cx # x position
        self.cy = cy # y position
        self.vx = vx # x component of velocity
        self.vy = vy # y component of velocity
        self.mass = mass
 
        self.r = 5
 
        self.trace = [] # contains previous missile positions
        self.traceR = 3
        self.drawTrace = True
 
        self.dt = 1/15 # time between position updates
 
    def checkCollision(self):
        # collision with planet
        for planet in self.mode.planets:
            if (Missile.distance(self.cx, self.cy, planet.cx, planet.cy)\
               <= planet.r+self.r):
                return (True, False, self.cx, self.cy)
        # collition with current player force field
        if (Missile.distance(self.cx, self.cy, self.mode.width//2, 0)\
             < self.mode.activePlayer.hitRadius + self.r):
            self.mode.P2.healthDecrease(self)
            return (True, True, self.cx, self.cy)
        elif (Missile.distance(self.cx, self.cy, self.mode.width//2,\
            self.mode.height) < self.mode.activePlayer.hitRadius + self.r):
            self.mode.P1.healthDecrease(self)
            return (True, True, self.cx, self.cy)
        # collision with upper or lower boundary
        elif (self.cy < 0 or self.cy > self.mode.height):
            return (True, False, self.cx, self.cy)
        else:
            return (False, False, -1, -1)
    
    def move(self, player):
        if player.name == self.mode.P1.name:
            self.cx += self.vx * self.dt
            self.cy -= self.vy * self.dt
        else:
            self.cx += self.vx * self.dt
            self.cy += self.vy * self.dt
        collision,playerCollision,collisionX,collisionY = self.checkCollision()
        if collision:
            self.mode.activePlayer.prevMissileTrace = self.trace
            if playerCollision:
                if collisionY > self.mode.height//2:
                    print(self.mode.width//2, self.mode.height, collisionX,\
                        collisionY)
                    angle = 180 - int(math.degrees(self.angleFromObject(\
                        self.mode.width//2, self.mode.height, collisionX,\
                        collisionY)))
                    self.mode.P1.hitAngles.append(angle)
                    self.mode.P1.removePossibleAngles(angle)
                    print("P1 Angle",angle)
                else:
                    angle = 180-int(math.degrees(self.angleFromObject(\
                        self.mode.width//2, 0, collisionX, collisionY)))
                    print("P2 Angle",angle)
                    self.mode.P2.hitAngles.append(angle)
                    self.mode.P2.removePossibleAngles(angle)
            return False # player turn is over
        else:
            if self.drawTrace == True:
                self.trace.append((self.cx, self.cy))
                self.drawTrace = False
            else:
                self.drawTrace = True
            self.updateVelocity()
            return True # missile keeps moving
 
    def angleFromObject(self, selfX, selfY, otherX, otherY):
        if self.mode.activePlayer.name == self.mode.P1.name:
            yDistance = otherY - selfY
        else:
            yDistance = selfY - otherY
        xDistance = selfX - otherX
        if xDistance == 0:
            if yDistance > 0:
                angle = 90
            else:
                angle = 270
        elif yDistance == 0:
            if xDistance > 0:
                angle = 0
            else:
                angle = 180
        elif xDistance > 0:
                if yDistance > 0:
                    angle = math.atan(yDistance/xDistance)
                else:
                    angle = 2*math.pi + math.atan(yDistance/xDistance)
        else: # xDistance < 0
                angle = math.pi + math.atan(yDistance/xDistance)
        return angle
    
    def updateVelocity(self):
        self.netForceX = 0
        self.netForceY = 0
        for planet in self.mode.planets:
            r = Missile.distance(self.cx, self.cy, planet.cx, planet.cy)
            gConstant = 3000
            gravityF = gConstant*(((planet.r**2) * self.mass)/(r**2))
    
            angle = self.angleFromObject(self.cx, self.cy, planet.cx,\
                                            planet.cy)
            self.netForceX += gravityF*(math.cos(angle))
            self.netForceY += gravityF*(math.sin(angle))
        #print(self.netForceX, self.netForceY)
        # vf = vi + at
        self.vx -= (self.netForceX/self.mass)*self.dt
        self.vy -= (self.netForceY/self.mass)*self.dt
      
    def drawMissile(self, canvas):
        tR = self.traceR
        for elem in self.trace: # draws trace of missile
            cx, cy = elem
            canvas.create_oval(cx-tR, cy-tR, cx+tR, cy+tR, fill="red",\
                               outline="red")
            
        cx, cy, r = self.cx, self.cy, self.r
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="goldenrod1")
                    
class Planet(object):
    def __init__(self, cx, cy, r):
        self.cx = cx
        self.cy = cy
        self.r = r
    
    def drawPlanet(self, canvas):
        cx, cy, r = self.cx, self.cy, self.r
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="red")
 
class Player(object):
    fullHealth = 100
    hitRadius = 50
 
    def __init__(self, mode, name, startHeight):
        self.mode = mode
        self.name = name
        self.startHeight = startHeight
        self.score = 0
        self.health = Player.fullHealth
 
        self.missileFired = False
        self.missileAngle = 90 # from 10 to 170
        self.missileStrength = 50 # initial velocity scale from 1 to 100
        self.numPlanetsPlaced = 0
        self.cannonLength = 30
        self.prevMissileTrace = []
        self.availableAngles = set(range(10,  171))
        self.hitAngles = []
        
    def healthDecrease(self, missile):
        # damage depends on velocity of missile
        missileVelocity = (missile.vx**2 + missile.vy**2)**0.5
        self.health -= int(0.25*missileVelocity)

    def removePossibleAngles(self, angle):
        anglesToRemove = set(range(angle-4, angle+5))
        newAngles = set()
        for angle in self.availableAngles:
            if angle not in anglesToRemove:
                newAngles.add(angle)
        self.availableAngles = newAngles
 
    def mousePressed(self, mode, event):
        x, y = event.x, event.y
        if self.name == self.mode.P1.name:
            fraction = ((self.mode.height-y)/(x-self.mode.width//2))
        else:
            fraction = (y/(x-self.mode.width//2))
        if fraction < 0:
            angle = math.atan(fraction) + math.pi
        else:
            angle = math.atan(fraction)
        angle = int(math.degrees(angle))
        if angle > self.mode.maxAngle:
            angle = self.mode.maxAngle
        elif angle < self.mode.minAngle:
            angle = self.mode.minAngle
        self.missileAngle = angle
 
    def fireMissile(self):
        radMissileAngle = math.radians(self.missileAngle)
        if self.startHeight == 0:
            cx = self.mode.width//2 + 60*math.cos(radMissileAngle)
            cy = 60*math.sin(radMissileAngle)
        else:
            cx = self.mode.width//2 + 60*math.cos(radMissileAngle)
            cy = self.startHeight - 60*math.sin(radMissileAngle)
        
        vx = self.missileStrength * 3/2 * math.cos(radMissileAngle)
        vy = self.missileStrength * 3/2 * math.sin(radMissileAngle)
        mass = 10
        self.missile = Missile(self.mode, cx, cy, vx, vy, mass)
 
    def drawCannon(self, canvas):
        # forcefield
        playerX, playerY = self.mode.width//2, self.startHeight
        r = Player.hitRadius
        canvas.create_oval(playerX-r, playerY-r, playerX+r, playerY+r,
        fill=None, outline="light blue", width=5)
        for angle in self.hitAngles:
            if self.mode.activePlayer.name == self.mode.P2.name:
                startAngle = 360 - angle - 5
                extent = 10
            else:
                startAngle = angle - 5
                extent = 10
            canvas.create_arc(playerX-r, playerY-r, playerX+r, playerY+r,\
                start=startAngle, extent=extent, style=ARC, width=5, outline="red")
        
        # moving cannon
        radMissileAngle = math.radians(self.missileAngle)
        if self.startHeight == 0:
            x = self.mode.width//2 + self.cannonLength*math.cos(radMissileAngle)
            y = self.cannonLength*math.sin(radMissileAngle)
        else:
            x = self.mode.width//2 + self.cannonLength*math.cos(radMissileAngle)
            y = self.startHeight - self.cannonLength*math.sin(radMissileAngle)

        if self.missileAngle in self.availableAngles:
            fill = "white"
        else:
            fill = "red"
        canvas.create_line(self.mode.width//2, self.startHeight, x, y,\
             width=5, fill=fill)
        
        bodyr = 15
        canvas.create_oval(playerX-bodyr, playerY-bodyr, playerX+bodyr,\
            playerY+bodyr, fill="white", outline="white")

    def drawActiveCannon(self, canvas):  
        playerX, playerY = self.mode.width//2, self.startHeight
        r = Player.hitRadius -2
        canvas.create_oval(playerX-r, playerY-r, playerX+r, playerY+r,
        fill=None, outline="goldenrod1", width=10)
 
    def drawPrevMissileTrace(self, canvas):
        for elem in self.prevMissileTrace:
            cx, cy = elem
            tR = 3
            canvas.create_oval(cx-tR, cy-tR, cx+tR, cy+tR, fill="light blue",\
                               outline="light blue")
 
    def drawPlayerStats(self, canvas):
        if self.name == self.mode.P1.name:
            y = self.startHeight - 80
        else:
            y = 10
        font = "Arial 20 italic bold"
        canvas.create_text(20, y, anchor="nw",\
                           text=f'angle: {self.missileAngle}°',\
                           fill="white", font=font)
        canvas.create_text(20, y+20, anchor="nw",\
                           text=f'strength: {self.missileStrength}',\
                           fill="white", font=font)
        canvas.create_text(20, y+40, anchor="nw", text=f'health: {self.health}',\
                           fill="red", font=font)
     
class GameMode(Mode):
    def appStarted(mode):
        mode.minAngle, mode.maxAngle = 30, 150
        mode.minStrength, mode.maxStrength = 20, 100
        mode.levels = []
        GameMode.addLevels(mode)
        GameMode.setupGame(mode)
        mode.mouseWasMoved = False
        mode.maxPlanets = 3
    
    def addLevels(mode):
        x, y = mode.width//2, mode.height//2
        level0 = [(x, y, 10)]
        level1 = [(x, y, 10), (x-150, y, 15), (x+150, y, 15)]
        level2 = [(x, y-100, 10), (x, y+100, 10)]
        level3 = [(x-50, y, 5), (x+50, y, 5), (x, y+50, 5), (x, y-50, 5)]
        # add random positions and label level Selection
        level4 = []
        numPlanetsRange = list(range(1, 6))
        numPlanets = random.choice(numPlanetsRange)
        radii = [5, 10, 15, 20]
        xpositions = list(range(50, mode.width-50, 5))
        ypositions = list(range(100, mode.height-100, 5))
        planetsAdded = 0
        while planetsAdded < numPlanets:
            x, y = random.choice(xpositions), random.choice(ypositions)
            radius = random.choice(radii)
            for r in radii:
                if (x, y, r) in level4:
                    continue
            level4.append((x, y, radius))
            planetsAdded += 1
        mode.levels.append(level0)
        mode.levels.append(level1)
        mode.levels.append(level2)
        mode.levels.append(level3)
        mode.levels.append(level4)
    
    def setupGame(mode):
        mode.planets = []
        GameMode.addPlanets(mode)
        mode.P1 = Player(mode, "Player 1", mode.height)
        mode.P2 = Player(mode, "Player 2", 0)
        mode.activePlayer = mode.P1
        mode.inactivePlayer = mode.P2
        mode.gameOver = False
        mode.missileMode = True
 
    def addPlanets(mode): 
        level = mode.app.levelSelectMode.levelSelection
        for (cx, cy, r) in mode.levels[level]:
            newPlanet = Planet(cx, cy, r)
            mode.planets.append(newPlanet)
    
    def switchPlayer(mode):
        mode.missileMode = True
        if mode.activePlayer == mode.P1:
            mode.activePlayer = mode.P2
            mode.inactivePlayer = mode.P1
        else: 
            mode.activePlayer = mode.P1
            mode.inactivePlayer = mode.P2
 
    def keyPressed(mode, event):
        if (mode.missileMode == True\
             and mode.activePlayer.missileFired == False\
                 and mode.gameOver == False):
            if event.key == "Right":
                if mode.activePlayer.missileAngle > mode.minAngle:
                    mode.activePlayer.missileAngle -= 1
            elif event.key == "Left":
                if mode.activePlayer.missileAngle < mode.maxAngle:
                    mode.activePlayer.missileAngle += 1
            elif event.key == "Up":
                if mode.activePlayer.missileStrength < mode.maxStrength:
                    mode.activePlayer.missileStrength += 1
            elif event.key == "Down":
                if mode.activePlayer.missileStrength > mode.minStrength:
                    mode.activePlayer.missileStrength -= 1
            elif event.key == "Space":
                if (mode.activePlayer.missileAngle in\
                    mode.activePlayer.availableAngles):
                    mode.activePlayer.fireMissile()
                    mode.activePlayer.missileFired = True
        elif event.key == "c":
            GameMode.completeMove(mode)
        if event.key == "r":
            GameMode.setupGame(mode)
        elif event.key == "R": #shift R
            mode.app.setActiveMode(mode.app.levelSelectMode)
 
    def mousePressed(mode, event):
        mode.startY = event.y
        if mode.missileMode == True:
            mode.activePlayer.mousePressed(mode, event)

    def completeMove(mode):
        while mode.activePlayer.missile.move(mode.activePlayer):
            continue
 
    def timerFired(mode):
        if mode.activePlayer.missileFired == True:
            # if missile collision
            # colX, colY, vxF, vyF, crashed = mode.activePlayer.missile.move(mode.activePlayer)
            if mode.activePlayer.missile.move(mode.activePlayer) == False:
                mode.activePlayer.missileFired = False
                GameMode.switchPlayer(mode)
                if mode.inactivePlayer.health <= 0 or\
                     mode.activePlayer.health <= 0:
                    mode.gameOver = True

    def drawGameOver(mode, canvas):
        w, h = mode.width, mode.height
        margin = 30
        canvas.create_rectangle(margin, h//2-h//4, w-margin, h//2+h//4,\
                fill="black")
        canvas.create_rectangle(margin+15, h//2-h//4+15, w-margin-15,\
                h//2+h//4-15, fill=None, outline="goldenrod1", width=3)
        canvas.create_text(w//2, h//2-40,\
                text="GAME OVER", font="Arial 38 italic bold", fill="white")
        if mode.P1.health <= 0:
            winningPlayer = mode.P2
        else:
            winningPlayer = mode.P1
        font = "Arial 18 italic bold"
        canvas.create_text(w//2, h//2, text=f"{winningPlayer.name} Wins!",
        font="Arial 24 italic bold", fill="white")
        canvas.create_text(w//2-20, h//2+30, font=font, fill="white",\
            text='''
            Press "r" to reset game
            Press "R" to return to level selection''')

    def redrawAll(mode, canvas): 
        w, h = mode.width, mode.height
        canvas.create_image(w//2, h//2, image=ImageTk.PhotoImage(mode.app.bg))
        for planet in mode.planets:
            planet.drawPlanet(canvas)
        mode.activePlayer.drawPrevMissileTrace(canvas)
        mode.activePlayer.drawPlayerStats(canvas)
        mode.inactivePlayer.drawPlayerStats(canvas)
        if mode.activePlayer.missileFired == True:
           mode.activePlayer.missile.drawMissile(canvas)
        mode.activePlayer.drawActiveCannon(canvas)
        mode.activePlayer.drawCannon(canvas) 
        mode.inactivePlayer.drawCannon(canvas)
        if mode.gameOver:
            GameMode.drawGameOver(mode, canvas)

        #testing angles
        #canvas.create_line(mode.x, mode.y, mode.planets[0].cx, mode.planets[0].cy)
 
class MultiplayerPlanetGameMode(GameMode):
    def appStarted(mode):
        super().appStarted()

    def mousePressed(mode, event):
        mode.startY = event.y
        if mode.missileMode == True:
            mode.activePlayer.mousePressed(mode, event)
        else:
            mode.planets.append(Planet(event.x, event.y, 10))
            GameMode.switchPlayer(mode)
 
    def mouseMoved(mode, event):
        mode.mouseWasMoved = True
        mode.planetX, mode.planetY = event.x, event.y
        mode.endY = event.y
    
    def keyPressed(mode, event):
        if (mode.missileMode == True\
             and mode.activePlayer.missileFired == False):
            if event.key == "Right":
                if mode.activePlayer.missileAngle > mode.minAngle:
                    mode.activePlayer.missileAngle -= 1
            elif event.key == "Left":
                if mode.activePlayer.missileAngle < mode.maxAngle:
                    mode.activePlayer.missileAngle += 1
            elif event.key == "Up":
                if mode.activePlayer.missileStrength < mode.maxStrength:
                    mode.activePlayer.missileStrength += 1
            elif event.key == "Down":
                if mode.activePlayer.missileStrength > mode.minStrength:
                    mode.activePlayer.missileStrength -= 1
            elif event.key == "Space":
                if (mode.activePlayer.missileAngle in\
                     mode.activePlayer.availableAngles):
                    mode.activePlayer.fireMissile()
                    mode.activePlayer.missileFired = True
        elif (mode.missileMode == False): 
            if event.key == "Enter":
                GameMode.switchPlayer(mode)
        elif event.key == "c":
            GameMode.completeMove(mode)
        
        if event.key == "r":
            GameMode.setupGame(mode)
        elif event.key == "R": #shift R
            mode.app.setActiveMode(mode.app.levelSelectMode)
    
    def timerFired(mode):
        if mode.activePlayer.missileFired == True:
            # if missile collision
            # colX, colY, vxF, vyF, crashed = mode.activePlayer.missile.move(mode.activePlayer)
            if mode.activePlayer.missile.move(mode.activePlayer) == False:
                mode.missileMode = False
                mode.activePlayer.missileFired = False
                if mode.inactivePlayer.health <= 0:
                    mode.gameOver = True
                elif mode.activePlayer.numPlanetsPlaced > mode.maxPlanets:
                    GameMode.switchPlayer(mode)

    def redrawAll(mode, canvas):
        super().redrawAll(canvas)
        if (mode.missileMode == False):
            r = 10
            if mode.mouseWasMoved == False:
                mode.planetX, mode.planetY = mode.width//2, mode.height//2
            canvas.create_oval(mode.planetX-r, mode.planetY-r,\
                mode.planetX+r, mode.planetY+r, fill="red")  
'''
# minimax algorithm structure adapted from stackabuse tic-tac-toe implementation
class State(object):
    def __init__(self, P1Health, P2Health, P1Angles, P2Angles):
        self.P1Health = P1Health
        self.P2Health = P2Health
        self.P1Angles = P1Angles
        self.P2Angles = P2Angles
    def __repr__(self):
        return str(P1Health)+str(P2Health)
'''

class SinglePlayerMode(GameMode):
    def appStarted(mode):
        super().appStarted()
        mode.P1Damages = SinglePlayerMode.calculateAngleDamages(mode, mode.P1,\
            mode.P2)
        mode.P2Damages = SinglePlayerMode.calculateAngleDamages(mode, mode.P2,\
            mode.P1)
        mode.moves = []

    def getMissile(mode, angle, strength, player):
        radMissileAngle = math.radians(angle)
        if player.startHeight == 0:
            cx = mode.width//2 + 60*math.cos(radMissileAngle)
            cy = 60*math.sin(radMissileAngle)
        else:
            cx = mode.width//2 + 60*math.cos(radMissileAngle)
            cy = player.startHeight - 60*math.sin(radMissileAngle)
        vx = strength * 3/2 * math.cos(radMissileAngle)
        vy = strength * 3/2 * math.sin(radMissileAngle)
        mass = 10
        return Missile(mode, cx, cy, vx, vy, mass)
    
    def missileDamage(missile):
        missileVelocity = (missile.vx**2 + missile.vy**2)**0.5
        return 0.25*missileVelocity

    def moveMissile(mode, missile, player):
        if player.name == mode.P1.name:
            missile.cx += missile.vx * missile.dt
            missile.cy -= missile.vy * missile.dt
        else:
            missile.cx += missile.vx * missile.dt
            missile.cy += missile.vy * missile.dt
        collision = SinglePlayerMode.checkCollision(mode, missile)
        if collision != None:
            return False # player turn is over
        else:
            missile.updateVelocity()
            return True # missile keeps moving

    def checkCollision(mode, missile):
        for planet in mode.planets:
            if (Missile.distance(missile.cx, missile.cy, planet.cx, planet.cy)\
                    <= planet.r+missile.r):
                return "planet"
        if (Missile.distance(missile.cx, missile.cy, mode.width//2, 0)\
             < mode.activePlayer.hitRadius + missile.r):
            return "Player 2"
        elif (Missile.distance(missile.cx, missile.cy, mode.width//2,\
            mode.height) < mode.activePlayer.hitRadius + missile.r):
            return "Player 1"
        elif (missile.cy <= 0 or missile.cy >= mode.height):
            return "boundary"
        else:
            return None

    def calculateAngleDamages(mode, player, otherPlayer):
        playerDamages = []
        for angle in range(mode.minAngle, mode.maxAngle+1):
            for strength in range(mode.minStrength, mode.maxStrength+1):
                missile = SinglePlayerMode.getMissile(mode, angle, strength, player)
                while SinglePlayerMode.moveMissile(mode, missile, player) == True:
                    continue
                collision = SinglePlayerMode.checkCollision(mode, missile)
                if (collision == otherPlayer.name):
                    damage = SinglePlayerMode.missileDamage(missile)
                    hitAngle = math.degrees(missile.angleFromObject(mode.width//2,\
                        otherPlayer.startHeight, missile.cx, missile.cy))
                    playerDamages.append((angle, strength, int(damage), int(hitAngle)))
                    #playerDamages[(angle, strength)] = int(damage)
        return playerDamages

    def keyPressed(mode, event):
        if mode.activePlayer == mode.P1:
            super().keyPressed(event)
        else:
            if event.key == "c":
                GameMode.completeMove(mode)
            if event.key == "r":
                GameMode.setupGame(mode)
            elif event.key == "R": #shift R
                mode.app.setActiveMode(mode.app.levelSelectMode)
    
    def switchPlayer(mode):
        if mode.activePlayer == mode.P1:
            mode.activePlayer = mode.P2
            mode.inactivePlayer = mode.P1
            SinglePlayerMode.opponent(mode)
        else: 
            mode.activePlayer = mode.P1
            mode.inactivePlayer = mode.P2

    def timerFired(mode):
        if mode.activePlayer.missileFired == True:
            # if missile collision
            # colX, colY, vxF, vyF, crashed = mode.activePlayer.missile.move(mode.activePlayer)
            if mode.activePlayer.missile.move(mode.activePlayer) == False:
                mode.activePlayer.missileFired = False
                SinglePlayerMode.switchPlayer(mode)
                if mode.inactivePlayer.health <= 0 or\
                    mode.activePlayer.health <= 0:
                    mode.gameOver = True

    def highestDamageMove(mode, damageAngles):
        bestDamage = 0
        bestMove = (0,0)
        for (angle, strength, damage, hitAngle) in damageAngles:
            if damage > bestDamage:
                bestDamage = damage
                bestMove = (angle, strength, damage, hitAngle)
        return bestMove

    def limitPlayerMove(mode, otherDamageAngles, damageAngles):
        optimalAngle, strength, damage, hitAngle =\
             SinglePlayerMode.highestDamageMove(mode, otherDamageAngles)
        otherDamageAngles.remove((optimalAngle, strength, damage, hitAngle))
        possibleMoves = []
        for (angle, strength, damage, hitAngle) in damageAngles:
            for i in range(hitAngle - 4, hitAngle + 5):
                if i == optimalAngle:
                    possibleMoves.append((angle, strength, damage, hitAngle))
        if possibleMoves == []:
            possibleMoves = damageAngles
        bestMove = SinglePlayerMode.highestDamageMove(mode, possibleMoves)
        return bestMove

    def opponent(mode):
        if mode.activePlayer == mode.P2:
            if mode.P2.health == 100:
                angle, strength, damage, hitAngle =\
                     SinglePlayerMode.highestDamageMove(mode,\
                    mode.P1Damages)
            else:
                angle, strength, damage, hitAngle =\
                 SinglePlayerMode.limitPlayerMove(mode,\
                    mode.P1Damages, mode.P2Damages)
            mode.activePlayer.missileAngle = angle
            mode.activePlayer.missileStrength = strength
            mode.activePlayer.fireMissile()
            mode.activePlayer.missileFired = True

    def removeAngles(angleList, hitAngle):
        anglesToRemove = set(range(hitAngle-4, hitAngle+5))
        newAngles = set()
        for angle in angleList:
            if angle not in anglesToRemove:
                newAngles.add(angle)
        return newAngles
'''
    def play(mode):
        if not mode.gameOver:
            mode.result = mode.isEnd()
            if mode.result != None:
                mode.gameOver = True
            if mode.activePlayer == mode.P2: #AI
                (m, angle, strength) = mode.maxAB(1000000, -1000000)
                print("passed")
                mode.activePlayer.missileAngle = angle
                mode.activePlayer.missileStrength = strength
                mode.activePlayer.fireMissile()
                mode.currentState = State(mode.P1.health, mode.P2.health,\
                    mode.P1.availableAngles, mode.P2.availableAngles)
                mode.activePlayer.missileFired = True
    
    def isEnd(mode):
        # checks if game over
        if mode.inactivePlayer.health <= 0:
            return mode.activePlayer.name
        elif mode.activePlayer.health <= 0:
            return mode.inactivePlayer.name
        elif len(mode.activePlayer.availableAngles) == 0:
            return mode.inactivePlayer.name
        elif len(mode.inactivePlayer.availableAngles) == 0:
            return mode.activePlayer.name
        else:
            return None

    def maxAB(mode, alpha, beta):
        maxv = -100000
        angleMove = None
        strengthMove = None 

        result = mode.isEnd()
        if result == "Player 1":
            healthDiff = abs(mode.currentState.P1Health-mode.currentState.P2Health)
            return (-healthDiff, 0, 0)
        elif result == "Player 2":
            healthDiff = abs(mode.currentState.P2Health-mode.currentState.P1Health)
            return (healthDiff, 0, 0)

        for (angle, strength, damage, hitAngle) in mode.P2Damages:
            if (angle in mode.currentState.P2Angles):
                mode.prevState = mode.currentState
                mode.currentState = State(mode.prevState.P1Health,\
                    mode.prevState.P2Health-damage, mode.prevState.P1Angles,\
                    SinglePlayerMode.removeAngles(mode.prevState.P2Angles, hitAngle))
                (m, minAngle, minStrength) = mode.minAB(alpha, beta)
                if m > maxv:
                    maxv = m
                    angleMove = angle
                    strengthMove = strength
                self.currentState = self.prevState
                if maxv >= beta:
                    return (maxv, angleMove, strengthMove)
                if maxv > alpha:
                    alpha = maxv
        return (maxv, angleMove, strengthMove)

    def minAB(mode, alpha, beta):
        minv = 100000
        angleMove = None
        strengthMove = None 
 
        result = mode.isEnd()
        if result == "Player 1":
            healthDiff = abs(mode.currentState.P1Health-mode.currentState.P2Health)
            return (-healthDiff, 0, 0)
        elif result == "Player 2":
            healthDiff = abs(mode.currentState.P2Health-mode.currentState.P1Health)
            return (healthDiff, 0, 0)

        for (angle, strength, damage, hitAngle) in mode.P1Damages:
            if (angle in mode.currentState.P1Angles):
                    mode.prevState = mode.currentState
                    mode.currentState = State(mode.prevState.P1Health-damage,\
                        mode.prevState.P2Health,\
                        SinglePlayerMode.removeAngles(mode.prevState.P1Angles, hitAngle),\
                        mode.prevState.P2Angles)
                    (m, maxAngle, maxStrength) = mode.maxAB(alpha, beta)
                    if m < minv:
                        minv = m
                        angleMove = angle
                        strengthMove = strength
                    mode.currentState = mode.prevState
                    if minv <= alpha:
                        return (minv, angleMove, strengthMove)
                    if minv < beta:
                        beta = minv
        return (minv, angleMove, strengthMove)
'''                     

class MyModalApp(ModalApp):
    def appStarted(app):
        app.bg = app.loadImage("https://tinyurl.com/ussunsf")
        app.splashScreenMode = SplashScreenMode()
        app.levelSelectMode = LevelSelectMode()
        app.gameRulesMode = GameRulesMode()
        app.gameMode = GameMode()
        app.singlePlayerMode = SinglePlayerMode()
        app.multiplayerPlanetGameMode = MultiplayerPlanetGameMode()
        app.setActiveMode(app.splashScreenMode)
    
def main():
    MyModalApp(width=550, height=550)
 
if __name__ == '__main__':
    main()
 
    
 

