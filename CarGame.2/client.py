
import sys
import threading
import time

import channel
import socket
import pickle

# REDIS_PRIMARY_LOCATION = 'localhost'
# REDIS_PRIMARY_PORT = 32771
#
# REDIS_SECONDARY_LOCATION = 'localhost'
# REDIS_SECONDARY_PORT = 30777

class Client(socket.socket):

    def __init__(self, serverLoc, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverLoc
        self.port = port
        self.connect((self.server, self.port))
        print(f"client connected to server at {self.server}:{self.port}")
        self.chan = channel.Channel()
        self.uuid = self.chan.join('client')
        self.chan.subgroup('server')



    def sendMsg(self):
        message = {
            'type': 'POST',
            'groupId': 'client',
            'uuid': self.uuid,
            'message': {
                'user': 'Omar0',
                'body': 'hello world'
            }
        }
        self.sendall(pickle.dumps(message))
        # print(self.chan.recvFrom(senderSet=self.server, timeout=100))
        return

    def getLatestMessages(self):
        while True:
            time.sleep(1)
            servers = self.chan.subgroup('server')
            self.chan.join('client')
            print(self.chan.recvFrom(servers, timeout=100))


if __name__ == '__main__':
    cli = Client("18.207.221.238", 1234)
    thread = threading.Thread(target=cli.getLatestMessages, args=())
    thread.start()
    try:
        while True:
            try:
                cli.sendMsg()
                time.sleep(10)
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        cli.close()
        sys.exit(0)