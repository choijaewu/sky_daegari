import pygame
import random
import time
from pyc import *
from pygame.sprite import AbstractGroup

pygame.init()

pygame.display.set_caption("게임이름") #게임 창 이름

clock = pygame.time.Clock()

#색 정의
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
purple = (148, 0, 211)

#폰트 정의
font = pygame.font.SysFont('malgungothic',30)

screen_width, screen_height = 1200, 700 #화면 넓이, 높이
screen = pygame.display.set_mode((screen_width, screen_height)) #게임 창 크기

display_duration = 1000 #1초 (단위:밀리초)
text_change_delay = 2000
start_time = pygame.time.get_ticks()

#text정의
current_text = "이곳은 새벽의 나라"
text_color = white
text = font.render(current_text, True, white)
text_rect = text.get_rect()
text_rect.center = (screen_width // 2, screen_height // 2)#크기

screen.fill(black)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(text,text_rect)

    current_time = pygame.time.get_ticks()
    if current_time - start_time >= text_change_delay:    #여기서 시간을 계산
        if current_text == "이곳은 새벽의 나라":
            current_text = "다른 나라에 비해 발전은 늦지만"

        elif current_text == "다른 나라에 비해 발전은 늦지만":
            current_text = "높은 인망으로 호평을 받는 곳이다."

        elif current_text == "높은 인망으로 호평을 받는 곳이다.":
            current_text = "그런데"
            text_color = red

        elif current_text == "그런데":
            current_text = "땅이 갈라지며 나타난"
            text_color = white

        elif current_text == "땅이 갈라지며 나타난":
            current_text = "절망의 군대"
            text_color = purple

        elif current_text == "절망의 군대":
            current_text = "그들은 모든 건물을 불태우고 사람들을 죽였다."
            text_color = white

        elif current_text == "그들은 모든 건물을 불태우고 사람들을 죽였다.":
            current_text = "그러나 나라를 구하기 위해 나타난 전사"
           

        elif current_text == "그러나 나라를 구하기 위해 나타난 전사":
            current_text = "그는 곧장 절망의 미로로 들어갔고"

        elif current_text == "그는 곧장 절망의 미로로 들어갔고":
            current_text = "적을 섬멸해 나간다."

        elif current_text == "적을 섬멸해 나간다.":
            current_text = "그의 이름은 바로..."

        screen.fill(black)
        text = font.render(current_text, True, white)
        text_rect = text.get_rect()
        text_rect.center = (screen_width // 2, screen_height // 2)

        start_time = pygame.time.get_ticks()
            
    pygame.display.flip()

pygame.quit()