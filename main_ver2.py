import pygame
import random


pygame.init() #초기화


background_image = pygame.image.load("")

player_image = pygame.image.load("")

enemy_1_image = pygame.image.load("")
enemy_2_image = pygame.image.load("")
enemy_3_image = pygame.image.load("")
boss_image = pygame.image.load("")

chest_image = pygame.image.load("")

player_info = {
    'max_health' : 5,
    'current_health' : 5,
    'max_cost' : 3,
    'current_cost' : 3,
    'critical' : 25,
    
}


enemy_xlocation = [i for i in range(600, 950, 50)]

game_display = pygame.display.set_mode((1200,700)) #게임 창 크기
pygame.display.set_caption("게임이름") #게임 창 이름


running = 1 #게임이 실행중인가?


while running:
    for event in pygame.event.get(): #이벤트 입력
        if event.type == pygame.QUIT: #X버튼 눌렀을 때
            running = 0 #프로그램 종료
        
    
    pygame.blit(background_image, (0,0))
    pygame.blit(player_image,(300, 350))

    pygame.display.update()


pygame.quit() #종료 