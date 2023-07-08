import pygame

pygame.init() #초기화

background = pygame.display.set_mode((1366,768)) #게임 창 크기
pygame.display.set_caption("게임이름") #게임 창 이름

running = 1 #게임이 실행중인가?

while running:
    for event in pygame.event.get(): #이벤트 입력
        if event.type == pygame.QUIT: #X버튼 눌렀을 때
            running = 0 #프로그램 종료

pygame.quit() #종료 