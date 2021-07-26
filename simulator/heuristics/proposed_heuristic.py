# Python Libraries
from scipy.spatial import Delaunay
from scipy.spatial import distance

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor


def proposed_heuristic(sensor_id):
    """ Proposed heuristic.
    """

    SimulationEnvironment.first().heuristic = 'Proposed Heuristic'

    virtual_sensor = Sensor.find_by_id(sensor_id)
    virtual_sensor.type = 'logical'

    valid_triangles = []
    all_sensors = virtual_sensor.find_neighbors_sorted_by_distance()
    sensors = [sensor.coordinates for sensor in all_sensors[0:4]]
    del all_sensors[:4]

    while len(all_sensors) > 0:
        sensor = all_sensors.pop(0)
        sensors.append(sensor.coordinates)

        triangles = [[Sensor.find_by('coordinates', sensors[i])[0] for i in list(triangle)]
                     for triangle in Delaunay(sensors, furthest_site=True).simplices]

        for triangle in triangles:
            if virtual_sensor.is_inside_triangle(triangle) and triangle not in valid_triangles:
                valid_triangles.append(triangle)

    best_triangle = sorted(valid_triangles, key=lambda t: distance.euclidean(virtual_sensor.coordinates,
                                                                             Sensor.get_triangle_centroid(t)))[0]

    inference = virtual_sensor.calculate_measurement(physical_sensors=best_triangle)
    virtual_sensor.inferred_measurement = inference
