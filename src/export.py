# module export

import os
import csv
import json

def json_to_csv(json_file_path: str) -> str:
    with open(json_file_path, mode='r', encoding='utf-8') as json_file:
        json_data: list[dict[str, str]] = json.load(json_file)

    csv_file_path = os.path.splitext(json_file_path)[0] + '.csv'

    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        csv_writer.writerow(json_data[0].keys())

        for item in json_data:
            csv_writer.writerow(item.values())

    return csv_file_path
