import logging
import pickle
import random
import socket
import sys
import time
from contextlib import contextmanager
from queue import Queue
from socketserver import BaseRequestHandler, TCPServer
from threading import Thread

import fire

from .blocks import Color, SingleBlock, GRID_HEIGHT, GRID_WIDTH

logger = logging.getLogger(__name__)


def _start_server(host, port, rcv_queue):
    class Server(BaseRequestHandler):
        def handle(self):
            data = pickle.loads(self.request.recv(1024))
            logger.info("Got %s from %s", data, self.client_address)
            rcv_queue.put(data)
            # if not rcv_queue.empty():
            #    data = rcv_queue.get()
            #    self.request.sendall(pickle.dumps(data))

    with TCPServer((host, port), Server) as server:
        server.serve_forever()


@contextmanager
def run_server(host, port):
    q = Queue()

    try:
        thread = Thread(target=_start_server, args=(host, port, q))
        thread.start()
        yield q
    finally:
        thread.join()


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_blocks(self, blocks):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.host, self.port))
            sock.sendall(pickle.dumps(blocks))

    def send_random_blocks(self):
        blocks = {}
        for _ in range(10):
            i = random.randint(0, GRID_HEIGHT)
            j = random.randint(0, GRID_WIDTH)
            blocks[(i, j)] = SingleBlock(i, j, Color.GREEN)
        self.send_blocks(blocks)


def cli():
    fire.Fire()
