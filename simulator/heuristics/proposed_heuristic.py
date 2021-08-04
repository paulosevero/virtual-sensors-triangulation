# Python Libraries
from itertools import combinations

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Helper Methods
from simulator.misc.helper_methods import triangle_weight
from simulator.misc.helper_methods import is_well_conditioned_triangle


def proposed_heuristic():
    """ Proposed heuristic that calculates the value of
    a virtual sensor. A description of the heuristic is given next.

    'IF' the virtual sensor is within a line formed by two physical sensors with known values:
        Calculate the virtual sensor value using a simple linear interpolation
    'ELSE IF' the virtual sensor is within a triangle formed by three physical sensors with known values:
        Calculate the virtual sensor value using a custom triangulation technique
    'ELSE':
        Calculate the virtual sensor value based on the weighted mean of its nearest spatial neighbor sensors.
        More specifically, the closest the neighbor sensor is from the virtual sensor the higher is its weight.
    """

    # Parameter that define the number of neighbor sensors that will be used to form the triangles to estimate the virtual sensor value
    NEIGHBORS_TO_FORM_TRIANGLES = SimulationEnvironment.first().sensors_to_form_triangles

    # Parameter that define the number of neighbor sensors that will be used to estimate the virtual sensor value (using weighted mean)
    NEIGHBORS_TO_ESTIMATE_MEASUREMENT_DIRECTLY = SimulationEnvironment.first().neighbors

    # Adding the number of neighbors (given by the 'k' parameter) and the number of sensors
    # used to create triangles (given by α) to the heuristic's name to ease post-simulation analysis
    SimulationEnvironment.first().heuristic = f'Proposal (k={NEIGHBORS_TO_ESTIMATE_MEASUREMENT_DIRECTLY}, α={NEIGHBORS_TO_FORM_TRIANGLES})'


    virtual_sensors = SimulationEnvironment.first().virtual_sensors
    for virtual_sensor in virtual_sensors:

        neighbor_sensors = virtual_sensor.find_neighbors_sorted_by_distance()
        # Checking if the virtual sensor is crossed by a line between two physical sensors. If so,
        # infers the sensor measurement with a simple linear interpolation between the two physical sensors
        aligned_sensors = virtual_sensor.crossed_by_line(neighbor_sensors)

        if aligned_sensors:
            inference = virtual_sensor.interpolate_measurement_aligned_sensors(sensor1=aligned_sensors[0], sensor2=aligned_sensors[1])
            virtual_sensor.inferred_measurement = inference

        else:
            neighbor_sensors = neighbor_sensors[0:NEIGHBORS_TO_FORM_TRIANGLES]

            valid_triangles = [triangle for triangle in combinations(neighbor_sensors, 3)
                               if virtual_sensor.is_inside_triangle(triangle) and is_well_conditioned_triangle(triangle)]

            # Checking if the virtual sensor is inside any triangle in a mesh of triangles formed with Delaunay algorithm. If so,
            # infers the sensor measurement by interpolating values of different lines based on the barycentric distance
            if len(valid_triangles) > 0:
                valid_triangles = sorted(valid_triangles, key=lambda t: triangle_weight(virtual_sensor=virtual_sensor, triangle=t))

                best_triangle = valid_triangles[0]
                inference = virtual_sensor.calculate_measurement(physical_sensors=best_triangle, use_auxiliary_sensors=True, weighted=True)
                virtual_sensor.inferred_measurement = inference

            # If the virtual sensor is not inside any triangle, estimates its measurement based on the values
            # of its k-nearest neighbors in a weighted arithmetic mean which gives a higher weight to the
            # neighbor sensors located closer to the virtual sensor
            else:
                neighbor_sensors = neighbor_sensors[0:NEIGHBORS_TO_ESTIMATE_MEASUREMENT_DIRECTLY]

                inference = virtual_sensor.calculate_measurement(physical_sensors=neighbor_sensors, use_auxiliary_sensors=False,
                                                                 weighted=True)
                virtual_sensor.inferred_measurement = inference
