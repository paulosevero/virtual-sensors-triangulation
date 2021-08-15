# Python Libraries
from itertools import combinations

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Helper Methods
from simulator.misc.helper_methods import triangle_weight
from simulator.misc.helper_methods import is_well_conditioned_triangle


def proposed_heuristic():
    """Proposed heuristic that calculates the value of a virtual sensor."""

    # Changing the heuristic name
    SimulationEnvironment.first().heuristic = f"Proposal"

    virtual_sensors = SimulationEnvironment.first().virtual_sensors
    for virtual_sensor in virtual_sensors:

        neighbor_sensors = virtual_sensor.find_neighbors_sorted_by_distance()

        # Checking if the virtual sensor is crossed by a line between two physical sensors. If so,
        # infers the sensor measurement with a simple linear interpolation between the two physical sensors
        aligned_sensors = virtual_sensor.crossed_by_line(neighbor_sensors)
        if aligned_sensors:
            inference = virtual_sensor.interpolate_measurement_aligned_sensors(
                sensor1=aligned_sensors[0], sensor2=aligned_sensors[1]
            )
            virtual_sensor.inferred_measurement = inference

        else:
            triangles = [
                triangle
                for triangle in combinations(neighbor_sensors, 3)
                if virtual_sensor.is_inside_triangle(triangle) and is_well_conditioned_triangle(triangle)
            ]

            # Finding the best triangle based on a custom weight function
            triangle = sorted(triangles, key=lambda t: triangle_weight(virtual_sensor, t))[0]

            # Estimating the value of the virtual sensor
            inference = virtual_sensor.calculate_measurement(
                physical_sensors=triangle, use_auxiliary_sensors=True, weighted=True
            )
            virtual_sensor.inferred_measurement = inference
