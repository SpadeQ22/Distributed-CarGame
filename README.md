# Distributed-CarGame
This GitHub repository contains the source code for a car racing game developed for a distributed computing college course. The objective of the project is to demonstrate how distributed computing can be used to enhance the performance of a game by dividing the workload among multiple machines.

## Youtube video link
https://youtu.be/g3p23vrI7fo

## Prerequisites (versions are in requirements file)
* Python 3.10 was used
* Pygame library
* requests library
* redis library

## Installation
1. Clone or download the repository.
2. install the stated above libraries
3. Run the game: python cargame.py
4. Enjoy :)

## How to play
* Enter the session number you want to join.
* Use left and right arrow keys to control the player's car.
* Avoid colliding with incoming traffic and drive as far as possible.
* Chat with other players and exchange messages while playing the game.

## Features
* Multiplayer game connecting players from different locations.
* Allows private games to play and chat only with your friends. 
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
* The game was developed by ASU students using Python coding language.
* Special thanks to Pygame community for their documentation and tutorials on building games with Pygame.

