from .constants import DEFAULT_COMM_URI
import kiwipy

class Client:
    def __init__(self, uri=DEFAULT_COMM_URI):
        self.comm = self._connect(uri)

    def _connect(self, uri):
        try:
            return kiwipy.connect(uri)
        except Exception:
            return None

    def broadcast(self, body, sender=None, subject=None, correlation_id=None):
        if self.comm:
            return self.comm.broadcast_send(
                body, sender, subject, correlation_id
            )

        return None

    def rpc(self, recepient, payload):
        if self.comm:
            return self.comm.rpc_send(
                recepient, payload
            )

        return None

    def task(self, recepient, payload):
        if self.comm:
            queue = self.comm.task_queue(recepient)
            return queue.task_send(
                payload
            )

        return None

    def close(self):
        if self.comm:
            self.comm.close()
