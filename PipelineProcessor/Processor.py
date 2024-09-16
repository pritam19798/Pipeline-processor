from logging import Logger
from typing import List, Dict, Iterator, Callable, Optional, Any
from PipelineProcessor.base_clases import BaseFunctionRepository, BaseProcessor, BaseIoHandler, \
    BaseConfigLoader


class Processor(BaseProcessor):
    """
    A class responsible for processing data using a series of functions defined in function repositories.
    It handles data input/output through specified handlers and configures processing steps based on a configuration loader.

    Attributes:
        logger (Logger): Logger object for logging information.
        io_handler (BaseIoHandler): An IO handler to manage input and output operations.
        config_loader (BaseConfigLoader): A configuration loader to manage processing steps and their configurations.
        function_repositories (List[BaseFunctionRepository]): A list of function repositories to pull processing functions from.
    """

    def __init__(self, *, logger: Logger, io_handler: BaseIoHandler, config_loader: BaseConfigLoader,
                 function_repositories: List[BaseFunctionRepository]):
        """
        Initializes the Processor with specified logger, IO handler, configuration loader, and function repositories.

        Args:
            logger (Logger): The logger instance.
            io_handler (BaseIoHandler): The IO handler for managing input and output.
            config_loader (BaseConfigLoader): The configuration loader to get processing steps.
            function_repositories (List[BaseFunctionRepository]): The list of repositories containing processing functions.
        """
        # logging
        self.logger = logger

        # Function lookup initialization
        self.function_lookup: Dict[str, Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]] = {}

        # Loading functions from function repository into function lookup
        for repository in function_repositories:
            self.function_lookup.update(repository.get_function_lookup())

        # Initializing
        self.io_handler: BaseIoHandler = io_handler
        self.config_loader: BaseConfigLoader = config_loader
        self.function_list: List[str] = []
        self.argument_list: Dict[str, Dict] = {}

    def process(self, functions: List[str], **kwargs) -> None:
        """
        Processes data sequentially using a list of function names from the function_lookup.

        Args:
            functions (List[str]): List of function names to apply.
            kwargs: Additional keyword arguments to pass to the functions.
        """
        # Read lines using FileHandler
        lines = self.io_handler.read_input()
        processed_lines: List[str] = []
        for line in lines:
            try:
                for func_name in functions:
                    if func_name in self.function_lookup:
                        line = self.function_lookup[func_name](line, **kwargs.get(func_name, {}))
                    else:
                        self.logger.error(f"Function '{func_name}' not found in available functions.")
                        raise TypeError(f"Function '{func_name}' not found in available functions.")

            except Exception as err:
                self.logger.error(f"An error occurred stopping the execution of processor.\nerror: {err}")
                break
            finally:
                processed_lines.append(line)

        self.io_handler.write_output(processed_lines)

    def stream_process(self, functions: List[str] = None,
                       additional_function_path: Optional[str] = None, **kwargs) -> None:
        """
        Processes data using a stream approach, potentially loading additional functions dynamically.

        Args:
            functions (List[str]): Optional list of additional function names to apply.
            additional_function_path (Optional[str]): Path to load additional functions from.
            kwargs: Additional keyword arguments to pass to the functions.
        """
        # Read lines using IoHandler
        processed_lines = self.io_handler.read_input()

        # Read additional function if specified
        if additional_function_path is not None:
            self.function_lookup.update(self.io_handler.load_external_functions(additional_function_path))

        # Read functions and arguments from pipeline.yml
        self._populate_functions_and_arguments_from_pipeline()

        # Add functions specified in caller function
        if functions is not None:
            self.function_list.extend(functions)

        if len(self.function_list) <= 0:
            self.logger.error("No Functions present in the pipline. Exited without any operation....")
            return None

        # Add arguments specified in caller function
        if kwargs is not None:
            self.argument_list.update(kwargs)

        # Process lines directly using stream functions
        for func_name in self.function_list:  # Read each element in function_list
            if func_name in self.function_lookup:  # Check if the function defined
                try:
                    processed_lines = self.function_lookup[func_name](processed_lines,
                                                                      **self.argument_list.get(func_name, {}))
                except TypeError as error:
                    self.logger.error(error)
                    break
            else:
                self.logger.info(f"Function {func_name} not found in available function lookup skipping {func_name}")

        # Write processed lines using FileHandler
        self.io_handler.write_output(processed_lines)

    def _update_function_to_lookup(self, name: str,
                                   func: Callable[[Iterator[str], Optional[Dict[str, Any]]], Iterator[str]]) -> None:
        """
        Updates or adds a function to the function lookup.

        Args:
            name (str): The name of the function to add or update.
            func (Callable): The function to add or update in the lookup.
        """
        if name not in self.function_lookup:
            self.function_lookup[name] = func
        else:
            self.logger.info(f"function {name} already present in function lookup")

    def _populate_functions_from_pipeline(self):
        """
        Populates the function list from the pipeline configuration loaded by the config loader.
        """
        self.function_list = self.config_loader.load_pipeline_steps()

    def _populate_functions_and_arguments_from_pipeline(self):
        """
        Populates both the function list and the argument list from the pipeline configuration loaded by the config loader.
        """
        self.function_list, self.argument_list = self.config_loader.load_pipeline_steps_with_arguments()
