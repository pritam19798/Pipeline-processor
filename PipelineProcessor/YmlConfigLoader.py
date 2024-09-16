from logging import Logger
from typing import List, Tuple, Dict, Any

import yaml

from PipelineProcessor.base_clases import BaseConfigLoader


class YmlConfigLoader(BaseConfigLoader):
    def __init__(self, *, logger: Logger, yml_path: str):
        self.logger: Logger = logger
        self.yml_path: str = yml_path

    def load_pipeline_steps(self) -> List[str]:
        if self.yml_path is not None:
            try:
                with open(self.yml_path, 'r') as yaml_file:
                    return yaml.safe_load(yaml_file)['pipeline']
            except FileNotFoundError:
                self.logger.error(f"Pipeline not found in specified location {self.yml_path}")
                self.logger.info(f"Returning empty pipline")
                return []
        else:
            return []

    def load_pipeline_steps_with_arguments(self) -> Tuple[List[str], Dict[str, Dict[str, Dict[str, Any]]]]:
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
                self.logger.error(f"error occurred during loading the pipline \nError: {error}")
                self.logger.info(f"Returning empty pipline")
                return [], {}
            except FileNotFoundError:
                self.logger.error(f"Pipeline not found in specified location {self.yml_path}")
                self.logger.info(f"Returning empty pipline")
                return [], {}

        else:
            self.logger.info(f"No pipline specified returning empty pipline ....")
            return [], {}
