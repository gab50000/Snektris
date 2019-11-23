import logging
import pickle
import socket
import sys
from socketserver import BaseRequestHandler, TCPServer
from threading import Thread
import time
from queue import Queue


logger = logging.getLogger(__name__)


def run_server(host, port, queue):
    class Server(BaseRequestHandler):
        def handle(self):
            data = pickle.loads(self.request.recv(1024))
            print("Got", data)
            queue.put(data)
            # just send back the same data, but upper-cased
            # self.request.sendall(pickle.dumps(np.ascontiguousarray(data.T)))

    with TCPServer((host, port), Server) as server:
        server.serve_forever()


q = Queue()

try:
    thread = Thread(target=run_server, args=("localhost", 8080, q))
    thread.start()

    for _ in range(20):
        if q.full():
            print(q.get())
        else:
            print("Nothing")
        time.sleep(3)
finally:
    thread.join()
