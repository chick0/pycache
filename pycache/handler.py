from socketserver import BaseRequestHandler

from .log import CommandLog
from .parse import parse_command
from .const import (
    LENGTH_SIZE,
    LENGTH_TYPE
)


class PyCacheHandler(BaseRequestHandler):
    def send(self, payload: bytes):
        length = len(payload)
        length = length.to_bytes(LENGTH_SIZE, LENGTH_TYPE)

        self.request.send(length)
        self.request.send(payload)

    def setup(self) -> None:
        CommandLog(client=self.client_address).connect()
        return

    def handle(self) -> None:
        length = self.request.recv(LENGTH_SIZE)
        length = int.from_bytes(length, LENGTH_TYPE)

        payload = self.request.recv(length)
        result = parse_command(
            log=CommandLog(client=self.client_address),
            payload=payload
        )

        self.send(result)

    def finish(self) -> None:
        CommandLog(client=self.client_address).disconnect()
        return
