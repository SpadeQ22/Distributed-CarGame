from _thread import *
import json,redis,socket,pickle

flag=False
redis_client = redis.Redis(host="redis-12791.c44.us-east-1-2.ec2.cloud.redislabs.com", port=12791, db=0, password='bg17VYxIffU1IyzMvsiaZ1xLY5xxbpeU')


ip = "0.0.0.0"
port = 1225

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

    def to_dict(self):
        return {'id': self.id, 'x_coordinate': self.x_coordinate, 'y_coordinate': self.y_coordinate,'high_score': self.high_score}


class dNetwork:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

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

def delete_game_state(session_id):
    key = f"game:{session_id}"
    value = redis_client.get(key)
    if value:
        redis_client.delete(key)
        return True
    else:
        # print(f"No game state found for session {session_id}")
        return False


def getID(arr):
    i = 0
    while True:
        if i not in arr:
            return i
        i += 1
        if i > 4:
            return -1

players_inSession=get_game_state(0)
players_inSession = {int(key): value for key, value in players_inSession.items()}

x="Y"
if x=="Y":
    save_game_state(0,{})
    for session in players_inSession:
        delete_game_state(session)
    players_inSession=get_game_state(0)
    players_inSession = {int(key): value for key, value in players_inSession.items()}


players_connected = 0
game_network = dNetwork(ip, port)
connection = game_network.host()

num_of_players = 12
connection.listen(num_of_players)
sessionsState={}


def remove_player(id,session):
    players_inSession = get_game_state(0)
    players_inSession={int(key): value for key, value in players_inSession.items()}
    players_inSession[session].remove(id)
    for d in sessionsState[session]:
            if d["id"] == id:
                sessionsState[session].remove(d)
                break

    if len(players_inSession[session])==0:
        del players_inSession[session]
        del sessionsState[session]
        delete_game_state(session)
    else:
        save_game_state(session, sessionsState[session])

    save_game_state(0, players_inSession)



def client_handler(id, client,session):
    global game_network,players_connected
    sessionsState[session] = get_game_state(session)
    while not flag:

        try:
            y=game_network.recv(client)
            if y=="EXIT" or y=="exit":
                remove_player(id,session)
                exit()
            st=sessionsState[session]
            list = [x for x in st if x["id"] != id]

            for i in range(len(st)):
                if st[i]["id"] == id:
                    sessionsState[session][i] = y
                    break
            game_network.send(client, list)
        except Exception as e:
            pass

def wait_for_client():
    global players_connected,flag
    while not flag:

        try:
            client, _ = connection.accept()
        except:
            flag = True
            quit()
        if players_connected != num_of_players:
            connectionInfo=game_network.recv(client)
            id = int(connectionInfo[0])
            session=int(connectionInfo[1])
            players_inSession=get_game_state(0)
            players_inSession = {int(key): value for key, value in players_inSession.items()}
            if session not in players_inSession:
                # print("New session\n\n")
                players_inSession[session] =[]
                save_game_state(session,[])
            if id==-1:
                id=getID(players_inSession[session])
                if id==-1:
                    print("Session full")
                    continue
                players_inSession[session].append(id)
                car = Car(id)
                p=get_game_state(session)
                p.append(car.to_dict())
                save_game_state(session,p)
                game_network.send(client, car)
                save_game_state(0, players_inSession)
            start_new_thread(client_handler, (id, client,session))
            players_connected += 1
        else:
            client.close()
            flag=True


wait_for_client()
