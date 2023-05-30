import socket
import pickle

class dNetwork:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def connect(self):
        try:
            self.connection.connect((self.ip,self.port))
            print("Successfully connected")
            return self.connection
        except:
            print("Server unreachable")

    def host(self):
        try:
            self.connection.bind((self.ip,self.port))
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