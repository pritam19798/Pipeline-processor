from PipelineProcessor.base_clases import BaseFunctionRepository
from typing import Iterator

class StreamFunctionRepository(BaseFunctionRepository):
    """
    A repository class that provides streaming text transformation functions.
    Each function is designed to process an iterator of strings, applying specific transformations
    like numbering lines, removing or coalescing empty lines, and breaking long lines.
    """

    def get_function_lookup(self) -> dict:
        """
        Returns a dictionary mapping function names to their corresponding streaming transformation functions.

        Returns:
            dict: A dictionary with keys as function names and values as the transformation functions.
        """
        return {
            "number_the_lines": self._number_the_lines,
            "coalesce_empty_lines": self._coalesce_empty_lines,
            "remove_empty_lines": self._remove_empty_lines,
            "remove_even_lines": self._remove_even_lines,
            "break_lines": self._break_lines,
        }

    def _number_the_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        """
        Adds a line number before each line of text.

        Args:
            lines (Iterator[str]): An iterator of strings to be numbered.

        Yields:
            Iterator[str]: An iterator where each string is prefixed with its line number.
        """
        for i, line in enumerate(lines, start=1):
            yield f"{i}: {line}"

    def _coalesce_empty_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        """
        Coalesces multiple consecutive empty lines into a single empty line.

        Args:
            lines (Iterator[str]): An iterator of strings from which to coalesce empty lines.

        Yields:
            Iterator[str]: An iterator of strings with consecutive empty lines coalesced.
        """
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
        """
        Removes all empty lines from the text.

        Args:
            lines (Iterator[str]): An iterator of strings from which to remove empty lines.

        Yields:
            Iterator[str]: An iterator of strings without empty lines.
        """
        for line in lines:
            if line.strip() != "":
                yield line

    def _remove_even_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        """
        Removes even-numbered lines from the input.

        Args:
            lines (Iterator[str]): An iterator of strings from which to remove even-numbered lines.

        Yields:
            Iterator[str]: An iterator of strings that includes only odd-numbered lines.
        """
        for i, line in enumerate(lines, start=1):
            if i % 2 != 0:
                yield line

    def _break_lines(self, lines: Iterator[str], **kwargs) -> Iterator[str]:
        """
        Breaks lines that exceed a specified maximum length into smaller lines.

        Args:
            lines (Iterator[str]): An iterator of strings to potentially break into smaller lines.
            kwargs (dict): A dictionary of keyword arguments, including 'max_length' which defines the maximum line length.

        Yields:
            Iterator[str]: An iterator of strings, where long lines are broken according to the specified maximum length.
        """
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

