from logging import Logger
from typing import List, Dict, Iterator, Callable, Optional, Any
from atk_training_pritam_wf_dynamic_loader.base_clases import BaseFunctionRepository, BaseProcessor, BaseIoHandler, \
    BaseConfigLoader


class Processor(BaseProcessor):
    def __init__(self, *, logger: Logger, io_handler: BaseIoHandler, config_loader: BaseConfigLoader,
                 function_repositories: List[BaseFunctionRepository]):

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
                self.logger.error(f"an error occurred stopping the execution of processor.\nerror: {err}")
                break
            finally:
                processed_lines.append(line)

        self.io_handler.write_output(processed_lines)

    def stream_process(self, functions: List[str] = None,
                       additional_function_path: Optional[str] = None, **kwargs) -> None:

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
        if name not in self.function_lookup:
            self.function_lookup[name] = func
        else:
            self.logger.info(f"function {name} already present in function lookup")

    def _populate_functions_from_pipeline(self):
        self.function_list = self.config_loader.load_pipeline_steps()

    def _populate_functions_and_arguments_from_pipeline(self):
        self.function_list, self.argument_list = self.config_loader.load_pipeline_steps_with_arguments()
