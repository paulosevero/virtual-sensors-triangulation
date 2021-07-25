# Python Libraries
import os
import csv
import numpy as np
import pandas as pd
import re
from datetime import datetime
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor
from simulator.components.topology import Topology

# Heuristic Algorithms
from simulator.heuristics.proposed_heuristic import proposed_heuristic
from simulator.heuristics.knn import knn
from simulator.heuristics.idw import idw


class Simulator:
    """ This class allows the creation objects that
    control the whole life cycle of simulations.
    """

    environment = None
    dataset = None

    @classmethod
    def load_dataset(cls, target, metric, formatting='INMET-BR'):
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
                dataset = Simulator.parse_dataset_inmet_br(target=target, metric=metric)

            # Adding sensors to the NetworkX topology
            for data in dataset:
                sensor = Sensor(coordinates=data['coordinates'], type='physical', timestamps=data['timestamps'],
                                measurements=data['measurements'], alias=data['alias'])

                topo.add_node(sensor)


    @classmethod
    def parse_dataset_inmet_br(cls, target, metric):
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

                # Parsing basic attributes
                latitude = float(re.sub(',', '.', content[4][1])) if len(content[4][1]) > 0 else None
                longitude = float(re.sub(',', '.', content[5][1])) if len(content[5][1]) > 0 else None
                sensor['coordinates'] = (latitude, longitude)
                sensor['alias'] = content[2][1]

                # Converting part of the CSV with data measurements to a pandas dataframe to ease manipulation. Replace
                # the number '755' in the code below with the desired date range. Examples of values for different data
                # ranges: 177 = First week of january; 755 = Whole january.
                raw_measurements = pd.DataFrame(content[9:177])
                raw_measurements.columns = content[8]  # Defining the dataframe header with names of each column

                # Removing rows with missing values
                raw_measurements[metric].replace('', np.nan, inplace=True)
                raw_measurements.dropna(subset=[metric], inplace=True)

                # Parsing sensor measurements
                sensor['measurements'] = [float(re.sub(',', '.', measurement))
                                          for measurement in list(raw_measurements[metric])]

                # Parsing measurement timestamps
                dates = list(raw_measurements['Data'])
                hours = list(raw_measurements['Hora UTC'])
                sensor['timestamps'] = [datetime.strptime(f'{dates[i]} {hours[i][0:4]}', '%Y/%m/%d %H%M')
                                        for i in range(0, len(dates))]

            dataset.append(sensor)

        return(dataset)


    @classmethod
    def run(cls, steps, algorithm, sensor_id):
        """ Starts the simulation.

        Parameters
        ==========
        steps : int
            Number of simulation steps

        algorithm : string
            Heuristic algorithm that will be executed

        sensor_id : int
            Target sensor whose measurement will be inferred
        """

        # Creating a simulation environment
        Simulator.environment = SimulationEnvironment(steps=int(steps), dataset=Simulator.dataset, heuristic=algorithm)

        # Informing the simulation environment what's the heuristic will be executed
        Simulator.environment.heuristic = algorithm

        # Starting the simulation
        Simulator.environment.run(sensor_id=sensor_id, heuristic=Simulator.heuristic(algorithm=algorithm))


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
        if algorithm == 'knn':
            return(knn)
        if algorithm == 'idw':
            return(idw)
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

        # print('\n\n=== PER-STEP RESULTS ===')

        expected_values = [step_results['measurements'][0]['real_measurement'] for step_results in Simulator.environment.metrics]
        inferred_values = [step_results['measurements'][0]['inference'] for step_results in Simulator.environment.metrics]
        accuracy = [step_results['measurements'][0]['accuracy'] for step_results in Simulator.environment.metrics]
        print('\n\n=== GENERAL RESULTS ===')

        mse = mean_squared_error(expected_values, inferred_values)
        mae = mean_absolute_error(expected_values, inferred_values)
        r2 = r2_score(expected_values, inferred_values)

        print(f'Heuristic: {Simulator.environment.heuristic}')
        print(f'R²: {r2}')
        print(f'Mean Squared Error: {mse}')
        print(f'Mean Absolute Error: {mae}')
        print(f'Accuracy: {round(sum(accuracy) / len(accuracy), 4)}%')


        Topology.first().draw(showgui=False, savefig=False)
