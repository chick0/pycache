from . import STORAGE
from .log import CommandLog
from .const import LENGTH_TYPE


class Commands:
    def __init__(self, command: str, key: str):
        self.commands = [
            "SET",
            "GET", "DEL",
        ]

        if command in self.commands:
            self.command = command.lower()
            self.key = key
        else:
            raise TypeError

    def run(self, **kwargs) -> bytes:
        return getattr(self, "on_" + self.command)(**kwargs)

    def on_set(self, payload: bytes) -> bytes:
        msg = b"created"
        if self.key in STORAGE.keys():
            msg = b"updated"

        STORAGE.update({
            self.key: payload
        })

        return msg

    def on_get(self, **kwargs) -> bytes:
        return STORAGE.get(self.key, b"")

    def on_del(self, **kwargs) -> bytes:
        try:
            STORAGE.pop(self.key)
        except KeyError:
            return b"undefined key"

        return b""


def parse_command(log: CommandLog, payload: bytes) -> bytes:
    command = payload[:3].decode()

    key_size = int.from_bytes(payload[3:4], LENGTH_TYPE)
    key = payload[4:4 + key_size].decode()

    payload = payload[4 + key_size:]

    log.execute(command=command, key=key)

    try:
        context = Commands(
            command=command,
            key=key
        )
    except TypeError:
        return b"undefined command"

    return context.run(payload=payload)
