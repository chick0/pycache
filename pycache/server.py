from os import environ
from socketserver import TCPServer

from .log import start
from .log import exited
from .handler import PyCacheHandler
from .const import (
    PYCACHE_HOST,
    PYCACHE_PORT,

    DEFAULT_HOST,
    DEFAULT_PORT,
)


def start_server():
    try:
        server_address = (
            environ.get(PYCACHE_HOST, DEFAULT_HOST),
            int(environ.get(PYCACHE_PORT, DEFAULT_PORT))
        )
    except ValueError:
        server_address = (None, None)
        exited(1)

    start(address=server_address)
    server = TCPServer(server_address, PyCacheHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        exited(0)


if __name__ == "__main__":
    start_server()
