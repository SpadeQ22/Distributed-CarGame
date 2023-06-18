import socket
import pickle
import subprocess

class dNetwork:
    def __init__(self,ip,port):
        self.ip=ip
        self.port=port
        self.connection=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def check_server(self):
        cmd = f"netstat -aon | findstr :{self.port}"
        output = subprocess.getoutput(cmd)
        return f"LISTENING" in output

    def connect(self,session):
        try:
            self.connection.connect((self.ip,self.port))
            print("Successfully connected")
            self.send(self.connection, [-1,session])
            return self.connection
        except:
            print("Server unreachable")


    def reconnect(self,id,session):
        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.ip,self.port))
            self.send(self.connection,[id,session])
            print("Successfully reconnected")
            return self.connection
        except:
            print("Server unreachable")
            return -1

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