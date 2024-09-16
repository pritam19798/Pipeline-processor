import os
import pathlib
from logging import Logger
from importlib.machinery import SourceFileLoader
from inspect import isfunction, getmembers
from typing import Iterator, Optional, Dict, Callable, Any
from PipelineProcessor.base_clases import BaseIoHandler


class FileHandler(BaseIoHandler):

    def __init__(self, *, logger: Logger, input_filename: str,
                 output_filename: Optional[str] = None):

        # logging
        self.logger: Logger = logger
        self.input_filename: str = input_filename

        if output_filename is None:
            base_name, extension = os.path.splitext(self.input_filename)
            self.output_filename = f"{base_name}.processed{extension}"
        else:
            self.output_filename: str = output_filename

    def read_input(self) -> Iterator[str]:
        with open(self.input_filename, 'r') as infile:
            for line in infile:
                yield line

    def write_output(self, processed_lines: Iterator[str]) -> None:
        with open(self.output_filename, 'w') as outfile:
            outfile.writelines(processed_lines)
        outfile.close()

    def load_external_functions(self, function_path: str) \
            -> Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:

        """Loads files from a path -- uses glob to list all files and uses SourceFileLoader to load the file."""
        functions_dict: Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]] = {}
        for file in pathlib.Path(function_path).glob('*.py'):
            module_name = os.path.basename(os.path.splitext(file)[0])
            loader = SourceFileLoader(module_name, file.as_posix())
            module = loader.load_module()
            functions = getmembers(module, isfunction)
            for (func_name, func) in functions:
                self.logger.info(f"Adding {func_name} in function lookup ....... ")
                functions_dict[func_name] = func
        return functions_dict
