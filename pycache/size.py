UPPER = 1024

KB = 1 * 1024
MB = KB * UPPER
GB = MB * UPPER


def parse_size(size: str) -> int:
    size = size.upper()

    units = {}
    [units.update({
        x: globals().get(x)
    }) for x in globals().keys() if not x.startswith("_") and len(x) == 2 and x.endswith("B")]

    try:
        unit = [x for x in units if x in size][0]
    except IndexError:
        unit = "MB"

    number = int(size.replace(unit, ""))

    return number * units.get(unit, KB)
