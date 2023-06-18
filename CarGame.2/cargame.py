import sys
import random
import uuid

import client
from dnetwork import dNetwork
import pygame
from car import Car
import threading
from startWindow import get_user_input
import requests



mainserver=["54.147.131.181",1225]
backupserver=["3.90.4.16",1225]

class CarRacing:
    def __init__(self,sessid):
        self.mains = dNetwork(mainserver[0], mainserver[1])
        self.uuid=uuid.uuid4()
        self.chat_messages=[]
        self.messageClient =None
        self.exit = False
        self.chat_update_required = True
        self.session=sessid
        self.car = Car
        pygame.init()
        self.display_width = 1200
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.network = dNetwork(mainserver[0],mainserver[1])
        self.cars=[]
        self.p_en = None
        self.p = None
        self.crashed = False
        self.connection = None
        self.first_try = True
        self.carImg = ['Audi', 'Black_viper', 'taxi', 'truck', 'Ambulance', 'Mini_truck']
        self.enemy=None

        self.BLACK = (0, 0, 0)
        self.msg_y_offset = 5
        self.WHITE = (255, 255, 255)
        self.CHAT_BOX_WIDTH = 200
        self.CHAT_BOX_HEIGHT = 300
        self.chat_box_surface = pygame.Surface((self.CHAT_BOX_WIDTH, self.CHAT_BOX_HEIGHT))
        self.chat_box_surface.fill(self.WHITE)
        self.chat_box_surface.set_colorkey(self.WHITE)

        self.user_input = ""
        self.font = pygame.font.Font("fonts/Valorax-lg25V.otf",14)


        self.sound = pygame.mixer.music.load("sounds/main.wav")
        self.music = pygame.mixer.music.play(loops=100)
        self.initialize()

    import threading
    import sys

    # Define a function to stop all threads
    def stop_threads(self):
        # Get all active threads
        for thread in threading.enumerate():
            # Set the "stop" flag for each thread
            thread.stop()

    def check_internet(self):
        try:
            response = requests.get('https://www.google.com')
            return True
        except:
            return False

    def initialize(self):

        if self.crashed:
            self.car.initialize()

        self.crashed = False

        # enemy_car
        self.enemy_car = pygame.image.load("images/Police.png")
        self.enemy_car = pygame.transform.scale(self.enemy_car,(150,150))
        self.enemy_car_startx = random.randrange(310, 450)
        self.enemy_car_starty = -600
        self.enemy_car_speed = 5
        self.enemy_car_width = 49
        self.enemy_car_height = 100

        # Background
        self.bgImg = pygame.image.load("images/road.png")
        self.bg_x1 = (self.display_width) - (1200)
        self.bg_x2 = (self.display_width) - (1200)
        self.bg_y1 = 0
        self.bg_y2 = -600
        self.bg_speed = 3
        self.count = 0
        self.connthread = threading.Thread(target=self.sendServer, args=())
        self.chatThread = threading.Thread(target=self.handlemessaging, args=())

    def disp_car(self, x_coordinate, y_coordinate, image):
        carimage = pygame.image.load(f'images/{self.carImg[image]}.png')
        carimage = pygame.transform.scale(carimage, (150, 150))
        self.gameDisplay.blit(carimage, (x_coordinate, y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def runget(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.crashed = True
            if (event.type == pygame.KEYDOWN):
                if event.key == pygame.K_ESCAPE:
                    return True
                if event.key == pygame.K_RETURN:
                    if self.user_input=="q" or self.user_input=="Q":
                        return True
                    elif self.user_input=="cheat" or self.user_input=="cheat":
                        self.car.high_score+=2000
                    self.messageClient.sendMsg(self.user_input)
                    self.user_input = ""
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                if (event.key == pygame.K_LEFT):
                    self.car.x_coordinate -= 50
                if (event.key == pygame.K_RIGHT):
                    self.car.x_coordinate += 50
                elif len(event.unicode) > 0:
                    # Check if key is valid (not Enter or Backspace)
                    key_code_point = ord(event.unicode)
                    if key_code_point != 13 and key_code_point != 8:
                        self.user_input += event.unicode
            return False
    def handlemessaging(self):
        while True:
            if self.exit:
                exit()
            x = self.messageClient.getmsgs()
            if x!=None:
                string=f"{x[-1]['user']}{x[-1]['body']}"
                self.chat_update_required=True
                self.draw_chat_box(string)

    def sendServer(self):
        while True:
            try:
                if self.exit:
                    self.network.send(self.connection, "EXIT")
                    exit()
                    sys.exit(0)
                self.network.send(self.connection, self.car.to_dict())
                self.enemy = self.network.recv(self.connection)
                self.car.connected = True
            except Exception as e:
                if not self.check_internet():
                    print("Please connect to the internet")
                else:
                    try:
                        try:
                            self.network =self.mains
                            self.connection = self.network.reconnect(self.car.id, self.session)
                        except:
                            self.network= dNetwork(backupserver[0],backupserver[1])
                            self.connection = self.network.reconnect(self.car.id, self.session)
                    except:
                        print("Unable to reconnect")
            else:
                # If no exceptions were raised, we can proceed with the rest of the program
                self.cars = self.enemy



    def run_car(self):
        if self.first_try:
            self.connection = self.network.connect(self.session)
            self.car = self.network.recv(self.connection)
            self.first_try = False

            self.connthread.start()
            self.messageClient=client.Client("NLB-Chat-Servers-681167bf072b08e3.elb.us-east-1.amazonaws.com", 1234, self.car.id, self.session,uuid=self.uuid)
            self.chatThread.start()

        while not self.crashed:
            self.exit=self.runget()
            if self.exit:
                print(self.exit)
                exit()
                sys.exit(0)


            self.gameDisplay.fill(self.black)
            self.back_ground_road()

            input_surface = self.font.render(self.user_input, True, self.WHITE)
            input_rect = input_surface.get_rect()
            input_rect.bottomleft = (0, self.display_height)
            self.gameDisplay.blit(input_surface, input_rect)

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(200, self.display_width-250)

            l = int(len(self.cars))
            for i in range(l):
                self.disp_car(self.cars[i]["x_coordinate"], self.cars[i]["y_coordinate"], self.cars[i]["id"])

            self.disp_car(self.car.x_coordinate, self.car.y_coordinate, self.car.id)
            self.highscore(self.count)

            if self.count > self.car.high_score:
                self.car.high_score = self.count

            self.hscore()

            self.count += 1
            if (self.count % 100 == 0):
                self.enemy_car_speed += 1
                self.bg_speed += 1
            if self.car.y_coordinate < self.enemy_car_starty + self.enemy_car_height:
                if self.car.x_coordinate > self.enemy_car_startx and self.car.x_coordinate < self.enemy_car_startx + self.enemy_car_width or self.car.x_coordinate + self.car.width > self.enemy_car_startx and self.car.x_coordinate + self.car.width < self.enemy_car_startx + self.enemy_car_width:
                    self.crashed = True
                    self.display_message("Game Over !!!")

            if self.car.x_coordinate < 160 or self.car.x_coordinate > self.display_width-300:
                self.crashed = True
                self.display_message("Game Over !!!")

            self.draw_chat_box("")
            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",72)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (300, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(30)
        pygame.time.delay(1000)
        self.initialize()
        self.racing_window()

    def back_ground_road(self):
        self.gameDisplay.blit(self.bgImg, (self.bg_x1, self.bg_y1 - 900))
        self.gameDisplay.blit(self.bgImg, (self.bg_x2, self.bg_y1))

        self.bg_y1 += self.bg_speed
        self.bg_y2 += self.bg_speed

        if self.bg_y1 >= 900:
            self.bg_y1 = 0



    def run_enemy_car(self, thingx, thingy):
        self.gameDisplay.blit(self.enemy_car, (thingx, thingy))

    def highscore(self, count):
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",20)
        text = font.render("Current score : " + str(count), True, self.white)
        self.gameDisplay.blit(text, (18, 0))

    def hscore(self):
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",20)
        text = font.render(f"High Score : {str(self.car.high_score)}", True, self.white)
        self.gameDisplay.blit(text, (18, 50))
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",20)
        text = font.render("High Scores", True, self.white)
        self.gameDisplay.blit(text, (1000, 0))

        l = len(self.cars)
        id_score=[]

        for d in self.cars:
            id_score.append((d["id"], d["high_score"]))

        id_score.append((self.car.id, self.car.high_score))

        id_score = sorted(id_score, key=lambda x: x[1], reverse=True)

        i=1
        for score in id_score:
            carid, carhs = score[0], score[1]
            if carid==self.car.id:
                score = f"You: {str(carhs)}"
            else:
                score = f"P{carid}: {str(carhs)}"

            text = font.render(score, True, self.white)
            self.gameDisplay.blit(text, (1000, i*50))
            i+=1

    def display_credit(self):
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (510, 520))

    # Define a function to draw the chat box and messages
    def draw_chat_box(self,newmsg):
        # Clear the chat box surface
        msg_y_offset = 0

        # Draw the messages onto the chat box surface
        if self.chat_update_required and newmsg!="":
            self.chat_messages.append(newmsg)
            self.chat_box_surface.fill(self.WHITE)
            for message in self.chat_messages[-1::-1]:
                id = message[0]
                if int(id) == self.car.id:
                    message = f'ME : {message[1:]}'
                    f'ME : {message[1:]}'
                else:
                    message = f'P{id} : {message[1:]}'
                message_surface = self.font.render(message, True, self.BLACK)
                self.chat_box_surface.blit(message_surface, (5, msg_y_offset))
                msg_y_offset += message_surface.get_height() + 1
                self.chat_update_required=False

        # Draw the chat box surface onto the main screen
        chat_box_x = self.display_width - self.CHAT_BOX_WIDTH - 10  # 10-pixel margin
        chat_box_y = self.display_height - self.CHAT_BOX_HEIGHT - 30  # 10-pixel margin
        self.gameDisplay.blit(self.chat_box_surface, (chat_box_x, chat_box_y))


if __name__ == "__main__":
    sessid=int(get_user_input())
    car_racing = CarRacing(sessid)
    car_racing.racing_window()
