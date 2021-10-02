from aiormq.exceptions import IncompatibleProtocolError, ConnectionClosed
from .constants import DEFAULT_COMM_URI
from .singleton import Singleton
from .utils import debug
import logging
import kiwipy
import time

class Blueprint:
    def __init__(self):
        self._broadcasts = list()
        self._tasks = list()
        self._rpcs = list()

        self.running = False
        self.debug = False
        self.comm = None

    def add_rpc(self, name):
        def decorator(f):
            rpc = (f, name,)
            self._rpcs.append(rpc)

            return f

        return decorator

    def add_task(self, name, prefetch=1):
        def decorator(f):
            task = (f, name, prefetch,)
            self._tasks.append(task)
            return f

        return decorator

    def add_broadcast(self, filters=[]):
        def decorator(f):
            broadcast = (f, filters)
            self._broadcasts.append(broadcast)
            return f

        return decorator

class Otter(Blueprint, Singleton):
    def _add_rpcs(self):
        for f, name in self._rpcs:
            f = debug(f, name) if self.debug else f
            self.comm.add_rpc_subscriber(f, name)

    def _add_tasks(self):
        for f, name, prefetch in self._tasks:
            f = debug(f, name) if self.debug else f
            queue = self.comm.task_queue(
                name, prefetch_count=prefetch
            )

            queue.add_task_subscriber(f)

    def _add_broadcasts(self):
        for f, filters in self._broadcasts:
            if filters:
                filtered = kiwipy.BroadcastFilter(f)

                for filter in filters:
                    filtered.add_subject_filter(filter)

                self.comm.add_broadcast_subscriber(filtered)

            else:
                self.comm.add_broadcast_subscriber(f)

    def register_blueprint(self, blueprint):
        self._broadcasts += blueprint._broadcasts
        self._tasks += blueprint._tasks
        self._rpcs += blueprint._rpcs

    def run(self, uri=DEFAULT_COMM_URI, debug=False):
        self.running = True
        self.debug = debug

        while self.running:
            logging.info("Running Peach")

            try:
                self.comm = kiwipy.connect(uri)

                self._add_rpcs()
                self._add_tasks()
                self._add_broadcasts()

                while True:
                    time.sleep(0.25)

            except IncompatibleProtocolError:
                logging.warning("Warming up, waiting")
                time.sleep(1)
                continue

            except (ConnectionClosed, ConnectionError, ConnectionRefusedError):
                logging.warning("Connection failed, retrying")
                time.sleep(1)
                continue

            except (KeyboardInterrupt, SystemExit):
                logging.warning("Exiting")
                self.running = False

            if self.comm and not self.running:
                self.comm.close()
