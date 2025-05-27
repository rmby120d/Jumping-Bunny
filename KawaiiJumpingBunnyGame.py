import pygame
import random
import math
import os

# Inicializar pygame
pygame.init()
WIDTH, HEIGHT = 680, 320
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Conejito Kawaii Salta Dulces")
clock = pygame.time.Clock()

# Colores
PASTEL_BG_TOP = (200, 247, 250)
PASTEL_BG_BOTTOM = (255, 232, 244)
GROUND_COLOR = (255, 230, 252)
BUNNY_BODY = (255, 255, 255)
BUNNY_SHADOW = (190, 125, 188)
BUNNY_EAR = (255, 216, 246)
BONUS_COLORS = [(122, 248, 209), (138, 228, 252)]

# Sonidos (opcional, puedes agregar archivos .wav si quieres)
# sound_jump = pygame.mixer.Sound("jump.wav")
# sound_crash = pygame.mixer.Sound("crash.wav")
# sound_bonus = pygame.mixer.Sound("bonus.wav")

GROUND_Y = 250

font = pygame.font.SysFont("Comic Sans MS", 22, bold=True)
font_small = pygame.font.SysFont("Comic Sans MS", 16)
font_big = pygame.font.SysFont("Comic Sans MS", 36, bold=True)
font_italic = pygame.font.SysFont("Comic Sans MS", 18, italic=True)

motivationalPhrases = [
    "¡Puedes mejorar tu récord!",
    "¡Sigue saltando, campeón!",
    "¡Eres un conejito imparable!",
    "¡Kawaii power! ¡No te rindas!",
    "¡La práctica hace al maestro!"
]

class Bunny:
    def __init__(self):
        self.x = 60
        self.y = GROUND_Y
        self.vy = 0
        self.w = 46
        self.h = 50
        self.jumping = False
        self.gravity = 0.8
        self.jumpPower = 13

    def draw(self, shield):
        # Sombra
        pygame.draw.ellipse(screen, BUNNY_SHADOW, (self.x-17, self.y+45, 34, 14), 0)
        # Cuerpo
        pygame.draw.ellipse(screen, BUNNY_BODY, (self.x-18, self.y-6, 36, 40))
        # Orejas
        pygame.draw.ellipse(screen, BUNNY_BODY, (self.x-22, self.y-28, 16, 48))
        pygame.draw.ellipse(screen, BUNNY_BODY, (self.x+6, self.y-28, 16, 48))
        pygame.draw.ellipse(screen, BUNNY_EAR, (self.x-18, self.y-23, 8, 30))
        pygame.draw.ellipse(screen, BUNNY_EAR, (self.x+10, self.y-23, 8, 30))
        # Ojos
        pygame.draw.circle(screen, (145, 85, 164), (self.x-6, self.y+6), 3)
        pygame.draw.circle(screen, (145, 85, 164), (self.x+6, self.y+6), 3)
        # Mejillas
        pygame.draw.circle(screen, (255, 215, 231), (self.x-10, self.y+14), 3)
        pygame.draw.circle(screen, (255, 215, 231), (self.x+10, self.y+14), 3)
        # Nariz
        pygame.draw.circle(screen, (227, 129, 180), (self.x, self.y+10), 2)
        # Boca
        pygame.draw.arc(screen, (227, 129, 180), (self.x-4, self.y+12, 8, 4), math.pi, 2*math.pi, 1)
        # Escudo
        if shield:
            pygame.draw.circle(screen, (157, 247, 250), (self.x, self.y+18), 29, 4)

class Obstacle:
    def __init__(self, kind):
        self.x = WIDTH + 60
        self.y = GROUND_Y + 18
        self.w = 36
        self.h = 38
        self.type = kind
        self.passed = False

    def draw(self):
        color_table = {
            "lollipop": (255, 152, 230),
            "cookie": (255, 235, 187),
            "cupcake": (251, 208, 236),
            "gummy": (168, 224, 254),
            "candycane": (255, 123, 185),
            "jellybean": (255, 232, 152),
            "donut": (251, 148, 233)
        }
        pygame.draw.ellipse(screen, color_table.get(self.type, (255,255,200)),
            (self.x-18, self.y-20, 36, 36))

class Bonus:
    def __init__(self, idx):
        self.x = WIDTH + 60
        self.y = GROUND_Y - 30 - random.random()*40
        self.r = 16
        self.type = idx  # 0: Salto alto, 1: Escudo
        self.active = True

    def draw(self, anim):
        color = BONUS_COLORS[self.type]
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), int(self.r+math.sin(anim/8)*2))

def randomCandyType():
    types = ["lollipop", "cookie", "cupcake", "gummy", "candycane", "jellybean", "donut"]
    return random.choice(types)

def resetGame():
    global bunny, obstacles, bonuses, score, gameOver, bunnyBonus, bunnyBonusTime, bunnyShield
    global finalMessage, frame, newRecord, newRecordAnim
    score = 0
    gameOver = False
    newRecord = False
    bunnyBonus = None
    bunnyBonusTime = 0
    bunnyShield = False
    obstacles = []
    bonuses = []
    bunny.y = GROUND_Y
    bunny.vy = 0
    bunny.jumping = False
    bunny.jumpPower = 13
    frame = 0
    newRecordAnim = 0
    finalMessage = random.choice(motivationalPhrases)

# Juego
bunny = Bunny()
score = 0
best = 0
gameOver = False
newRecord = False
newRecordAnim = 0
bunnyBonus = None
bunnyBonusTime = 0
bunnyShield = False
frame = 0
bonusAnim = 0
accelerating = False

obstacles = []
bonuses = []
finalMessage = ""

def addObstacle():
    kind = randomCandyType()
    obstacles.append(Obstacle(kind))

def addBonus():
    if random.random() < 0.5:
        idx = random.choice([0, 1])
        bonuses.append(Bonus(idx))

def jump():
    global gameOver
    if not bunny.jumping and not gameOver:
        bunny.vy = -bunny.jumpPower
        bunny.jumping = True
        # sound_jump.play()
    if gameOver:
        resetGame()

def update():
    global frame, bonusAnim, bunnyBonusTime, bunnyBonus, bunnyShield, score, best, newRecord, newRecordAnim, gameOver
    frame += 1
    bonusAnim += 1
    if bunnyBonusTime > 0:
        bunnyBonusTime -= 1
    if bunnyBonusTime <= 0 and bunnyBonus:
        bunny.jumpPower = 13
        bunnyBonus = None
        bunnyShield = False

    bunny.y += bunny.vy
    bunny.vy += bunny.gravity

    if bunny.y >= GROUND_Y:
        bunny.y = GROUND_Y
        bunny.vy = 0
        bunny.jumping = False

    vel = 4 + (score // 8) + (2 if accelerating else 0)
    if frame % (68 if accelerating else 86) == 0:
        addObstacle()
    if frame % 270 == 0 and random.random() < 0.5:
        addBonus()

    for obs in obstacles:
        obs.x -= vel
    obstacles[:] = [o for o in obstacles if o.x > -60]

    for bon in bonuses:
        bon.x -= vel
    bonuses[:] = [b for b in bonuses if b.x > -40 and b.active]

    # Colisiones
    for obs in obstacles:
        if not obs.passed and obs.x+bunny.w/2 > bunny.x-bunny.w/2:
            if (obs.x < bunny.x+bunny.w/2 and
                obs.x+obs.w > bunny.x-bunny.w/2 and
                bunny.y+bunny.h-20 > obs.y and
                bunny.y < obs.y+obs.h-6):
                if bunnyShield:
                    bunnyShield = False
                    # sound_bonus.play()
                    obs.passed = True
                    score += 1
                else:
                    # sound_crash.play()
                    gameOver = True
                    if score > best:
                        best = score
                        newRecord = True
                        newRecordAnim = 50
            if not obs.passed and obs.x+bunny.w/2 < bunny.x-bunny.w/2:
                obs.passed = True
                score += 1

    # Bonus
    for bon in bonuses:
        if bon.active and abs(bon.x-bunny.x)<24 and abs(bon.y-bunny.y)<36:
            bon.active = False
            # sound_bonus.play()
            if bon.type == 0:  # Salto alto
                bunnyBonus = "salto"
                bunnyBonusTime = 400
                bunny.jumpPower = 20
            else:
                bunnyBonus = "escudo"
                bunnyBonusTime = 400
                bunnyShield = True

def drawBackground():
    # Fondo pastel
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(PASTEL_BG_BOTTOM[0] * (1-ratio) + PASTEL_BG_TOP[0] * ratio)
        g = int(PASTEL_BG_BOTTOM[1] * (1-ratio) + PASTEL_BG_TOP[1] * ratio)
        b = int(PASTEL_BG_BOTTOM[2] * (1-ratio) + PASTEL_BG_TOP[2] * ratio)
        pygame.draw.line(screen, (r,g,b), (0, y), (WIDTH, y))
    # Suelo
    pygame.draw.line(screen, GROUND_COLOR, (0, GROUND_Y+32), (WIDTH, GROUND_Y+32), 12)

def draw():
    screen.fill((255,255,255))
    drawBackground()

    for obs in obstacles:
        obs.draw()
    for bon in bonuses:
        if bon.active: bon.draw(bonusAnim)
    bunny.draw(bunnyShield)

    # Power-up indicador
    if bunnyBonus:
        name = "Salto Alto" if bunnyBonus == "salto" else "Escudo"
        txt = font.render(name, True, (10,180,220) if bunnyBonus=="salto" else (20,119,220))
        screen.blit(txt, (500, 18))

    # Score
    txt = font.render(f"Puntaje: {score}", True, (228,129,255))
    screen.blit(txt, (24, 8))
    if best > 0:
        screen.blit(font.render(f"Mejor: {best}", True, (228,129,255)), (24, 38))
    # Nuevo récord
    if newRecordAnim > 0:
        t = math.sin(newRecordAnim/2)
        surf = font_big.render("¡Nuevo récord mundial!", True, (255,224,112))
        surf.set_alpha(int(170 + 85*t))
        screen.blit(surf, (WIDTH//2 - surf.get_width()//2, 100))
    # Game Over
    if gameOver:
        pygame.draw.rect(screen, (255,244,252), (90,60,500,180))
        pygame.draw.rect(screen, (251,201,250), (90,60,500,180), 4)
        txt1 = font_big.render("¡Fin del juego!", True, (255,129,190))
        txt2 = font.render(f"Puntaje: {score}", True, (179,147,211))
        txt3 = font.render(f"Récord: {best}", True, (255,199,77))
        txt4 = font_italic.render(finalMessage, True, (172,105,242))
        txt5 = font_small.render("Presiona espacio o toca para jugar de nuevo", True, (255,127,161))
        screen.blit(txt1, (WIDTH//2 - txt1.get_width()//2, 112))
        screen.blit(txt2, (WIDTH//2 - txt2.get_width()//2, 150))
        screen.blit(txt3, (WIDTH//2 - txt3.get_width()//2, 178))
        screen.blit(txt4, (WIDTH//2 - txt4.get_width()//2, 207))
        screen.blit(txt5, (WIDTH//2 - txt5.get_width()//2, 237))
    pygame.display.flip()

resetGame()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump()
            if event.key == pygame.K_RIGHT:
                accelerating = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                accelerating = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            jump()

    if not gameOver:
        update()
    if newRecordAnim > 0:
        newRecordAnim -= 1
    draw()
    clock.tick(60)

pygame.quit()