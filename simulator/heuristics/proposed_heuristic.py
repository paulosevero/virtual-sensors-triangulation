# Python Libraries
import random
import itertools
from scipy.spatial import Delaunay

# Helper Methods
from simulator.misc.helper_methods import matrix_determinant

# Simulator Components
from simulator.components.topology import Topology
from simulator.components.sensor import Sensor


def proposed_heuristic(sensor_id):
    """ Proposed heuristic.
    """

    virtual_sensor = Sensor.find_by_id(sensor_id)
    virtual_sensor.type = 'logical'

    sensors = virtual_sensor.find_neighbors_sorted_by_distance()
    covered_sensors = [sensors[0]]
    sensors.pop(0)

    inference_completed = False

    for sensor in sensors:
        covered_sensors.append(sensor)

        # VERIFICAR SE ESTÁ ALINHADO
        combinations = itertools.combinations(covered_sensors, 2)

        for pair in combinations:
            determinant = matrix_determinant(coord1=pair[0].coordinates, coord2=virtual_sensor.coordinates,
                                             coord3=pair[1].coordinates)

            if determinant == 0 and virtual_sensor.is_inside_line(sensor1=pair[0], sensor2=pair[1]):
                inferred_measurement = virtual_sensor.interpolate_measurement_aligned_sensors(sensor1=pair[0],
                                                                                              sensor2=pair[1])
                print(f'INFERRED VALUE OF SENSOR WITHIN LINE (SENSOR_{pair[0].id} AND SENSOR_{pair[1].id})')
                print(f'    Covered Sensors: {len(covered_sensors)}')
                print(f'    Expected: {virtual_sensor.measurement}')
                print(f'    Inferred: {inferred_measurement}')

                Topology.first().add_edge(pair[0], pair[1])

                inference_completed = True
                break

        if inference_completed:
            break

        # VERIFICAR SE ESTÁ DENTRO DE ALGUM TRIÂNGULO
        if len(covered_sensors) >= 3:
            triangles = Sensor.create_delaunay_triangles(physical_sensors=covered_sensors)

            for triangle in triangles:

                if virtual_sensor.is_inside_triangle(triangle=triangle):
                    inferred_measurement = virtual_sensor.calculate_measurement(physical_sensors=triangle)

                    print('INFERRED VALUE OF SENSOR WITHIN TRIANGLE')
                    print(f'    Covered Sensors: {len(covered_sensors)}')
                    print(f'    Expected: {virtual_sensor.measurement}')
                    print(f'    Inferred: {inferred_measurement}')

                    inference_completed = True
                    break

            if inference_completed:
                break
