# Python Libraries
import os
import csv
import numpy as np
import pandas as pd
import re
from datetime import datetime
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor
from simulator.components.topology import Topology

# Heuristic Algorithms
from simulator.heuristics.proposed_heuristic import proposed_heuristic
from simulator.heuristics.first_fit_proposal import first_fit_proposal
from simulator.heuristics.knn import knn
from simulator.heuristics.idw import idw

VERBOSITY = 1


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

            elif '.json' in target:
                print(f'JSON input file: {target}')

            elif formatting == 'INMET-BR':
                dataset = Simulator.parse_dataset_inmet_br(target=target, metric=metric)
            else:
                raise Exception('Invalid dataset.')

            # Adding sensors to the NetworkX topology
            for data in dataset:
                Sensor(coordinates=data['coordinates'], type='physical', timestamps=data['timestamps'],
                       measurements=data['measurements'], alias=data['alias'])


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

                # Converting part of the CSV with data measurements to a pandas dataframe to ease manipulation
                starting_row = 1449
                ending_row = starting_row + 23
                raw_measurements = pd.DataFrame(content[starting_row:starting_row + ending_row])
                raw_measurements.columns = content[8]  # Defining the dataframe header with names of each column

                # Removing rows with missing values
                raw_measurements[metric].replace('', np.nan, inplace=True)
                raw_measurements.dropna(subset=[metric], inplace=True)

                # Parsing sensor measurements
                sensor['measurements'] = [float(re.sub(',', '.', measurement)) for measurement in list(raw_measurements[metric])]

                # Parsing measurement timestamps
                dates = list(raw_measurements['Data'])
                hours = list(raw_measurements['Hora UTC'])
                sensor['timestamps'] = [datetime.strptime(f'{dates[i]} {hours[i][0:4]}', '%Y/%m/%d %H%M') for i in range(0, len(dates))]

            dataset.append(sensor)

        return(dataset)


    @classmethod
    def run(cls, steps, algorithm, sensors):
        """ Starts the simulation.

        Parameters
        ==========
        steps : int
            Number of simulation steps

        algorithm : string
            Heuristic algorithm that will be executed

        sensors : int
            Number of sensors whose measurements will be inferred
        """

        # Creating a simulation environment
        Simulator.environment = SimulationEnvironment(steps=int(steps), dataset=Simulator.dataset, heuristic=algorithm)

        # Informing the simulation environment what's the heuristic will be executed
        Simulator.environment.heuristic = algorithm

        # Starting the simulation
        Simulator.environment.run(sensors=sensors, heuristic=Simulator.heuristic(algorithm=algorithm))


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
            Simulator.environment.heuristic = 'Proposed Heuristic'
            return(proposed_heuristic)
        elif algorithm == 'first_fit_proposal':
            Simulator.environment.heuristic = 'Proposed Heuristic (Simplified Version)'
            return(first_fit_proposal)
        elif algorithm == 'knn':
            Simulator.environment.heuristic = 'k-Nearest Neighbors'
            return(knn)
        elif algorithm == 'idw':
            Simulator.environment.heuristic = 'Inverse Distance Weighting'
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


        metrics_by_sensor = []

        for sensor in Simulator.environment.virtual_sensors:

            # Initializing a dictionary that will centralize all metrics from the sensor
            sensor_metrics = {'sensor': sensor, 'real_measurements': [], 'inferences': [], 'timestamps': [],
                              'r2': None, 'mse': None, 'mae': None}

            # Collecting real measurements and inferences from the sensor in each step
            for step in Simulator.environment.metrics:
                metrics = next(metrics for metrics in step['measurements'] if metrics['sensor'] == sensor.id)
                sensor_metrics['timestamps'].append(metrics['timestamp'])
                sensor_metrics['real_measurements'].append(metrics['real_measurement'])
                sensor_metrics['inferences'].append(metrics['inference'])

            # Calculating accuracy metrics for the sensor inferences
            sensor_metrics['mse'] = mean_squared_error(sensor_metrics['real_measurements'], sensor_metrics['inferences'], squared=False)
            sensor_metrics['mae'] = mean_absolute_error(sensor_metrics['real_measurements'], sensor_metrics['inferences'])

            # Adding sensor metrics to the list of metrics of all sensors
            metrics_by_sensor.append(sensor_metrics)


        mse = []
        mae = []

        if VERBOSITY >= 2:
            print('=== METRICS BY SENSOR ===')
        for sensor_metrics in metrics_by_sensor:
            if VERBOSITY >= 2:
                print(f'Sensor_{sensor_metrics["sensor"]}')
                print(f'    Real Measurements ({len(sensor_metrics["real_measurements"])}): {sensor_metrics["real_measurements"]}')
                print(f'    Inferences ({len(sensor_metrics["inferences"])}): {[round(inference, 1) for inference in sensor_metrics["inferences"]]}')
                print(f'    Coefficient of Determination (R²): {sensor_metrics["r2"]}')
                print(f'    Root Mean Squared Error (RMSE): {sensor_metrics["mse"]}')
                print(f'    Mean Absolute Error (MAE): {sensor_metrics["mae"]}')

            mse.append(sensor_metrics['mse'])
            mae.append(sensor_metrics['mae'])

        mse = sum(mse) / len(mse)
        mae = sum(mae) / len(mae)


        if VERBOSITY >= 1:
            print('=== OVERALL RESULTS ===')
            print(f'Heuristic: {Simulator.environment.heuristic}')
            print(f'Sensors: {[sensor.id for sensor in Simulator.environment.virtual_sensors]}')
            print(f'Root Mean Squared Error (RMSE): {mse}')
            print(f'Mean Absolute Error (MAE): {mae}')

            Topology.first().draw(showgui=False, savefig=True)
