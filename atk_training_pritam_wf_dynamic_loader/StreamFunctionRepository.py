from atk_training_pritam_wf_dynamic_loader.base_clases import BaseFunctionRepository
from typing import Iterator


class StreamFunctionRepository(BaseFunctionRepository):

    def get_function_lookup(self) -> dict:
        return {
            "number_the_lines": self._number_the_lines,
            "coalesce_empty_lines": self._coalesce_empty_lines,
            "remove_empty_lines": self._remove_empty_lines,
            "remove_even_lines": self._remove_even_lines,
            "break_lines": self._break_lines,
        }

    def _number_the_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        for i, line in enumerate(lines, start=1):
            yield f"{i}: {line}"

    def _coalesce_empty_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        empty_line_found = False
        for line in lines:
            if line.strip() == "":
                if not empty_line_found:
                    empty_line_found = True
                    yield line
            else:
                empty_line_found = False
                yield line

    def _remove_empty_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        for line in lines:
            if line.strip() != "":
                yield line

    def _remove_even_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        for i, line in enumerate(lines, start=1):
            if i % 2 != 0:
                yield line

    def _break_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        # max_length: int = 20
        if 'max_length' in kwargs:
            max_length: int = kwargs['max_length']
        else:
            max_length: int = 20
        for line in lines:
            if line.strip() == "":
                yield line  # Don't modify empty lines.
            else:
                while len(line) > max_length:
                    yield line[:max_length] + '\n'
                    line = line[max_length:]
                if line:  # Yield remaining non-empty line after breaking.
                    yield line


