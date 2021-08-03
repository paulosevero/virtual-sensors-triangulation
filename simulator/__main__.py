"""
===================
== Usage Example ==
===================
python3 -B -m simulator -d "inmet_2020_rs" -m "TEMPERATURA DO PONTO DE ORVALHO (°C)" -s 24 -n 3 -a "proposed_heuristic" -o "topo1.png"

=========================
== Metrics of Interest ==
=========================
PRECIPITAÇÃO TOTAL, HORÁRIO (mm)
PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)
RADIACAO GLOBAL (Kj/m²)
TEMPERATURA DO PONTO DE ORVALHO (°C)
UMIDADE RELATIVA DO AR, HORARIA (%)
VENTO, VELOCIDADE HORARIA (m/s)
"""

# Python Libraries
import random
import argparse

# General-purpose Simulator Modules
from simulator.simulator import Simulator


def main(dataset, steps, sensors, algorithm, metric, output):
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

    Simulator.load_dataset(target=dataset, metric=metric)
    Simulator.run(steps=steps, algorithm=algorithm, sensors=sensors)
    Simulator.show_output(output_file=output)


if __name__ == '__main__':
    # Defining a seed value to enable reproducibility in case any stochastic behavior occurs during simulation
    random.seed(1)  # VALID SEED VALUES: [11, 111]

    # Parsing named arguments from the command line
    parser = argparse.ArgumentParser()

    parser.add_argument('--dataset', '-d', help='Dataset file or directory containing list of dataset files')
    parser.add_argument('--simulation-steps', '-s', help='Number of simulation steps')
    parser.add_argument('--metric', '-m', help='Metric to be inferred')
    parser.add_argument('--number-of-sensors', '-n', help='Number of virtual sensors whose measurements will be infered')
    parser.add_argument('--algorithm', '-a', help='Heuristic algorithm to be executed')
    parser.add_argument('--output', '-o', help='Output file name', default='topology.png')
    args = parser.parse_args()

    # Calling the main method
    main(dataset=args.dataset, steps=args.simulation_steps, sensors=int(args.number_of_sensors),
         algorithm=args.algorithm, metric=args.metric, output=args.output)
