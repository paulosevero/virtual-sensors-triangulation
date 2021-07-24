# Python Libraries
# import simpy

# General-Purpose Components
from simulator.misc.object_collection import ObjectCollection

# Simulator Components
# from simulator.components.topology import Topology
# from simulator.components.sensor import Sensor


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

        # Adding the new object to the list of instances of its class
        SimulationEnvironment.instances.append(self)


    def run(self, sensor_id, heuristic):
        """ Triggers the set of events that ocurr during the simulation.
        """

        # The simulation goes on while the stopping criteria is not met
        while self.current_step <= self.steps:
            # Running a set of user-defined tasks
            heuristic(sensor_id=sensor_id)

            # Collecting simulation metrics for the current step and moving to the next step
            self.collect_metrics()
            self.current_step += 1


    def collect_metrics(self):
        """ Stores relevant events that occur during the simulation.
        """

        step_metrics = {'step': self.current_step, 'awesome_metric': 1}

        self.metrics.append(step_metrics)
