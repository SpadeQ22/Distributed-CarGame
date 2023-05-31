import pickle
import socket
import threading
import os
import channel

class Server(socket.socket):
    def __init__(self, host, port):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.bind((self.host, self.port))
        print(f"server started at  {self.host, self.port}")
        self.chan = channel.Channel(0, flush=True)
        self.chan.bind(0)
        self.server = self.chan.join('server')
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
            print("Stopped")
        finally:
            if self:
                self.close()
            for t in self.workers:
                t.join()

    def handleConnection(self, conn, client_addr):
        conn.setblocking(1)
        conn.settimeout(240)
        try:
            while conn:
                data = conn.recv(2048)
                message_with_meta = pickle.loads(data)
                print(f"received data from {client_addr}: {message_with_meta}")
                if message_with_meta['type'] == 'POST':
                    self.chan.join(message_with_meta['groupId'])
                    clients = self.chan.subgroup(message_with_meta['groupId'])
                    self.chan.sendTo(destinationSet=clients, message=message_with_meta['message'])
        except socket.timeout:
            conn.close()
        except EOFError:
            conn.close()




if __name__ == '__main__':
    server = Server("localhost", 1234)
    server.run()
