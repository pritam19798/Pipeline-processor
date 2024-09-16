import re
import requests
from typing import Callable

from PipelineProcessor.base_clases import BaseFunctionRepository

class BasicFunctionRepository(BaseFunctionRepository):
    """
    A repository class that extends BaseFunctionRepository to provide specific text processing functions.
    This class provides functions for transforming text in various ways such as changing case,
    removing stop words, converting UK spelling to US, and fetching geographical information from IP addresses.
    """

    def get_function_lookup(self) -> dict[str, Callable[[str], str]]:
        """
        Provides a dictionary mapping function names to their corresponding callable methods.

        Returns:
            dict[str, Callable[[str], str]]: A dictionary with keys as function names and values as the methods.
        """
        return {
            "upper_case": self._upper_case,
            "lower_case": self._lower_case,
            "capitalized": self._capitalized,
            "remove_stop_words": self._remove_stop_words,
            "uk_to_us": self._uk_to_us,
            "fetch_geo_ip": self._fetch_geo_ip,
        }

    def _upper_case(self, line: str) -> str:
        """
        Converts all characters in the input string to upper case.

        Args:
            line (str): The input string to transform.

        Returns:
            str: The transformed string with all characters in upper case.
        """
        return line.upper()

    def _lower_case(self, line: str) -> str:
        """
        Converts all characters in the input string to lower case.

        Args:
            line (str): The input string to transform.

        Returns:
            str: The transformed string with all characters in lower case.
        """
        return line.lower()

    def _capitalized(self, line: str) -> str:
        """
        Capitalizes the first letter of each word in the input string.

        Args:
            line (str): The input string to transform.

        Returns:
            str: The transformed string with the first letter of each word capitalized.
        """
        return ' '.join([word.capitalize() for word in line.split()]) + '\n'

    def _remove_stop_words(self, line: str) -> str:
        """
        Removes common English stop words from the input string.

        Args:
            line (str): The input string from which to remove stop words.

        Returns:
            str: The transformed string with stop words removed.
        """
        stop_words = {"a", "an", "the", "and", "or"}
        return " ".join([word for word in line.split() if word.lower() not in stop_words])

    def _uk_to_us(self, line: str) -> str:
        """
        Converts UK spelling to US spelling in the input string, focusing on -ise to -ize suffix changes.

        Args:
            line (str): The input string to transform.

        Returns:
            str: The string with UK spelling converted to US spelling.
        """
        pattern = re.compile(r'(?<=[a-zA-Z])+s(?=ation)', re.IGNORECASE)
        return re.sub(pattern, 'z', line)

    def _fetch_geo_ip(self, line: str) -> str:
        """
        Fetches geographical location information for each IP address found in the input string.

        Args:
            line (str): The input string containing IP addresses.

        Returns:
            str: A newline-separated string with geographical information for each IP address found.
        """
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
