import threading
import time
from game.consumers import gameServer


class serverThreat(threading.Thread):
    def __init__(self, thread_name, thread_ID, gameServerSocket: gameServer):
        threading.Thread.__init__(self)
        self.thread_name = thread_name
        self.thread_ID = thread_ID
        self.gameServerSocket: gameServer = gameServerSocket
        print("server Worker Threat started")

    def run(self):
        running = True
        start = time.perf_counter()
        last = None
        now = time.perf_counter()

        while running:
            if not self.gameServerSocket.getRunning():
                running = False
            last = now
            now = time.perf_counter()
            time.sleep(1)
            delta = now - last
            self.gameServerSocket.update()
