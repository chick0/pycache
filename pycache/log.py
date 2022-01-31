from time import time


def _log(message: str):
    now = int(time())
    print(now, message, sep=" || ")


def start(address: tuple):
    host, port = address
    address = f"'{host}:{port}'"
    _log(f"PyCache server started at {address}")


def exited(code: int):
    from sys import exit
    message = {
        0: "success",
        1: "host or port is wrong"
    }.get(code, "unknown")

    _log(f"exited! with {code}({message})")

    exit(1)


class CommandLog:
    def __init__(self, client: tuple):
        host, port = client
        self.client = f"'{host}:{port}'"

    def connect(self):
        _log(f"connected from {self.client}")

    def disconnect(self):
        _log(f"disconnected from {self.client}")

    def execute(self, command: str, key: str = None):
        _log(f"command executed '{command} {key}' from {self.client}")
