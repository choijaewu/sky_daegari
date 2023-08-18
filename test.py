import pygame
from pyc import *
import time


pygame.init()

screen_width, screen_height = 1200, 700
screen = pygame.display.set_mode((screen_width, screen_height))
koreanfont = pygame.font.SysFont('malgungothic', 30)
story = ['건후바보',
         '건후건후',
         '옛날 옛적에 어느 한 마을에 김건후라는 소녀가 살았어요',
         '그 아이는 가난했지만 어머니의 사랑만큼은 가득했죠',
         '어느날 부자가 그녀에게 와서 이렇게 말했어요',
         '금을 줄테니 그 순간을 나와 바꾸지 않을래?'
         '그러자 건후가 말했어요. "도를 아십니까?"']
times = [1, 1, 3, 3, 3, 3, 3]
pos = [[540.0, 30],
       [540.0, 80],
       [216.5, 130],
       [242.5, 180],
       [287.5, 230],
       [305.0, 280],
       [3100.0, 330]]
    

def storyscene():
    for i in range(len(story)):
        screen.fill((0,0,0)) #검은색 배경
        for j in range(i+1):
            message = koreanfont.render(story[j], True, (100,100,100)) #메세지 지정
            screen.blit(message, pos[j]) #메세지 띄우기

        pygame.display.update() #화면 업데이트
        
        for event in pygame.event.get(): #이벤트 입력
            if event.type == pygame.QUIT: #X버튼 눌렀을 때
                break #종료
        
        time.sleep(times[i]) #멈추기

    pygame.quit()


        
if __name__ == "__main__": storyscene()