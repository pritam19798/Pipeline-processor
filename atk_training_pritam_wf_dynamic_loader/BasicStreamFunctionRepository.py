from typing import Callable, Iterator, Optional, Dict, Any
from atk_training_pritam_wf_dynamic_loader.BasicFunctionRepository import BasicFunctionRepository


class BasicStreamBasicFunctionRepository(BasicFunctionRepository):
    def get_function_lookup(self) -> dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:
        return {
            "stream_upper_case": self._string_to_stream_function(self._upper_case),
            "stream_lower_case": self._string_to_stream_function(self._lower_case),
            "stream_capitalized": self._string_to_stream_function(self._capitalized),
            "stream_remove_stop_words": self._string_to_stream_function(self._remove_stop_words),
            "stream_uk_to_us": self._string_to_stream_function(self._uk_to_us),
            "stream_fetch_geo_ip": self._string_to_stream_function(self._fetch_geo_ip)
        }

    def _string_to_stream_function(self, in_function: Callable[[str], str]) \
            -> Callable:
        def wrapped_function(lines: Iterator[str]) -> Iterator[str]:
            for line in lines:
                yield in_function(line)

        return wrapped_function
