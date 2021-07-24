# Python Libraries
import os
import csv
import re
from datetime import datetime

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor
from simulator.components.topology import Topology

# Heuristic Algorithms
from simulator.heuristics.proposed_heuristic import proposed_heuristic


class Simulator:
    """ This class allows the creation objects that
    control the whole life cycle of simulations.
    """

    environment = None
    dataset = None

    @classmethod
    def load_dataset(cls, target, formatting='INMET-BR'):
        """ Loads data from input files and creates a topology with sensor objects.

        target : string
            String representing a CSV file or a directory containing a list of CSV files

        formatting : string
            Information on the type of formatting needs to be performed to load the dataset
        """

        # Storing the dataset name
        Simulator.dataset = target

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
                dataset = Simulator.parse_dataset_inmet_br(target=target)

            # Adding sensors to the NetworkX topology
            for sensor in dataset:
                sensor = Sensor(coordinates=sensor['coordinates'], timestamp=sensor['timestamp'], type='physical',
                                measurement=sensor['measurement'], metric=sensor['metric'], alias=sensor['alias'])
                topo.add_node(sensor)


    @classmethod
    def parse_dataset_inmet_br(cls, target):
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


    @classmethod
    def run(cls, steps, algorithm):
        """ Starts the simulation.

        Parameters
        ==========
        steps : int
            Number of simulation steps

        algorithm : string
            Heuristic algorithm that will be executed
        """

        # Creating a simulation environment
        Simulator.environment = SimulationEnvironment(steps=int(steps), dataset=Simulator.dataset, heuristic=algorithm)

        # Informing the simulation environment what's the heuristic will be executed
        Simulator.environment.heuristic = algorithm

        # Starting the simulation
        Simulator.environment.run(heuristic=Simulator.heuristic(algorithm=algorithm))


    @classmethod
    def heuristic(cls, algorithm):
        """ Checks if the heuristic informed by the user is valid
        and passes it as a parameter to the simulation environment.

        Parameters
        ==========
        algorithm : string
            Heuristic algorithm that will be executed

        Returns
        =======
        heuristic : function
            Function that accommodates the heuristic algorithm that will be executed
        """

        if algorithm == 'proposed_heuristic':
            return(proposed_heuristic)
        else:
            raise Exception('Invalid heuristic algorithm.')


    @classmethod
    def show_output(cls, output_file):
        """ Exhibits the simulation results.

        Parameters
        ==========
        output_file : string
            Name of the output file containing the simulation results
        """

        print('\n\n=== SIMULATION RESULTS ===')
        for step_metrics in Simulator.environment.metrics:
            print(step_metrics)
