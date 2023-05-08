import pygame
import time
import random
from sys import exit

pygame.init()
screen = pygame.display.set_mode((1200,800)) # width/height
pygame.display.set_caption("Distributed Driving Game") # Set game name 
font=pygame.font.Font("fonts/Valorax-lg25V.otf",60) # type/size

clock = pygame.time.Clock() # fps

game_window=pygame.Surface((1200,800))
chat_window = pygame.Surface((300,800))

play_text = font.render("Play",True,"White")
play_rect = play_text.get_rect(topleft= (490,250))

options_text = font.render("Options",True,"White")
options_rect = play_text.get_rect(topleft= (450,350))



quit_text = font.render("Quit",True,"White")
quit_rect = play_text.get_rect(topleft= (510,450))

start_car = pygame.image.load("images/start_car.png").convert_alpha()
start_car_x_pos=-200


#option_window=pygame.image.load("images/credits.png")
back_text = font.render("Back",True,"White")
back_rect = play_text.get_rect(topleft= (0,0))




audi = pygame.image.load("images/Audi.png").convert_alpha()
ambulance = pygame.image.load("images/Ambulance.png").convert_alpha()
black = pygame.image.load("images/Black_viper.png").convert_alpha()
orange = pygame.image.load("images/Car.png").convert_alpha()
blue = pygame.image.load("images/Mini_truck.png").convert_alpha()
van = pygame.image.load("images/Mini_van.png").convert_alpha()
police = pygame.image.load("images/Police.png").convert_alpha()
taxi = pygame.image.load("images/taxi.png").convert_alpha()
truck = pygame.image.load("images/truck.png").convert_alpha()

audi_rect = audi.get_rect(topleft=(200,100))
orange_rect = orange.get_rect(topleft=(600,100))
black_rect = black.get_rect(topleft=(400,100))
police_rect = police.get_rect(topleft=(800,100))
taxi_rect = taxi.get_rect(topleft=(200,500))
van_rect = van.get_rect(topleft=(400,500))
blue_rect = van.get_rect(topleft=(600,500))
truck_rect = van.get_rect(topleft=(800,500))


road = pygame.image.load("images/road.png")
road_pos=0
start_pos=[215,400,570,745]


pygame.mixer.music.load("sounds/main.wav")
pygame.mixer.music.play(loops=100)

menu=0

while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT:
            pygame.quit()
            exit()

    

    if menu==0:
        first_time = True
        screen.blit(game_window,(0,0)) # game window position
        #screen.blit(chat_window,(900,0)) # chat window position

        screen.blit(play_text,play_rect) # Play
        screen.blit(options_text,options_rect) # Options
        screen.blit(quit_text,quit_rect) # Quit


        start_car_x_pos+=5
        if start_car_x_pos>1200: start_car_x_pos=-200
        screen.blit(start_car,(start_car_x_pos,700)) # Sliding car


        if play_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                menu = 1
                time.sleep(0.2)

        elif options_rect.collidepoint(pygame.mouse.get_pos()):

            if pygame.mouse.get_pressed()[0]:
                menu = 3
        
        elif quit_rect.collidepoint(pygame.mouse.get_pos()):

            if pygame.mouse.get_pressed()[0]:
                pygame.quit()
                exit()


    elif menu==1:
        if first_time:
            
            screen.blit(game_window,(0,0)) # game window position
            screen.blit(back_text,back_rect)
            screen.blit(audi,audi_rect)
            screen.blit(orange,orange_rect)
            screen.blit(police,police_rect)
            screen.blit(black,black_rect)
            screen.blit(van,van_rect)
            screen.blit(truck,truck_rect)
            screen.blit(blue,blue_rect)
            screen.blit(taxi,taxi_rect)


            if back_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 0
            elif audi_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = audi
                        saved_car_rect = audi_rect
            elif orange_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = orange
                        saved_car_rect = orange_rect
            elif black_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = black
                        saved_car_rect = black_rect
            elif police_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = police
                        saved_car_rect = police_rect
            elif taxi_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = taxi
                        saved_car_rect = taxi_rect
            elif van_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = van
                        saved_car_rect = van_rect
            elif blue_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = blue
                        saved_car_rect = blue_rect
            if truck_rect.collidepoint(pygame.mouse.get_pos()):
                    if pygame.mouse.get_pressed()[0]:
                        menu = 2
                        saved_car = truck
                        saved_car_rect = truck_rect
                        

        

        

    elif menu==2:
        screen.blit(road,(0,road_pos-900))
        screen.blit(road,(0,road_pos))
        if first_time: x = random.choice(start_pos)
        first_time = False
        screen.blit(saved_car,(x,550))
        road_pos+=5
        if road_pos>900:
             road_pos=0


        





    elif menu==3:
        screen.blit(game_window,(0,0))
        screen.blit(back_text,back_rect)

        if back_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                menu = 0


    pygame.display.update()
    clock.tick(60) # 60 fpse