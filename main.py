import pygame
import random
import math
import sys

# initialize sounds effect
pygame.init()
pygame.mixer.init()

# screen display
WIDTH ,HEIGHT = 800, 600
wn = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NFS 2D Raing Game")
font = pygame.font.Font("freesansbold.ttf", 33)
small_font = pygame.font.Font("freesansbold.ttf", 25)

# colors
WHITE = (255, 255,255)
BLACK = (0, 0, 0)
RED = (255, 0, 0 )
YELLOW = (255, 255, 0)


#=====game images========
bg = pygame.image.load("bg.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
maincar = pygame.image.load("car.png")
car1 = pygame.image.load("car1.png")
car2 = pygame.image.load("car2.png")
car3 = pygame.image.load("car3.png")
logo = pygame.image.load("logo.png")
logo = pygame.transform.scale(logo, (400, 200))

# ======variables of the game======== 
game_exit = False
score_value = 0
maincar_x, maincar_y = 290, 500
maincar_xchange = 0
speed = 5
level = "Easy"
game_pause = False
game_over = False 

# --------sound effects-----
pygame.mixer.music.load('background.mp3')
crash_sound = pygame.mixer.Sound('car_crash.mp3')


# ======enemy cars========
enemy_cars = [
    {"image": car1, "x": random.randint(190, 493), "y": -200, "speed": speed},
    {"image": car2, "x": random.randint(190, 493), "y": -500, "speed": speed},
    {"image": car3, "x": random.randint(190, 493), "y": -800, "speed": speed},
]

# =====game functions========
 #display text 
def display_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    wn.blit(text_surface, (x, y))

# ======display the menu =====
def draw_menu():
    wn.fill(BLACK)
    display_text("NFC 2D Raing Game", font, WHITE, 300, 150)
    display_text("1. start Game", small_font, WHITE, 300, 200)
    display_text("2. Difficulty: " + level, small_font, WHITE, 300, 250)
    display_text("3. Exit", small_font, WHITE, 300, 300)
    pygame.display.update()

# ======resets the game======
def reset_game():
    global maincar_x, maincar_y, score_value, game_paused, game_over, enemy_cars, maincar_xchange
    maincar_x, maincar_y = 290, 400
    maincar_xchange = 0
    score_value = 0
    game_paused = False
    game_over = False
    enemy_cars = [
        {"image": car1, "x": random.randint(180, 493), "y": -200, "speed": speed},
        {"image": car2, "x": random.randint(190, 493), "y": -500, "speed": speed},
        {"image": car3, "x": random.randint(190, 493), "y": -800, "speed": speed},
    ]

    pygame.mixer.music.play(-1)

# =====function for cheking if you have hit an obstacle or enemy car=====
def is_collision(maincar_x, maincar_y, car_x, car_y):
    distance = math.sqrt((maincar_x - car_x) ** 2 + (maincar_y - car_y) ** 2) 
    return distance < 50

def  update_enemy_car():
    for car in enemy_cars:
        car["y"] += car["speed"]
        if car["y"] > HEIGHT:
            car["y"] = -200
            car ["x"] = random.randint(200, 500)
            global score_value
            score_value += 1

def game():
    wn.blit(bg, (0, 0))
    wn.blit(maincar, (maincar_x, maincar_y))
    for car in enemy_cars:
        wn.blit(car["image"], (car["x"], car["y"]))
    display_text(f"Score: {score_value}", font, WHITE, 10, 10)
    if game_paused:
        display_text("PAUSED", font, YELLOW, 320, 250)
        display_text("PRess C to continue", small_font, WHITE, 280, 300)
        display_text("Press R to Restart", small_font, WHITE,280, 350)
    elif game_over:
        wn.fill(BLACK)
        display_text("GAME OVER!", font, RED, 300, 200)
        display_text(f"Final Score: {score_value}", small_font, WHITE, 300,300)
        display_text(f"Level: {level}", small_font, WHITE, 300, 350)
        display_text("Press R to Restart", small_font, WHITE, 300, 400)
        display_text("Press M for Menu", small_font,WHITE, 300, 450)
    pygame.display.update()

    
    # ===game loop=====

def main():
        global game_exit, maincar_x, maincar_y, maincar_xchange, game_paused, game_over, level, speed

        clock = pygame.time.Clock()
        menu_active = True
        show_logo = True
        logo_start = pygame.time.get_ticks()

        while not game_exit:
            if show_logo:
                wn.fill(BLACK)
                wn.blit(logo, (WIDTH // 2 - logo.get_width() // 2, HEIGHT // 2 - logo.get_height() // 2))
                pygame.display.update()

                if pygame.time.get_ticks() - logo_start > 3000: 
                    show_logo = False
            else:       
                if menu_active:
                    draw_menu()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_exit = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_1:
                                reset_game()
                                menu_active = False
                            elif event.key == pygame.K_2:
                                level = "Hard" if level == "Easy" else "Easy"
                                speed = 8 if level == "Hard" else 5
                                draw_menu()
                            elif event.key == pygame.K_3:
                                game_exit = True

                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            game_exit = True

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RIGHT:
                                maincar_xchange = 5
                            elif event.key == pygame.K_LEFT:
                                maincar_xchange = -5
                            elif event.key == pygame.K_p:
                                game_paused = not game_paused
                            elif event.key == pygame.K_r and (game_paused or game_over):
                                reset_game()
                            elif event.key == pygame.K_c and game_paused:
                                game_paused = False
                            elif event.key == pygame.K_m and game_over:
                                menu_active = True
                            
                        if event.type == pygame.KEYUP:
                            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                                    maincar_xchange = 0

                    if not game_paused and not game_over:
                        maincar_x += maincar_xchange
                        update_enemy_car()


                        # boundaries................
                        if maincar_x <=200:
                            maincar_x = 200
                        elif maincar_x >= 495:
                            maincar_x = 495


                        
                        # collition checking..

                        for car in enemy_cars:
                            if is_collision(maincar_x, maincar_y, car["x"], car["y"]):
                                pygame.mixer.music.stop()
                                crash_sound.play()
                                game_over = True

                    game()
                    clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()
                    