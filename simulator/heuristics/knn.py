# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment


def knn():
    """ Adapted version of the k-Nearest Neighbors (kNN) algorithm that calculates the
    value of a unknown points based on the arithmetic mean of the k nearest spatial neighbors.
    This algorithm is widely used to imputate missing data points [1, 2].

    [1]Deng, Y., Han, C., Guo, J., & Sun, L. (2021). Temporal and spatial nearest neighbor values
    based missing data imputation in wireless sensor networks. Sensors, 21(5), 1782.

    [2] Troyanskaya, O., Cantor, M., Sherlock, G., Brown, P., Hastie, T., Tibshirani, R., ... & Altman,
    R. B. (2001). Missing value estimation methods for DNA microarrays. Bioinformatics, 17(6), 520-525.
    """

    # Parameter that define the number of neighbor sensors that will be used to estimate the virtual sensor value
    NEIGHBORS_TO_ESTIMATE_MEASUREMENT_DIRECTLY = SimulationEnvironment.first().neighbors

    # Adding the number of neighbors (given by the 'k' parameter) to the heuristic's name to ease post-simulation analysis
    SimulationEnvironment.first().heuristic = f'k-Nearest Neighbors (k={NEIGHBORS_TO_ESTIMATE_MEASUREMENT_DIRECTLY})'

    # Gathering the list of virtual sensors whose measurements need to be inferred
    virtual_sensors = SimulationEnvironment.first().virtual_sensors

    # Inferring the values of the virtual sensors using the kNN algorithm
    for virtual_sensor in virtual_sensors:
        neighbor_sensors = virtual_sensor.find_neighbors_sorted_by_distance()[0:NEIGHBORS_TO_ESTIMATE_MEASUREMENT_DIRECTLY]
        neighbors_measurements = [neighbor.measurement for neighbor in neighbor_sensors]

        # Calculating the sensor value through the arithmetic mean of its k nearest spatial neighbors
        virtual_sensor.inferred_measurement = sum(neighbors_measurements) / len(neighbor_sensors)
