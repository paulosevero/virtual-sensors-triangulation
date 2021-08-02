# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.topology import Topology


def first_fit_proposal():
    """ Simplified version of the proposed heuristic.
    """

    virtual_sensors = SimulationEnvironment.first().virtual_sensors

    for virtual_sensor in virtual_sensors:

        sensors = virtual_sensor.find_neighbors_sorted_by_distance()
        covered_sensors = [sensors[0]]
        sensors.pop(0)

        for sensor in sensors:
            covered_sensors.append(sensor)

            # Checking if the virtual sensor is crossed by a line between two physical sensors. If so,
            # infers the sensor measurement with a simple linear interpolation between the two physical sensors
            aligned_sensors = virtual_sensor.crossed_by_line(covered_sensors)
            if aligned_sensors:
                inference = virtual_sensor.interpolate_measurement_aligned_sensors(sensor1=aligned_sensors[0], sensor2=aligned_sensors[1])
                virtual_sensor.inferred_measurement = inference

                Topology.first().add_edge(aligned_sensors[0], aligned_sensors[1])
                break

                # Checking if the virtual sensor is inside any triangle in a mesh of triangles formed with Delaunay algorithm. If so,
                # infers the sensor measurement by interpolating values of different lines based on the barycentric distance
                triangles = virtual_sensor.can_be_triangulated(covered_sensors)
            elif triangles:
                triangle = triangles[0]

                inference = virtual_sensor.calculate_measurement(physical_sensors=triangle, use_auxiliary_sensors=True, weighted=False)
                virtual_sensor.inferred_measurement = inference

                break
