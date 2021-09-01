import pygame
import random

#initialize pygame after import
pygame.init()

#create the game clock
clock = pygame.time.Clock()
speed = 30

#set display parameters
display_width = 500
display_height = 300

#set ball parameters
x = 100
y = 100
radius = 10

#set paddle parameters
paddle_x = 10
paddle_y = 10
paddle_width = 3
paddle_height = 40


score = 0

#ball's movement
dx = 3
dy = 3


def randomize_start():
    global x, y, dy
    x = random.randint(int(display_width/4), display_width - 20)
    y = random.randint(10, display_height - 10)
    if random.randint(0, 2) % 2 == 0:
        dy *= -1

def hit_back():
    return x + radius > display_width

def hit_sides():
    return y - radius < 0 or y + radius > display_height

def hit_paddle():
    global score
    if x - radius <= paddle_x + paddle_width and y > paddle_y and y < paddle_y + paddle_height:
        score += 100
        return True
    return False

def game_over():
    global score
    end_game = True
    #display.fill(0, 0, 0)
    font_title = pygame.font.Font(None, 36)
    font_instructions = pygame.font.Font(None, 36)
    announcement = font_title.render("Game Over", True, (255, 255, 255))
    announcement_rect = announcement.get_rect(center = (int(display_width/2), int(display_height/2)))
    display.blit(announcement, announcement_rect)
    qinstructions = font_instructions.render("Press q to quit", True, (255, 255, 255))
    qinstructions_rect = qinstructions.get_rect(center = (int(display_width/2), int(display_height/1.5)))
    display.blit(qinstructions, qinstructions_rect)
    rinstructions = font_instructions.render("Press r to resume", True, (255, 255, 255))
    rinstructions_rect = rinstructions.get_rect(center = (int(display_width/2), int(display_height/1.3)))
    display.blit(rinstructions, rinstructions_rect)    
    final_score = "Final score: " + str(score)
    score_ann = font_instructions.render(final_score, True, (255, 255, 255))
    score_ann_rect = score_ann.get_rect(center = (int(display_width/2), int(25)))
    display.blit(score_ann, score_ann_rect)   
    pygame.display.flip()

    while end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    exit()
                if event.key == pygame.K_r:
                    end_game = False

#initialize the display and add caption
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Let's Pong!")

welcome_screen = pygame.font.Font(None, 36)
welcome = welcome_screen.render("Let's play Pong", True, (255, 255, 255))
welcome_rect = welcome.get_rect(center = (int(display_width/2), int(display_height/2)))
startmsg = welcome_screen.render("To start hit y or wait for 10s", True, (255, 255, 255))
startmsg_rect = startmsg.get_rect(center = (int(display_width/2), int(display_height/3)))
display.blit(welcome, welcome_rect)
display.blit(startmsg, startmsg_rect)
pygame.display.flip()

pygame.time.set_timer(pygame.USEREVENT, 10000)
timer_active = True

while timer_active == True:
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            timer_active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_y:
                timer_active = False

randomize_start()

while True:
    clock.tick(speed)

    pressed_key = pygame.key.get_pressed()
    if pressed_key[pygame.K_DOWN] or pressed_key[pygame.K_s]:
        if paddle_y + paddle_height + 10 <= display_height:
            paddle_y += 10
    elif pressed_key[pygame.K_UP] or pressed_key[pygame.K_w]:
        if paddle_y - 10 >= 0:
            paddle_y -= 10    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    display.fill((0, 0, 0))
    x += dx
    y += dy

    #create the paddles
    pygame.draw.rect(display, (255, 255, 255), (paddle_x, paddle_y, paddle_width, paddle_height))

    #draw the ball
    pygame.draw.circle(display, (255, 255, 255), (x, y), radius)
    
    #check for collisions
    if x < radius:
        game_over()
        dx = abs(dx)
        score = 0
        randomize_start()
    if hit_back() or hit_paddle():
        dx *= -1
    if hit_sides():
        dy *= -1

    #update the display
    pygame.display.update()

    stayopen = True