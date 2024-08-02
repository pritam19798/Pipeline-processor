from typing import Iterator


def custom_function(lines: Iterator[str]) -> Iterator[str]:
    for line in lines:
        new_line = line.strip() + " <new custom string> \n"
        yield new_line
