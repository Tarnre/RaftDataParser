

from enum import Enum
from pathlib import Path
from typing import List, Optional
from raft_data_parser.csv_object import CsvObject


class FuelType(Enum):
    WATERTANK = 0
    MOTORTANK = 1
    FUELTANK = 2
    HONEYTANK = 3
    COMPOSTTANK = 4
    RECYCLER = 5



class FuelValue(CsvObject):
    """Class of items that have a fuel value

    Args:
        CsvObject (_type_): _description_
    """

    def __init__(self, name: Optional[str] = None, value: Optional[str] = None, fuel_type: Optional[FuelType] = None) -> None:
        super().__init__()
        self.name = name
        self.value = value
        self.fuel_type = fuel_type

    def to_row(self) -> List[str]:
        if self.fuel_type is None:
            fuel_type = "None"
        else:
            fuel_type = self.fuel_type.name
        return [str(self.name), fuel_type, str(self.value)]

    def get_header(self) -> List[str]:
        return ["Name", "Fuel Type", "Value"]

    def parse_file(self, path: Path) -> None:
        with open(path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                starting_point = line.find("=")
                index = line.find("m_Name")
                if index != -1:
                    self.name = line[starting_point + 13:-2]
                    self.strip_identifier()
                index = line.find("fuelValueOfType")
                if index != -1:
                    self.value = line[starting_point + 2:-1]
                index = line.find("fuelFiltrationType")
                if index != -1:
                    self.fuel_type = FuelType(int(line[starting_point + 2:-1]))

            if None in {self.name, self.fuel_type, self.value}:
                print(f"Missing fields when parsing file: {path}")

    def strip_identifier(self) -> None:
        if self.name is None:
            return
        for fuel_type in FuelType:
            search = "_" + fuel_type.name.lower()
            search_len = len(search)
            index = self.name.lower().find(search)
            if index != -1:
                self.name = self.name[:-search_len]
                return
