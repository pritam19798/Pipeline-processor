# PipelineProcessor

## Overview

Framework for processing text pipeline using classes and objects

## Installation

poetry installation
```bash
poetry add PipelineProcessor
```

## Usage
Use in command line

```bash
#Usage: PipelineProcessor [OPTIONS] INPUT_FILENAME YML_PATH

#Arguments:
#  INPUT_FILENAME  [required]
#  YML_PATH        [required]
#
#Options:
#  --additional-function-path TEXT
#  --output-filename TEXT
#  --install-completion [bash|zsh|fish|powershell|pwsh]
#                                  Install completion for the specified shell.
#  --show-completion [bash|zsh|fish|powershell|pwsh]
#                                  Show completion for the specified shell, to
#                                  copy it or customize the installation.
#  --help                          Show this message and exit.

# example usage

PipelineProcessor  /path/to/input /path/to/pipeline --additional-function-path /path/to/additional_functions --output-filename /path/to/output
```

## Sample pipeline.yml file
```yaml
pipeline:
   - stream_lower_case
   - coalesce_empty_lines
   - stream_uk_to_us
   - break_lines:
      kwargs: # Use a kwargs dictionary to pass arguments
         max_length: 25
   - number_the_lines
   - stream_capitalized
   - custom_function
```
## List of available functions
1. ```number_the_lines``` : adds the line number as a prefix to each line.
2. ```coalesce_empty_lines``` : removes multiple empty lines and produces only one empty line.
3. ```remove_empty_lines``` : removes any empty lines.
4. ```remove_even_lines```  : removes all the even numbered lines
5. ```break_lines```  : breaks up a single long line into short (default 20) lines.
6. ```Stream_remove_stop_words```: Removes all the words "a", "an", "the", "and" "or" assuming that the text does not contain any punctuation -- and the words are separated by just simple space. 
7. ```stream_capitalize```: Capitalizes the words in the file.
8. ```stream_fetch_geo_ip```: Collect city, region, and country in comma separated values from https://ipinfo.io/{ip_number}/geo .
9. ```stream_upper_case```: Uppercase the words in the file.
10. ```stream_lower_case```: Just like upper case, but lower case.
11. ```stream_uk_to_us```: Use regular expressions to convert any word ending with sation to zation, in lower case.

## Example of  custom function creation
Example of custom function
```python
#additional function  
from typing import Iterator
def custom_function(lines: Iterator[str]) -> Iterator[str]:               
   for line in lines:                                                     
       new_line = line.strip() + " <new custom string> \n"                
       yield new_line 
```

## Extension
If you want to extend the functionality, you can add or update with your custom function. Example:

```python
# In your main module
# Instantiate logger
# Instantiate  FileHandler, Processor and FunctionRepositories
import logging
from logging import Logger
from PipelineProcessor.StreamFunctionRepository import StreamFunctionRepository
from PipelineProcessor.FileHandler import FileHandler
from PipelineProcessor.Processor import Processor
from PipelineProcessor.BasicStreamFunctionRepository import BasicStreamBasicFunctionRepository
from PipelineProcessor.YmlConfigLoader import YmlConfigLoader

# logging
logger: Logger = logging.getLogger()
# instantiate File handler
file_handler: FileHandler = FileHandler(logger=logger, input_filename='input/file/path', output_filename='output/file/path')
# instantiate Yml Config Loader
yml_config_loader: YmlConfigLoader = YmlConfigLoader(logger=logger, yml_path='yml/path')

# instantiate Function repositories
stream_repository: StreamFunctionRepository = StreamFunctionRepository()
extended_stream_repository: BasicStreamBasicFunctionRepository = BasicStreamBasicFunctionRepository()

# instantiate processor
processor: Processor = Processor(logger=logger, io_handler=file_handler,
                                 config_loader=yml_config_loader,
                                 function_repositories=[stream_repository, extended_stream_repository])

# call processor
processor.stream_process(additional_function_path='additional/function/path')

```

```python                                                                 
#additional function                                                      
from typing import Iterator                                               
                                                                          
def custom_function(lines: Iterator[str]) -> Iterator[str]:               
   for line in lines:                                                     
       new_line = line.strip() + " <new custom string> \n"                
       yield new_line                                                     
 ```                                                                      