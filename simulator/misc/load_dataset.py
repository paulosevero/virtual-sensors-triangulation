import os
import csv
import re
from datetime import datetime

from simulator.sensor import Sensor
from simulator.topology import Topology


def load_dataset(target, formatting='INMET-BR'):
    """ Loads data from input files and creates a topology with sensor objects.
    """

    topo = Topology()

    data = os.listdir('data')

    if target not in data:
        raise Exception('Invalid input target.')

    else:
        # Checking if the passed argument represents a CSV file or a directory.
        # In case the argument points to a CSV file, loads the data directly.
        # Otherwise, it assumes the argument denotes a directory containing a
        # list of CSV files that will be merged as part of a single dataset.
        if '.csv' in target:
            print(f'CSV input file: {target}')

        if '.json' in target:
            print(f'JSON input file: {target}')

        else:
            dataset = inmet_br(target=target)

        for sensor in dataset:
            sensor = Sensor(coordinates=sensor['coordinates'], timestamp=sensor['timestamp'], type='physical',
                            measurement=sensor['measurement'], metric=sensor['metric'], alias=sensor['alias'])

            topo.add_node(sensor)


def inmet_br(target):
    """ Parse data following the format adopted by the
    Brazilian National Institute of Meteorology (INMET).

    Parameters
    ==========
    target : String
        List of files or directory containing the dataset

    Returns
    =======
    dataset : List
        Parsed dataset
    """

    dataset = []

    files = [file for file in os.listdir(f'data/{target}') if '.csv' in file.lower()]

    for file in files:

        sensor = {}

        with open(f'data/{target}/{file}', newline='', encoding='ISO-8859-1') as csvfile:
            content = list(csv.reader(csvfile, delimiter=';', quotechar='|'))

            if len(content[4][1]) > 0:
                latitude = float(re.sub(',', '.', content[4][1]))
            else:
                latitude = None

            if len(content[5][1]) > 0:
                longitude = float(re.sub(',', '.', content[5][1]))
            else:
                longitude = None

            if len(content[9][9]) > 0:
                sensor['measurement'] = float(re.sub(',', '.', content[9][9]))
            else:
                sensor['measurement'] = None

            sensor['alias'] = content[2][1]
            sensor['coordinates'] = (latitude, longitude)
            timestamp = f'{content[9][0]}@{content[9][1][0:4]}'
            sensor['timestamp'] = datetime.strptime(timestamp, '%Y/%m/%d@%H%M')
            sensor['metric'] = content[8][9]

        dataset.append(sensor)

    return(dataset)
