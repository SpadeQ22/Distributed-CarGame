from dnetwork import dNetwork
from _thread import *
from car import Car
import time
from backup import save_game_state, get_game_state
import threading

lock = threading.Lock()

flag=True
ip = "localhost"
port = 55555
last_call_time = time.time()
players_connected = 0

def checkpoint(pn):
    global last_call_time
    current_time = time.time()
    if current_time - last_call_time >= 30:
        last_call_time = current_time
        save_game_state(1, pn)


game_network = dNetwork(ip, port)
connection = game_network.host()

num_of_players = 2
connection.listen(num_of_players)

p = []
messages = []


def wait_for_client():
    global players_connected
    while True:
        if flag:
            client, _ = connection.accept()

        if players_connected != num_of_players:
            id = int(game_network.recv(client))
            if id==-1:
                id=players_connected
            car = Car(players_connected)
            p.append(car.to_dict())
            save_game_state(1,p)
            game_network.send(client, car)
            start_new_thread(client_handler, (id, client))
            players_connected += 1
        else:
            client.close()

def client_quit(id):
    global players_connected
    client, _ = connection.accept()
    reconn_id = int(game_network.recv(client))
    if reconn_id == -1:
        reconn_id = id
    car=Car.retrieve_car(p[id])
    game_network.send(client, car)
    start_new_thread(client_handler, (reconn_id, client))
    players_connected += 1

def client_handler(id, client):
    global game_network, p,players_connected
    p = get_game_state(1)

    while True:
        try:
            # checkpoint(p)
            list = [x for x in p if x["id"] != id]
            p[id] = game_network.recv(client)[0]
            game_network.send(client, [list, messages])
            if len(p[id]["message"]) > 1:
                messages.append(p[id]["message"])
                print(messages)
        except:
            client_quit(id)
            quit()

wait_for_client()