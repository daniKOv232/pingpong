import pygame
from pygame import sprite, transform, image, display, event, time
from random import randint

pygame.init()

window_width = 700
window_height = 500
window = display.set_mode((window_width, window_height))
display.set_caption('Пинг-Понг')

background = transform.scale(image.load('фон.jpg'), (window_width, window_height))
left_wall_image = transform.scale(image.load('стена.png'), (10, 200)) 
right_wall_image = transform.scale(image.load('стена.png'), (10, 200))  
ball_image = transform.scale(image.load('мячик.jpg'), (30, 30))

font = pygame.font.SysFont('Arial', 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, speed, x, y):
        super().__init__()
        self.image = player_image
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(GameSprite):
    def update(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

        if self.rect.top <= 0 or self.rect.bottom >= window_height:
            self.speed[1] *= -1  

left_score = 0
right_score = 0

def reset_ball():
    ball.rect.x = window_width // 2 - 15
    ball.rect.y = window_height // 2 - 15
    ball.speed[0] *= -1 

left_wall = GameSprite(left_wall_image, 0, 50, (window_height - 200) // 2)  
right_wall = GameSprite(right_wall_image, 0, window_width - 60, (window_height - 200) // 2)  
ball_speed = [randint(3, 5), randint(3, 5)]
ball = Ball(ball_image, ball_speed, window_width // 2 - 15, window_height // 2 - 15)

clock = time.Clock()
running = True

while running:
    for e in event.get():
        if e.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()  
    
    if keys[pygame.K_w] and left_wall.rect.top > 0:   
        left_wall.rect.y -= 5
    if keys[pygame.K_s] and left_wall.rect.bottom < window_height:   
        left_wall.rect.y += 5

    if keys[pygame.K_UP] and right_wall.rect.top > 0:   
        right_wall.rect.y -= 5
    if keys[pygame.K_DOWN] and right_wall.rect.bottom < window_height:   
        right_wall.rect.y += 5

    ball.update()

    
    if ball.rect.colliderect(left_wall.rect) or ball.rect.colliderect(right_wall.rect):
        ball.speed[0] *= -1 
    elif ball.rect.left <= 0:
        right_score += 1
        reset_ball()
    elif ball.rect.right >= window_width: 
        left_score += 1
        reset_ball()

    window.blit(background, (0, 0))
    
    score_text = font.render(f"{left_score} : {right_score}", True, (0,0,0))
    window.blit(score_text, (window_width // 2 - score_text.get_width() // 2 ,20))

    left_wall.reset()
    right_wall.reset()
    ball.reset()

    display.update()
    clock.tick(60)

pygame.quit()