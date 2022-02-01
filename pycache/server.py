from os import environ
from socketserver import TCPServer

from .log import start
from .log import exited
from .handler import PyCacheHandler
from . import STORAGE
from .size import (parse_size, MB)
from .const import (
    PYCACHE_HOST,
    PYCACHE_PORT,
    PYCACHE_STORAGE_MAX,

    DEFAULT_HOST,
    DEFAULT_PORT,
    DEFAULT_STORAGE_MAX
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

    try:
        size = parse_size(size=environ.get(PYCACHE_STORAGE_MAX))
    except (AttributeError, ValueError):
        size = DEFAULT_STORAGE_MAX * MB

    STORAGE.limit = size

    start(address=server_address, size=size)
    server = TCPServer(server_address, PyCacheHandler)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        exited(0)


if __name__ == "__main__":
    start_server()
