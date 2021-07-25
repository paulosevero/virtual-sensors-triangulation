# Python Libraries
import numpy as np

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor


def distance_matrix(x0, y0, x1, y1):
    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    # Make a distance matrix between pairwise observations
    # Note: from <http://stackoverflow.com/questions/1871536>
    # (Yay for ufuncs!)
    d0 = np.subtract.outer(obs[:, 0], interp[:, 0])
    d1 = np.subtract.outer(obs[:, 1], interp[:, 1])

    return np.hypot(d0, d1)


def idw(sensor_id):
    """ IDW....
    """

    virtual_sensor = Sensor.find_by_id(sensor_id)
    virtual_sensor.type = 'logical'

    SimulationEnvironment.first().heuristic = 'Inverse Distance Weighting'

    sensors_latitude = np.array([sensor.coordinates[0] for sensor in Sensor.all() if sensor.type == 'physical'])
    sensors_longitude = np.array([sensor.coordinates[1] for sensor in Sensor.all() if sensor.type == 'physical'])
    sensors_measurement = np.array([sensor.measurement for sensor in Sensor.all() if sensor.type == 'physical'])

    dist = distance_matrix(sensors_latitude, sensors_longitude, virtual_sensor.coordinates[0], virtual_sensor.coordinates[1])

    # In IDW, weights are 1 / distance
    weights = 1.0 / dist

    # Make weights sum to one
    weights /= weights.sum(axis=0)

    # Multiply the weights for each interpolated point by all observed Z-values
    zi = np.dot(weights.T, sensors_measurement)

    virtual_sensor.inferred_measurement = zi[0]
