import csv
from pathlib import Path
import sys
from typing import Dict, List

from raft_data_parser.csv_object import CsvObject
from raft_data_parser.scriptable_object.fuel_value import FuelValue


def process_folder(path: Path, output_dir_path: Path) -> None:
    csv_files: Dict[Path, List[CsvObject]] = {}
    for file in path.rglob("*"):
        if file.suffix == ".txt":
            if file.name.startswith("FuelValue"):
                csv_file = output_dir_path / "FuelValue.csv"
                fuelvalue = FuelValue()
                fuelvalue.parse_file(file)
                csvlist = csv_files.get(csv_file, [])
                csvlist.append(fuelvalue)
                csv_files[csv_file] = csvlist

    for output_path, csv_objects in csv_files.items():
        with open(output_path, "w", encoding="utf-8") as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            do_once = True
            for csv_object in csv_objects:
                if do_once:
                    csvwriter.writerow(csv_object.get_header())
                    do_once = False
                csvwriter.writerow(csv_object.to_row())
                
def main() -> None:
    print("Loading Stuff")
    folder_with_data_path: Path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    error_bool: bool = False
    if not folder_with_data_path.is_dir():
        error_bool = True
        print(f"Argument is not a dir: {folder_with_data_path}")
    if not folder_with_data_path.exists():
        error_bool = True
        print(f"Folder doesn't exist: {folder_with_data_path}")
    if not error_bool:
        process_folder(folder_with_data_path, output_path)
    else:
        return


if __name__ == "__main__":
    main()
