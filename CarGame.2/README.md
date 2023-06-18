# Car Racing Game

 This is a multiplayer car racing game built using Python and Pygame library. It connects players over the internet to compete with each other.

## Prerequisites
* Python 3.10 was used
* Pygame library
* requests library

## Installation
1. Clone or download the repository.
2. Install pipenv: pip install pipenv
3. Navigate to the project directory in terminal/cmd prompt and run: pipenv install
4. Start the virtual environment: pipenv shell
5. Run the game: python main.py

## How to play
* Use left and right arrow keys to control the player's car.
* Avoid colliding with incoming traffic and drive as far as possible.
* Chat with other players and exchange messages while playing the game.

## Features
* Multiplayer game connecting players from different locations.
* Chat feature allows players to communicate with each other during the game.
* High score tracking system records the highest score achieved by each player.
* Internet connection check, enabling automatic reconnection to backup server if the main server is down.
* Music and sound effects for a more immersive experience.

## Developer Notes
* The code uses Pygame library to create the game window and handle user input.
* dNetwork module is used for network connectivity between players.
* threading module is used for concurrent execution of threads.
* client module is used for chat messaging functionality.
* requests library is used for checking internet connectivity.

## Acknowledgments
* The game was developed by Little B using OpenAI's product GPT-3.5.
* Special thanks to Pygame community for their documentation and tutorials on building games with Pygame.
* Credit for the music and sound effects goes to the respective artists and creators.
