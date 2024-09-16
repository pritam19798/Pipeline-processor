from logging import Logger
from typing import List, Tuple, Dict, Any

import yaml

from PipelineProcessor.base_clases import BaseConfigLoader


class YmlConfigLoader(BaseConfigLoader):
    """
    A configuration loader that retrieves pipeline steps and their associated arguments from a YAML file.

    Attributes:
        logger (Logger): Logger object for logging information.
        yml_path (str): Path to the YAML file containing pipeline configurations.
    """

    def __init__(self, *, logger: Logger, yml_path: str):
        """
        Initializes the YmlConfigLoader with a logger and path to the YAML configuration file.

        Args:
            logger (Logger): The logger instance.
            yml_path (str): The file path of the YAML configuration file.
        """
        self.logger: Logger = logger
        self.yml_path: str = yml_path

    def load_pipeline_steps(self) -> List[str]:
        """
        Loads the list of pipeline step names from the YAML file.

        Returns:
            List[str]: A list of pipeline step names. Returns an empty list if the file is not found or another error occurs.
        """
        if self.yml_path is not None:
            try:
                with open(self.yml_path, 'r') as yaml_file:
                    return yaml.safe_load(yaml_file)['pipeline']
            except FileNotFoundError:
                self.logger.error(f"Pipeline not found in specified location {self.yml_path}")
                self.logger.info("Returning empty pipeline")
                return []
        else:
            return []

    def load_pipeline_steps_with_arguments(self) -> Tuple[List[str], Dict[str, Dict[str, Dict[str, Any]]]]:
        """
        Loads the pipeline steps along with their associated arguments from the YAML configuration file.

        Returns:
            Tuple[List[str], Dict[str, Dict[str, Dict[str, Any]]]]:
            A tuple containing a list of function names and a dictionary mapping each function name
            to its respective arguments. Returns empty structures if the file is not found or another error occurs.
        """
        if self.yml_path is not None:
            try:
                with open(self.yml_path, 'r') as yaml_file:
                    pipeline = yaml.safe_load(yaml_file)['pipeline']
                    function_list = []
                    function_args_dict = {}
                    for step in pipeline:
                        if isinstance(step, dict):
                            # Extract function name and arguments
                            function_name = list(step.keys())[0]   # {'a':1,'b':2}->['a','b']
                            function_args = step[function_name]['kwargs']
                            function_list.append(function_name)
                            function_args_dict[function_name] = function_args
                        else:
                            # Append function name directly
                            function_list.append(step)
                return function_list, function_args_dict
            except TypeError as error:
                self.logger.error(f"Error occurred during loading the pipeline\nError: {error}")
                self.logger.info("Returning empty pipeline")
                return [], {}
            except FileNotFoundError:
                self.logger.error(f"Pipeline not found in specified location {self.yml_path}")
                self.logger.info("Returning empty pipeline")
                return [], {}

        else:
            self.logger.info("No pipeline specified returning empty pipeline ....")
            return [], {}
