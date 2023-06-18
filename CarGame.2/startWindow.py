import pygame

def get_user_input():
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock() # fps


    # Set up the window
    screen_width, screen_height = 1200, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Enter Session ID")
    # Define colors and fonts   
    white = (255, 255, 255)
    black = (0, 0, 0)
    font_size = 60
    font = pygame.font.Font("fonts/TechnoRaceItalic-eZRWe.otf", font_size)

    play_text = font.render("Play",False, (128, 128, 128))
    play_rect = play_text.get_rect(topleft= (screen_width//2 -50,150))

    quit_text = font.render("Quit",True,white)
    quit_rect = play_text.get_rect(topleft= (screen_width//2 -50,350))

    # Define text input box
    text_input_box_width, text_input_box_height = 420, 70
    text_input_box_rect = pygame.Rect(screen_width//2 - text_input_box_width//2,
                                      screen_height//2 - text_input_box_height//2 - 25,
                                      text_input_box_width, text_input_box_height)
    text_input_box_color = white
    text_input_box_active_color = (200, 200, 200)
    screen.blit(play_text,play_rect) # Play
    screen.blit(quit_text,quit_rect) # Quit


    car_window = pygame.Surface((screen_width,200))
    start_car = pygame.image.load("images/start_car.png").convert_alpha()
    start_car_x_pos=-200

    # Start the input loop
    getting_input = True
    user_text = ''
    while getting_input:
        start_car_x_pos+=5
        if start_car_x_pos>1200: start_car_x_pos=-200
        screen.blit(car_window,(start_car_x_pos-5,400))
        screen.blit(start_car,(start_car_x_pos,500)) # Sliding car
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                getting_input = False
                pygame.quit()
                exit()

            elif play_rect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    getting_input = False

            elif quit_rect.collidepoint(pygame.mouse.get_pos()):

                if pygame.mouse.get_pressed()[0]:
                    pygame.quit()
                    exit()

            elif event.type == pygame.KEYDOWN:
                # Handle backspace
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                # Handle return key
                elif event.key == pygame.K_RETURN:
                    getting_input = False
                # Handle any other key pressed
                else:
                    user_text += event.unicode

        # Draw input box with user text
        if user_text:
            user_text_surface = font.render(user_text, True, black)
            play_text = font.render("Play",True,white)
        else:
            user_text_surface = font.render("Enter Session ID", True, (128, 128, 128))
        text_input_box_color = text_input_box_active_color if getting_input else white
        pygame.draw.rect(screen, text_input_box_color, text_input_box_rect, border_radius=5)
        screen.blit(user_text_surface, (text_input_box_rect.x + 10, text_input_box_rect.y + 10))
        screen.blit(play_text,play_rect) # Play
        # Update the screen
        pygame.display.update()
        clock.tick(60) # 60 fps

    # Clean up and return user input
    pygame.quit()
    return user_text




