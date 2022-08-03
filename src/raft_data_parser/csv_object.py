

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class CsvObject(ABC):
    """Base Class for Objects that can be written to a csv file

    Args:
        ABC (_type_): _description_
    """
    @abstractmethod
    def to_row(self) -> List[str]:
        """Converts object variables to a list of strings

        Returns:
            List[str]: list of object variables
        """
    @abstractmethod
    def get_header(self) -> List[str]:
        """Returns the expected header of csv object

        Returns:
            List[str]: list of headers
        """
        
    @abstractmethod
    def parse_file(self, path: Path) -> None:
        """Parses text file that has relevant information

        Args:
            path (Path): text file path
        """