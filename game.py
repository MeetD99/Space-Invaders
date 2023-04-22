import pygame
import random
import math

pygame.init()

#Screen Setup
screen = pygame.display.set_mode((800 , 600))

#Game Window Title
pygame.display.set_caption("Space Invaders")

#Icon Setup and Display
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

#Background Image
background = pygame.image.load("background.jpg")

#Player Setup
playerIMG = pygame.image.load('spaceship.png')
resizedIMG = pygame.transform.scale(playerIMG , (64,64))
playerX = 370
playerY = 500
playerx_change=0


#enemy Setup
enemyIMG = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

no_of_enemies = 6
for i in range(0 , no_of_enemies):

        if i in [3 , 4 , 5]:
            enemyIMG.append(pygame.image.load('alien.png'))

        enemyIMG.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(0.2)
        enemyY_change.append(40)
def enemies(no_of_enemies):
    for i in range(0 , no_of_enemies):

        if i in [3 , 4 , 5]:
            enemyIMG.append(pygame.image.load('alien.png'))

        enemyIMG.append(pygame.image.load('enemy.png'))
        enemyX.append(random.randint(0,736))
        enemyY.append(random.randint(50,150))
        enemyX_change.append(0.2)
        enemyY_change.append(20)

#Missile Setup
missileIMG = pygame.image.load('missile.png')
missile_resizedIMG = pygame.transform.scale(missileIMG , (32,32))
missileX = 0
missileY = 500
missileX_change = 0
missileY_change = 0.8
missile_state = "ready"



def player(x,y):
    screen.blit(resizedIMG , (x , y))

def enemy(x , y , i):
    screen.blit(enemyIMG[i] , (x,y))

def fire_missile(x,y):
    global missile_state
    missile_state = "fire"
    screen.blit(missile_resizedIMG , ( x+16 , y+10 ))

def isCollision(enemyX , enemyY , missileX , missileY):
    distance = math.sqrt((math.pow((enemyX - missileX),2)) + (math.pow((enemyY - missileY),2)))

    if distance < 27:
        return True
    else:
        return False

def isCollisionOver(enemyX , enemyY , missileX , missileY):
    distance = math.sqrt((math.pow((enemyX - missileX),2)) + (math.pow((enemyY - missileY),2)))

    if distance < 50:
        return True
    else:
        return False



# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf' , 32)

# Game Over
over_font = pygame.font.Font('freesansbold.ttf' , 64)

textX = 10
textY=10

def show_score(x , y):
    score = font.render( f"Score: {str(score_value)}" , True , (255 , 255 , 128))
    screen.blit(score , (x,y))

# def game_over_text():
#     over_text = over_font.render( "Game Over!" , True , (0 , 0 , 0))
#     #screen.blit(over_text , (310 , 270))


####  MAIN WHILE LOOP  ####
running = True
while running:
    # Screen background addition
    screen.fill((0,0,0))
    screen.blit(background , (0,0))

    # Iterating through events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -0.7
            if event.key == pygame.K_RIGHT:
                playerx_change = 0.7
            if event.key == pygame.K_SPACE:
                if missile_state == "ready":
                    missileX = playerX
                    fire_missile(missileX , missileY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0


    # Player Movement
    playerX += playerx_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    # Enemy Movement
    for i in range(no_of_enemies):

        if isCollisionOver(playerX , playerY , enemyX[i] , enemyY[i]):
            for j in range(no_of_enemies):
                enemyY[j] = 2000
            over_text = over_font.render( "Game Over!" , True , (255 , 255 , 255) )
            screen.blit(over_text , (240 , 130))
            over_text2 = over_font.render( f"Score : {score_value}" , True , (255 , 255 , 255) )
            screen.blit(over_text2 , (270 , 190))
            pygame.display.update()
            pygame.time.delay(5000)
            break



        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i]  = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision checking
        collision = isCollision(enemyX[i] , enemyY[i] , missileX , missileY)
        if collision:
            missileY = 500
            missile_state = "ready"
            score_value += 1
            if score_value == 20:
                no_of_enemies = 10
                enemies(10)

            if score_value == 30:
                no_of_enemies = 15
                enemies(15)

            if score_value == 40:
                no_of_enemies = 20
                enemies(20)

            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i] , enemyY[i] , i)

    # Bullet Movement
    if missileY <= 0:
        missileY = 500
        missile_state = "ready"


    if missile_state is "fire":
        fire_missile(missileX , missileY)
        missileY -= missileY_change




    #Running Functions
    player(playerX , playerY)
    show_score(textX , textY)
    pygame.display.update()
