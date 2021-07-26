# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor

NUMBER_OF_NEIGHBORS = 3


def knn(sensor_id):
    """ kNN....
    """

    virtual_sensor = Sensor.find_by_id(sensor_id)
    virtual_sensor.type = 'logical'

    SimulationEnvironment.first().heuristic = f'k-Nearest Neighbors (k={NUMBER_OF_NEIGHBORS})'

    neighbor_sensors = virtual_sensor.find_neighbors_sorted_by_distance()[0:NUMBER_OF_NEIGHBORS]

    neighbors_measurements = [neighbor.measurement for neighbor in neighbor_sensors]

    virtual_sensor.inferred_measurement = sum(neighbors_measurements) / len(neighbor_sensors)
