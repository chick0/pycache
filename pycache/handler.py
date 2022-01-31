from socketserver import BaseRequestHandler

from .log import CommandLog
from .parse import parse_command
from .const import (
    LENGTH_SIZE,
    LENGTH_TYPE
)


class PyCacheHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.log = CommandLog(client=client_address)
        super().__init__(request, client_address, server)

    def send(self, payload: bytes):
        length = len(payload)
        length = length.to_bytes(LENGTH_SIZE, LENGTH_TYPE)

        self.request.send(length)
        self.request.send(payload)

    def setup(self) -> None:
        self.log.connect()
        return

    def handle(self) -> None:
        length = self.request.recv(LENGTH_SIZE)
        length = int.from_bytes(length, LENGTH_TYPE)

        payload = self.request.recv(length)

        need_more = length - len(payload)
        while need_more:
            need_more = length - len(payload)
            payload += self.request.recv(need_more)

        result = parse_command(
            log=self.log,
            payload=payload
        )

        self.send(result)

    def finish(self) -> None:
        self.log.disconnect()
        return
