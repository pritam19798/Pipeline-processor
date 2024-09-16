from typing import Iterator, List, Callable, Optional, Dict, Tuple, Any
from abc import ABC, abstractmethod


class BaseFunctionRepository(ABC):
    @abstractmethod
    def get_function_lookup(self) -> dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:
        raise NotImplementedError


class BaseIoHandler(ABC):

    @abstractmethod
    def read_input(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def write_output(self, processed_lines: List[str]) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_external_functions(self, function_path: str) \
            -> Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:
        raise NotImplementedError


class BaseConfigLoader(ABC):
    @abstractmethod
    def load_pipeline_steps(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def load_pipeline_steps_with_arguments(self) -> Tuple[List[str], Dict[str, Dict]]:
        raise NotImplementedError


class BaseProcessor(ABC):
    @abstractmethod
    def process(self, functions: List[str], **kwargs: Dict) -> None:
        raise NotImplementedError

    @abstractmethod
    def stream_process(self, functions: List[str], **kwargs) -> None:
        raise NotImplementedError
