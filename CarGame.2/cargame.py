import random
from dnetwork import dNetwork
import pygame


ip = "localhost"
port = 5555


class CarRacing:
    def __init__(self):
        self.car = None
        pygame.init()
        self.display_width = 1200
        self.display_height = 600
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.clock = pygame.time.Clock()
        self.gameDisplay = None
        self.n = dNetwork(ip, port)
        self.p_en = None
        self.p = None
        self.crashed = False
        self.connection = None
        self.first_try = True
        self.carImg = ['Audi', 'Black_viper']
        self.msg = ""

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
        self.chat_messages = []
        
        self.sound = pygame.mixer.music.load("sounds/main.wav")
        self.music = pygame.mixer.music.play(loops=100)
        self.initialize()

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

    def disp_car(self, x_coordinate, y_coordinate, image):
        carimage = pygame.image.load(f'images/{self.carImg[image]}.png')
        carimage = pygame.transform.scale(carimage, (150, 150))
        self.gameDisplay.blit(carimage, (x_coordinate, y_coordinate))

    def racing_window(self):
        self.gameDisplay = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption('Car Dodge')
        self.run_car()

    def run_car(self):
        if self.first_try:
            self.connection = self.n.connect()
            self.car = self.n.recv(self.connection)
            self.first_try = False

        while not self.crashed:
            # self.n.send(self.connection, [self.car.to_dict(f"{self.car.id}{self.msg}"),self.chat_messages])
            # k = self.n.recv(self.connection)

            try:
                # Attempt to send player info to server
                self.n.send(self.connection, [self.car.to_dict(f"{self.car.id}{self.msg}"), self.chat_messages])

                # Wait for response from server
                k = self.n.recv(self.connection)
                self.car.connected=True

            except Exception as e:
                # Handle other types of errors
                print("An error occurred:", e)
                print("Server Down - trying to reconnect")
                # Take appropriate action depending on the specific error
                self.connection = self.n.connect()


            else:
                # If no exceptions were raised, we can proceed with the rest of the program
                self.car2 = k[0]
                self.chat_messages = k[1]
                pass


            # try:
            #     if self.chat_messages[self.car2['id']] == f"Player {self.car2['id']} is connected":
            #         x=2
            # except:
            #     continue

            self.msg = ""

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.crashed = True

                if (event.type == pygame.KEYDOWN):
                    if event.key == pygame.K_RETURN:
                        self.add_message(self.user_input)
                        self.user_input = ""
                    if event.key == pygame.K_BACKSPACE:
                        self.user_input = self.user_input[:-1]

                    if (event.key == pygame.K_LEFT):
                        self.car.x_coordinate -= 50
                        # print("CAR X COORDINATES: %s" % self.car.x_coordinate)
                    if (event.key == pygame.K_RIGHT):
                        self.car.x_coordinate += 50
                        # print("CAR X COORDINATES: %s" % self.car.x_coordinate)
                    elif len(event.unicode) > 0:
                        # Check if key is valid (not Enter or Backspace)
                        key_code_point = ord(event.unicode)
                        if key_code_point != 13 and key_code_point != 8:
                            self.user_input += event.unicode

                    # print("x: {x}, y: {y}".format(x=self.car.x_coordinate, y=self.car.y_coordinate))

            self.gameDisplay.fill(self.black)



            self.back_ground_road()


            self.draw_chat_box()
            input_surface = self.font.render(self.user_input, True, self.WHITE)
            input_rect = input_surface.get_rect()
            input_rect.bottomleft = (0, self.display_height)
            self.gameDisplay.blit(input_surface, input_rect)

            self.run_enemy_car(self.enemy_car_startx, self.enemy_car_starty)
            self.enemy_car_starty += self.enemy_car_speed

            if self.enemy_car_starty > self.display_height:
                self.enemy_car_starty = 0 - self.enemy_car_height
                self.enemy_car_startx = random.randrange(200, self.display_width-250)

            self.disp_car(self.car2["x_coordinate"], self.car2["y_coordinate"], self.car2["id"])
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

            pygame.display.update()
            self.clock.tick(60)

    def display_message(self, msg):
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",72)
        text = font.render(msg, True, (255, 255, 255))
        self.gameDisplay.blit(text, (300, 240 - text.get_height() // 2))
        self.display_credit()
        pygame.display.update()
        self.clock.tick(60)
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
        self.gameDisplay.blit(text, (900, 0))
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",20)
        car2id, car2hs = self.car2["id"], self.car2["high_score"]
        text = font.render(f"P{car2id} high Score : {str(car2hs)}", True, self.white)
        self.gameDisplay.blit(text, (18, 50))

    def display_credit(self):
        font = pygame.font.Font("fonts/Valorax-lg25V.otf",14)
        text = font.render("Thanks for playing!", True, self.white)
        self.gameDisplay.blit(text, (510, 520))

    def add_message(self, message):
        # self.chat_messages.append(f'ME: {message}')
        self.msg = message

    # Define a function to draw the chat box and messages
    def draw_chat_box(self):
        # Clear the chat box surface
        msg_y_offset = 0
        self.chat_box_surface.fill(self.WHITE)

        # Draw the messages onto the chat box surface

        for message in self.chat_messages[-1:1:-1]:
            id = message[0]
            if int(id) == self.car.id:
                message = f'ME : {message[1:]}'
                f'ME : {message[1:]}'
            else:
                message = f'P{id} : {message[1:]}'
            message_surface = self.font.render(message, True, self.BLACK)
            self.chat_box_surface.blit(message_surface, (5, msg_y_offset))
            msg_y_offset += message_surface.get_height() + 1

        # Draw the chat box surface onto the main screen
        chat_box_x = self.display_width - self.CHAT_BOX_WIDTH - 10  # 10-pixel margin
        chat_box_y = self.display_height - self.CHAT_BOX_HEIGHT - 30  # 10-pixel margin
        self.gameDisplay.blit(self.chat_box_surface, (chat_box_x, chat_box_y))


if __name__ == "__main__":
    car_racing = CarRacing()
    car_racing.racing_window()
