"""
===================
== Usage Example ==
===================
python3 -B -m simulator -d "inmet_2020_rs" -m "TEMPERATURA DO PONTO DE ORVALHO (°C)" -s 24 -n 3 -a "proposed_heuristic" -o "topo1.png"

=========================
== Metrics of Interest ==
=========================
PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)
TEMPERATURA DO PONTO DE ORVALHO (°C)
UMIDADE RELATIVA DO AR, HORARIA (%)
"""

# Python Libraries
import random
import argparse

# General-purpose Simulator Modules
from simulator.simulator import Simulator

# Helper variable that dictates whether the simulator execution will be profiled by 'cProfile'
PROFILING = False


def main(dataset, steps, sensors, algorithm, sensors_to_form_triangles, neighbors, metric, output):
    """ Executes the simulation.

    Parameters
    ==========
    dataset : string
        Dataset file (CSV format) or directory containing list of CSV files

    steps : int
        Number of simulation time steps

    sensors : int
        Number of virtual sensors whose measurements will be inferred

    algorithm : string
        Heuristic algorithm that will be executed

    sensors_to_form_triangles : int
        Number of sensors that can be used to form triangles

    neighbors : int
        Number of nearest neighbor sensors that can be used to estimate the value of a virtual sensor

    metric : string
        Metric to be inferred

    output : string
        Output file (image with topology)
    """

    Simulator.load_dataset(target=dataset, metric=metric)
    Simulator.run(steps=steps, metric=metric, algorithm=algorithm, sensors_to_form_triangles=sensors_to_form_triangles,
                  neighbors=neighbors, sensors=sensors)
    Simulator.show_output(output_file=output)


if __name__ == '__main__':
    # Defining a seed value to enable reproducibility in case any stochastic behavior occurs during simulation
    random.seed(1)

    # Parsing named arguments from the command line
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', '-d', help='Dataset file or directory containing list of dataset files')
    parser.add_argument('--simulation-steps', '-s', help='Number of simulation steps')
    parser.add_argument('--metric', '-m', help='Metric to be inferred')
    parser.add_argument('--number-of-sensors', '-n', help='Number of virtual sensors whose measurements will be inferred')
    parser.add_argument('--sensors-to-form-triangles', '-t', help='Number of physical sensors that can be used to form triangles', default=0)
    parser.add_argument('--number-of-neighbors', '-k', help='Number of nearest physical sensors that can be used to estimate the value of a virtual sensor', default=0)
    parser.add_argument('--algorithm', '-a', help='Heuristic algorithm to be executed')
    parser.add_argument('--output', '-o', help='Output file name', default='topology.png')
    args = parser.parse_args()

    # Calling the main method
    main(dataset=args.dataset, steps=args.simulation_steps, sensors=int(args.number_of_sensors), output=args.output, metric=args.metric,
         sensors_to_form_triangles=int(args.sensors_to_form_triangles), neighbors=int(args.number_of_neighbors), algorithm=args.algorithm)
