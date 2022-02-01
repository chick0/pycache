from hashlib import md5

from . import STORAGE
from .log import CommandLog
from .const import LENGTH_TYPE
from .cleaner import clean_up


class Commands:
    def __init__(self, command: str, key: str, value: bytes = b""):
        self.command = command.lower()
        self.key = key
        self.value = value

    @property
    def memory(self) -> int:
        size = STORAGE.__sizeof__()
        for b in STORAGE.values():
            size += b.__sizeof__()

        return size

    def run(self) -> bytes:
        return getattr(self, "on_" + self.command)()

    def on_set(self) -> bytes:
        STORAGE.update({
            self.key: self.value
        })

        if self.memory > STORAGE.limit:
            clean_up(memory=self.memory)

        return b"updated"

    def on_get(self) -> bytes:
        return STORAGE.get(self.key, b"")

    def on_del(self) -> bytes:
        try:
            STORAGE.pop(self.key)
        except KeyError:
            return b"undefined key"

        return b""

    def on_md5(self) -> bytes:
        target = STORAGE.get(self.key, None)

        if target is None:
            return b""

        return md5(target).hexdigest().encode()


def parse_command(log: CommandLog, payload: bytes) -> bytes:
    command = payload[:3].decode()

    key_size = int.from_bytes(payload[3:4], LENGTH_TYPE)
    key = payload[4:4 + key_size].decode()

    value = payload[4 + key_size:]

    context = Commands(
        command=command,
        key=key,
        value=value
    )

    try:
        log.execute(command=command, key=key)
        result = context.run()
    except AttributeError:
        return b"undefined command"

    return result
