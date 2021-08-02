# Python Libraries
import numpy as np

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor


def distance_matrix(x0, y0, x1, y1):
    """ Calculates the distance matrix between two locations.

    Parameters
    ==========
    x0 : float
        'x' of the first coordinates
    y0 : float
        'y' of the first coordinates
    x1 : float
        'x' of the second coordinates
    y1 : float
        'y' of the second coordinates

    Returns
    =======
    dist_matrix : float
        Distance matrix between the given coordinates
    """

    obs = np.vstack((x0, y0)).T
    interp = np.vstack((x1, y1)).T

    # Make a distance matrix between pairwise observations
    # Note: from <http://stackoverflow.com/questions/1871536>
    d0 = np.subtract.outer(obs[:, 0], interp[:, 0])
    d1 = np.subtract.outer(obs[:, 1], interp[:, 1])

    dist_matrix = np.hypot(d0, d1)
    return(dist_matrix)


def idw():
    """ The Inverse Distance Weighting (IDW) [1] calculates the value of unknown points using a weighted
    mean of the values available at the known points. The weight of known points is given by the inverse
    of their distance from the unknown point (the smallest the distance the higher the weight).

    [1] Shepard, D. (1968, January). A two-dimensional interpolation function for
    irregularly- spaced data. In Proceedings of the 1968 23rd ACM national conference (pp. 517-524).
    """

    virtual_sensors = SimulationEnvironment.first().virtual_sensors

    for virtual_sensor in virtual_sensors:

        sensors_latitude = np.array([sensor.coordinates[0] for sensor in Sensor.all() if sensor.type == 'physical'])
        sensors_longitude = np.array([sensor.coordinates[1] for sensor in Sensor.all() if sensor.type == 'physical'])
        sensors_measurement = np.array([sensor.measurement for sensor in Sensor.all() if sensor.type == 'physical'])

        dist = distance_matrix(sensors_latitude, sensors_longitude, virtual_sensor.coordinates[0], virtual_sensor.coordinates[1])

        # Defining weights
        weights = 1.0 / dist

        # Make weights sum to one
        weights /= weights.sum(axis=0)

        # Multiply the weights for each interpolated point by all observed Z-values
        zi = np.dot(weights.T, sensors_measurement)

        virtual_sensor.inferred_measurement = zi[0]
