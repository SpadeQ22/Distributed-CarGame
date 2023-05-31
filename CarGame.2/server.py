from dnetwork import dNetwork
from _thread import *
from car import Car

ip = "127.0.0.1"
port=5555

def client_handler(id, client,car):
    global game_network,p
    game_network.send(client, car)

    while True:
        try:
            if id==0:
                p[0]=game_network.recv(client)[0]
                game_network.send(client, [p[1], messages])
                if len(p[0]["message"])>1:
                    messages.append(p[0]["message"])
            elif id==1:
                game_network.send(client, [p[0], messages])
                p[1] = game_network.recv(client)[0]
                if len(p[1]["message"])>1:
                    messages.append(p[1]["message"])
        except:
            quit()

players_connected=0

game_network=dNetwork(ip, port)
connection=game_network.host()

connection.listen(3)
players=[Car(0),Car(1)]
p=[Car(0).to_dict(""),Car(1).to_dict("")]

messages=[]

while True:
    client,_=connection.accept()
    if players_connected!=2 :
        start_new_thread(client_handler,(players_connected,client,players[players_connected]))
        messages.append(f"Player {players_connected} is connected")
        players_connected+=1
    else:
        client.close()
