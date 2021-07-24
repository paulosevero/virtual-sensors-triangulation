# USAGE EXAMPLE: python3 -B -m simulator -d "inmet_2020_rs" -a "proposal" -o "topo1.png"

# Python Libraries
import random
import argparse

# General-purpose Simulator Modules
from simulator.simulator import Simulator


def main(dataset, steps, algorithm, output):
    """ Executes the simulation.

    Parameters
    ==========
    dataset : string
        Dataset file (CSV format) or directory containing list of CSV files

    algorithm : string
        Heuristic algorithm that will be executed

    output : string
        Output file (image with topology)
    """

    Simulator.load_dataset(target=dataset)
    Simulator.run(steps=steps, algorithm=algorithm)
    Simulator.show_output(output_file=output)


if __name__ == '__main__':
    # Defining a seed value to enable reproducibility in case any stochastic behavior occurs during simulation
    random.seed(1)

    # Parsing named arguments from the command line
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', '-d', help='Dataset file or directory containing list of dataset files')
    parser.add_argument('--simulation-steps', '-s', help='Number of simulation steps')
    parser.add_argument('--algorithm', '-a', help='Heuristic algorithm to be executed')
    parser.add_argument('--output', '-o', help='Output file name', default='topology.png')
    args = parser.parse_args()

    # Calling the main method
    main(dataset=args.dataset, steps=args.simulation_steps, algorithm=args.algorithm, output=args.output)
