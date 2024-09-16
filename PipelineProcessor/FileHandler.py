import os
import pathlib
from logging import Logger
from importlib.machinery import SourceFileLoader
from inspect import isfunction, getmembers
from typing import Iterator, Optional, Dict, Callable, Any
from PipelineProcessor.base_clases import BaseIoHandler


class FileHandler(BaseIoHandler):
    """
    A class to handle file operations including reading from and writing to files,
    and dynamically loading external functions from Python source files.

    Attributes:
        logger (Logger): Logger object for logging information.
        input_filename (str): Path to the input file.
        output_filename (str): Path to the output file, which is automatically derived if not provided.
    """

    def __init__(self, *, logger: Logger, input_filename: str,
                 output_filename: Optional[str] = None):
        """
        Initializes the FileHandler with logging capabilities, input, and output file paths.

        Args:
            logger (Logger): Logger object for logging.
            input_filename (str): Path to the input file.
            output_filename (Optional[str]): Path to the output file. If None, a default name is generated.
        """
        # logging
        self.logger: Logger = logger
        self.input_filename: str = input_filename

        if output_filename is None:
            base_name, extension = os.path.splitext(self.input_filename)
            self.output_filename = f"{base_name}.processed{extension}"
        else:
            self.output_filename: str = output_filename

    def read_input(self) -> Iterator[str]:
        """
        Reads lines from the input file and yields them one by one.

        Returns:
            Iterator[str]: An iterator that yields lines from the input file.
        """
        with open(self.input_filename, 'r') as infile:
            for line in infile:
                yield line

    def write_output(self, processed_lines: Iterator[str]) -> None:
        """
        Writes processed lines to the output file.

        Args:
            processed_lines (Iterator[str]): An iterator of processed lines to be written to the output file.
        """
        with open(self.output_filename, 'w') as outfile:
            outfile.writelines(processed_lines)
        outfile.close()

    def load_external_functions(self, function_path: str) \
            -> Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:
        """
        Loads Python functions from external files within a specified directory that match a *.py pattern.

        Args:
            function_path (str): The directory path containing .py files to load.

        Returns:
            Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]]:
            A dictionary with function names as keys and the callable functions as values.
        """
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
