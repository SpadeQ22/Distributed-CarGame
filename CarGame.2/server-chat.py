import pickle
import socket
import threading
from channelServer import channel
import sys

class Server(socket.socket):
    def __init__(self, host, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.bind((self.host, self.port))
        # print(f"server started at  {self.host, self.port}")
        self.chan = channel.Channel()
        self.chan.join('server')
        self.workers = []

    def run(self):
        try:
            while True:
                self.listen()
                conn, client_addr = self.accept()
                thread = threading.Thread(target=self.handleConnection, args=(conn, client_addr, ))
                thread.start()
                self.workers.append(thread)
        except KeyboardInterrupt:
            sys.exit(0)
        finally:
            if self:
                self.close()
                self.chan.leave('server')
            for t in self.workers:
                t.join()

    def handleConnection(self, conn, client_addr):
        conn.setblocking(1)
        conn.settimeout(60)
        groupId = ""
        uuid = ""
        try:
            while conn:
                data = conn.recv(2048)
                message_with_meta = pickle.loads(data)
                print(f"received data from {client_addr}: {message_with_meta}")
                groupId = message_with_meta['groupId']
                uuid = message_with_meta['uuid']
                if message_with_meta['type'] == 'POST':
                    self.chan.join(message_with_meta['groupId'])
                    clients = self.chan.subgroup(message_with_meta['groupId'])
                    self.chan.sendTo(destinationSet=clients, message=message_with_meta['message'])
        except socket.timeout:
            conn.close()
            # print("time")
        except EOFError:
            conn.close()
            # print("EOF")
        except ConnectionError:
            conn.close()
            # print("ConErr")
        finally:
            self.chan.force_leave(groupId, uuid)
            self.workers.remove(threading.current_thread())
            return


if __name__ == '__main__':
    server = Server("localhost", 1234)
    server.run()
