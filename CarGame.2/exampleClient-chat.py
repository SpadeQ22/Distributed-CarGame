import channel
import socket
import pickle

class Client(socket.socket):

    def __init__(self, serverLoc, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverLoc
        self.port = port
        self.connect((self.server, self.port))
        print(f"client connected to server at {self.server}:{self.port}")
        self.chan = channel.Channel()
        self.chan.bind(0)
        self.client = self.chan.join('client')
        self.server = self.chan.subgroup('server')

    def sendMsg(self):
        message = {
            'type': 'POST',
            'groupId': 'client',
            'message': {
                'user': 'Omar',
                'body': 'hello world'
            }
        }
        self.sendall(pickle.dumps(message))
        print(self.chan.recvFrom(senderSet=self.server, timeout=100))
        return

    def getLatestMessages(self):
        pass

