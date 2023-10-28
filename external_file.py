import pandas as pd
import csv
import logging

def import_id_list(filename: str)-> list:
    listobj = pd.read_csv(f".\id_feeder_folder\{filename}")[
            "tickerID"
        ]
    return listobj

def export_result_list_of_dist(listobj: list,filename:str)->None:
    """In output file, each row represent one ticker and the record of its all other keys"""
    keys = listobj[0].keys() # Listobj[0]: pick one of the ticker record. And then took out their keys.
    with open(f".\info_folder\{filename}", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, keys)
        writer.writeheader()
        writer.writerows(listobj)
    logging.info(
        f"csv file created or updated. Location: .\info_folder\{filename}"
    )