
import pygame
import random


pygame.init() #초기화



game_display = pygame.display.set_mode((1200,700)) #게임 창 크기
pygame.display.set_caption("게임이름") #게임 창 이름


running = 1 #게임이 실행중인가?


while running:
    for event in pygame.event.get(): #이벤트 입력
        if event.type == pygame.QUIT: #X버튼 눌렀을 때
            running = 0 #프로그램 종료
        
    li = [i for i in range(950, 600, -50)]
    li2 = ['건후', '좋건후', '건후 바보', '김건후']
    for i in range(6):
        pygame.draw.circle(game_display, 'blue', (li[i],350), 20)
        print(li2[i * -1])
    x, y = 300, 350
    pygame.draw.circle(game_display, 'red', (x,y), 20)
    pygame.display.update()

print(li2[-1])
print(li2[-2])

pygame.quit() #종료 