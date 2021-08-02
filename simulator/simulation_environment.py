# Python Libraries
import random

# General-Purpose Components
from simulator.misc.object_collection import ObjectCollection

# Simulator Components
from simulator.components.sensor import Sensor
from simulator.components.topology import Topology


class SimulationEnvironment(ObjectCollection):
    """ This class allows the creation objects that
    control the whole life cycle of simulations.
    """

    # Class attribute that allows the class to use ObjectCollection methods
    instances = []

    def __init__(self, steps, dataset, heuristic):
        """ Initializes the simulation object.

        Parameters
        ==========
        dataset : string
            Name of the dataset file or directory containing a list of dataset files

        heuristic : string
            Heuristic algorithm that will be executed during simulation
        """

        # Auto increment identifier
        self.id = SimulationEnvironment.count() + 1

        # List object that can be used to store any event that occurs during the simulation
        self.metrics = []

        # Dataset
        self.dataset = None

        # Heuristic algorithm used to infer the value of virtual sensors
        self.heuristic = None

        # Simulation steps
        self.steps = steps
        self.current_step = 1

        # Logic sensors whose measurements will be estimated
        self.virtual_sensors = []

        # Adding the new object to the list of instances of its class
        SimulationEnvironment.instances.append(self)


    def run(self, sensors, heuristic):
        """ Triggers the set of events that ocurr during the simulation.
        """

        # Picking 'n' virtual sensors whose measurements will be estimated
        self.virtual_sensors = random.sample([sensor for sensor in Sensor.all() if sensor.type == 'physical'], sensors)
        for sensor in self.virtual_sensors:
            sensor.type = 'logical'

        # The simulation goes on while the stopping criteria is not met
        while self.current_step <= self.steps:
            # Updating system state
            self.update_system_state()

            # Running a set of user-defined tasks
            heuristic()

            # Removing temporary items in the topology
            self.clean_environment()

            # Collecting simulation metrics for the current step and moving to the next step
            self.collect_metrics()
            self.current_step += 1


    def update_system_state(self):
        """
        """

        # Updating sensors measurements and their timestamps
        for sensor in [sensor for sensor in Sensor.all() if sensor.type == 'physical' or sensor.type == 'logical']:
            sensor.measurement = sensor.measurements[self.current_step - 1]
            sensor.timestamp = sensor.timestamps[self.current_step - 1]


    def clean_environment(self):
        """
        """

        # Removing auxiliary sensors and any links used to triangulate measurements of a logical sensor
        Topology.first().remove_edges_from(list(Topology.first().edges()))

        auxiliary_sensors = [sensor for sensor in Sensor.all() if sensor.type == 'auxiliary']

        Sensor.instances = [sensor for sensor in Sensor.all() if sensor.type == 'physical' or sensor.type == 'logical']
        Topology.first().remove_nodes_from(auxiliary_sensors)


    def collect_metrics(self):
        """ Stores relevant events that occur during the simulation.
        """

        measurements = []

        for sensor in Sensor.all():

            if sensor.inferred_measurement is not None:

                measurements.append({'sensor': sensor.id, 'timestamp': sensor.timestamp,
                                     'real_measurement': sensor.measurement,
                                     'inference': sensor.inferred_measurement})

        step_metrics = {'step': self.current_step, 'measurements': measurements}

        self.metrics.append(step_metrics)
