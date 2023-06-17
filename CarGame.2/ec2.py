from _thread import *
import time,json,redis,socket,pickle,subprocess
from cargame import abc
redis_client = redis.Redis(host="redis-12791.c44.us-east-1-2.ec2.cloud.redislabs.com", port=12791, db=0, password='bg17VYxIffU1IyzMvsiaZ1xLY5xxbpeU')
flag=False

if abc:
    ip = "172.31.47.236"
    port = 8000
else:
    ip = "localhost"
    port = 55555

class Car:
    def __init__(self,id):
        self.display_width = 1200
        self.display_height = 600
        self.x_coordinate = None
        self.y_coordinate = None
        self.high_score = 0
        self.pending_message=False
        self.id=id
        self.initialize()

    def initialize(self):
        self.x_coordinate = 600
        self.y_coordinate = (self.display_height * 0.75)
        self.width = 49
        self.connected=False

    def to_dict(self,message):
        return {'id': self.id, 'x_coordinate': self.x_coordinate, 'y_coordinate': self.y_coordinate,'high_score': self.high_score,
                'message': message}
    @staticmethod
    def retrieve_car(car):
        newcar=Car(car["id"])
        newcar.x_coordinate=car["x_coordinate"]
        newcar.y_coordinate = car["y_coordinate"]
        newcar.high_score = car["high_score"]
        return newcar

class dNetwork:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def check_server(self):
        port=80
        cmd = f"netstat -aon | findstr :{port}"
        output = subprocess.getoutput(cmd)
        return f"LISTENING" in output

    def connect(self):
        try:
            self.connection.connect((self.ip,self.port))
            print("Successfully connected")
            self.send(self.connection, -1)
            return self.connection
        except:
            print("Server unreachable")


    def reconnect(self,id):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip,self.port))
            self.send(self.connection,id)
            print("Successfully connected")
            return self.connection
        except:
            print("Server unreachable")

    def host(self):
        try:
            self.connection.bind((self.ip,self.port))
            self.serverconnected=True
            print("Server started")
            return self.connection
        except:
            print("Operation Failed")

    def send(self,connection,data):
        data=pickle.dumps(data)
        data_length=str(len(data))
        data_length=(8-len(data_length))*'0'+data_length
        connection.send(data_length.encode())
        connection.send(data)

    def recv(self,connection):
        data_length=connection.recv(8)
        data=connection.recv(int(data_length))
        return pickle.loads(data)

# Save game state to Redis
def save_game_state(session_id, game_state):
    key = f"game:{session_id}"
    value = json.dumps(game_state)
    result = redis_client.set(key, value)
    if result:
        pass
        # print(f"Saved game state for session {session_id}")
    else:
        pass
        # print(f"Error saving game state for session {session_id}")

# Retrieve game state from Redis
def get_game_state(session_id):
    key = f"game:{session_id}"
    value = redis_client.get(key)
    if value:
        game_state = json.loads(value)
        return game_state
    else:
        pass
        # print(f"No game state found for session {session_id}")
        return None

def checkpoint(pn):
    global last_call_time
    current_time = time.time()
    if current_time - last_call_time >= 30:
        last_call_time = current_time
        save_game_state(1, pn)


last_call_time = time.time()
players_connected = 0
game_network = dNetwork(ip, port)
connection = game_network.host()

num_of_players = 5
connection.listen(num_of_players)

p = []
messages = []

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

    while not flag:
        try:
            # checkpoint(p)
            list = [x for x in p if x["id"] != id]
            p[id] = game_network.recv(client)[0]
            game_network.send(client, [list, messages])
            if len(p[id]["message"]) > 1:
                messages.append(p[id]["message"])
        except:
            pass

def wait_for_client():
    global flag
    global players_connected
    while not flag:

        try:
            client, _ = connection.accept()
        except:
            flag = True
            quit()
        if players_connected != num_of_players:
            id = int(game_network.recv(client)[0])
            session=int(game_network.recv(client)[1])
            if id==-1:
                id=players_connected
            car = Car(players_connected)
            p=get_game_state(session)
            p.append(car.to_dict(""))
            save_game_state(session,p)
            game_network.send(client, car)
            start_new_thread(client_handler, (id, client))
            players_connected += 1
        else:
            client.close()
            flag=True


wait_for_client()