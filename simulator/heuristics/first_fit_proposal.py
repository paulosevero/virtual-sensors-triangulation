# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment


def first_fit_proposal():
    """Simple missing data imputation algorithm that estimates the value of a virtual sensor using triangulation."""

    # Changing the heuristic name
    SimulationEnvironment.first().heuristic = f"First-Fit Proposal"

    virtual_sensors = SimulationEnvironment.first().virtual_sensors

    for virtual_sensor in virtual_sensors:

        sensors = virtual_sensor.find_neighbors_sorted_by_distance()
        covered_sensors = [sensors[0]]
        sensors.pop(0)

        for sensor in sensors:
            covered_sensors.append(sensor)

            # Checking if the virtual sensor is inside any triangle in a mesh of triangles formed with
            # Delaunay algorithm. If so, infers the sensor measurement using linear interpolation.
            triangles = virtual_sensor.can_be_triangulated(covered_sensors)

            if triangles:
                triangle = triangles[0]

                inference = virtual_sensor.calculate_measurement(
                    physical_sensors=triangle,
                    use_auxiliary_sensors=True,
                    weighted=False,
                )
                virtual_sensor.inferred_measurement = inference

                break
