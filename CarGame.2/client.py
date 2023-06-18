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

    def __init__(self, serverLoc, port, id,groupid,uuid):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.server = serverLoc
        self.port = port
        self.id=id
        self.groupid=groupid
        self.connect((self.server, self.port))
        print(f"client connected to server at {self.server}:{self.port}")
        self.chan = channel.Channel(uuid=uuid)
        self.uuid = self.chan.join(f"{self.groupid}")
        self.chan.subgroup('server')
        self.servers = self.chan.subgroup('server')
        self.chan.join(f"{self.groupid}")



    def sendMsg(self,msg):
        message = {
            'type': 'POST',
            'groupId': f"{self.groupid}",
            'uuid': self.uuid,
            'message': {
                'user': f'{self.id}',
                'body': msg
            }
        }
        self.sendall(pickle.dumps(message))
        return

    def getLatestMessages(self):
        while True:
            time.sleep(1)
            servers = self.chan.subgroup('server')
            self.chan.join(f"{self.groupid}")
            x=self.chan.recvFrom(servers, timeout=1)
            if x!=None:
                print(x)

    def getmsgs(self):
        while True:
            time.sleep(0.5)
            x = self.chan.recvFrom(self.servers, timeout=1)
            return x


if __name__ == '__main__':
    cli = Client("18.207.221.238", 1234,2,2)
    thread = threading.Thread(target=cli.getLatestMessages, args=())
    thread.start()
    try:
        while True:
            try:
                cli.sendMsg("4")
                time.sleep(10)
            except KeyboardInterrupt:
                break
    except KeyboardInterrupt:
        cli.close()
        sys.exit(0)

