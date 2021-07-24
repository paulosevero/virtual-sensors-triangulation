# Python Libraries
import random

# General-purpose Simulator Modules
from simulator.simulation_environment import SimulationEnvironment

# Simulator Components
from simulator.components.sensor import Sensor


def proposed_heuristic():
    """ Proposed heuristic.
    """

    time_step = SimulationEnvironment.first().current_step
    random_sensor = random.choice(Sensor.all())

    print(f'[{time_step}] Random Sensor: {random_sensor.id}')


# Q1: How to structure the simulation (number of steps, infer measurement from which sensor)?
# Q2: Which metrics to collect?
