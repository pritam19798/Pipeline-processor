
import requests
import re
from typing import Callable

from atk_training_pritam_wf_dynamic_loader.base_clases import BaseFunctionRepository


class BasicFunctionRepository(BaseFunctionRepository):

    def get_function_lookup(self) -> dict[str, Callable[[str], str]]:
        return {
            "upper_case": self._upper_case,
            "lower_case": self._lower_case,
            "capitalized": self._capitalized,
            "remove_stop_words": self._remove_stop_words,
            "uk_to_us": self._uk_to_us,
            "fetch_geo_ip": self._fetch_geo_ip,
        }

    def _upper_case(self, line: str) -> str:
        return line.upper()

    def _lower_case(self, line: str) -> str:
        return line.lower()

    def _capitalized(self, line: str) -> str:
        return ' '.join([word.capitalize() for word in line.split()]) + '\n'

    def _remove_stop_words(self, line: str) -> str:
        stop_words = {"a", "an", "the", "and", "or"}
        return " ".join([word for word in line.split() if word.lower() not in stop_words])

    def _uk_to_us(self, line: str) -> str:
        pattern = re.compile(r'(?<=[a-zA-Z])+s(?=ation)', re.IGNORECASE)
        return re.sub(pattern, 'z', line)

    def _fetch_geo_ip(self, line: str) -> str:
        results = []
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"

        ip_numbers = re.findall(ip_pattern, line)
        for ip_number in ip_numbers:
            response = requests.get(f"https://ipinfo.io/{ip_number}/geo")

            if response.ok:
                data = response.json()
                results.append(f"{data['city']}, {data['region']}, {data['country']}")
            else:
                results.append("Not a valid IP")

        return "\n".join(results)
