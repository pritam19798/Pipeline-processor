from typing import Callable, Iterator, Optional, Dict, Any
from PipelineProcessor.BasicFunctionRepository import BasicFunctionRepository

class BasicStreamBasicFunctionRepository(BasicFunctionRepository):
    """
    A class that extends BasicFunctionRepository to implement streaming operations
    on text input where transformations are applied to a stream of strings (e.g., lines from a file).
    This allows for processing large datasets or streams in a memory-efficient manner.
    """

    def get_function_lookup(self) -> dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:
        """
        Provides a dictionary mapping function names to their corresponding callable methods
        that are adapted to operate on streams of strings.

        Returns:
            dict[str, Callable]:
            A dictionary with keys as function names and values as methods suitable for streaming data.
        """
        return {
            "stream_upper_case": self._string_to_stream_function(self._upper_case),
            "stream_lower_case": self._string_to_stream_function(self._lower_case),
            "stream_capitalized": self._string_to_stream_function(self._capitalized),
            "stream_remove_stop_words": self._string_to_stream_function(self._remove_stop_words),
            "stream_uk_to_us": self._string_to_stream_function(self._uk_to_us),
            "stream_fetch_geo_ip": self._string_to_stream_function(self._fetch_geo_ip)
        }

    def _string_to_stream_function(self, in_function: Callable[[str], str]) -> Callable:
        """
        Wraps a string transformation function to work with streams of strings, yielding transformed lines.

        Args:
            in_function (Callable[[str], str]): A function that takes a single string as input
                                                and returns a transformed string.

        Returns:
            Callable[[Iterator[str]], Iterator[str]]: A function that takes an iterator of strings
                                                     and yields transformed strings.
        """
        def wrapped_function(lines: Iterator[str]) -> Iterator[str]:
            """
            A wrapped function that applies the transformation function to each line in the input iterator.

            Args:
                lines (Iterator[str]): An iterator of strings to be transformed.

            Returns:
                Iterator[str]: An iterator yielding transformed strings.
            """
            for line in lines:
                yield in_function(line)

        return wrapped_function
