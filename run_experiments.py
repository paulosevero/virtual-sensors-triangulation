# Python Libraries
import csv
import os
import re
import random
import numpy as np

VERBOSE = 1


def run_simulation(dataset, metric, steps, virtual_sensors, k, heuristic_name):
    """Executes the simulation with specified parameters."""

    # Adjusting the simulation command based on the parameters
    cmd = f'python3 -B -m simulator -d "{dataset}" -m "{metric}" -s {steps} -n {virtual_sensors} -k {k} -a "{heuristic_name}"'

    # Running the simulation with the specified parameters
    stream = os.popen(cmd)
    output = stream.read()

    # Parsing simulation results
    rmse = float(re.findall("\d+\.\d+", output.splitlines()[5])[0])
    mae = float(re.findall("\d+\.\d+", output.splitlines()[6])[0])
    result = {
        "heuristic": heuristic_name,
        "metric": metric,
        "k": k,
        "rmse": rmse,
        "mae": mae,
    }

    return result


def main():
    random.seed(1)
    np.random.seed(1)
    np.random.default_rng(1)

    # General (fixed) experiment parameters
    dataset = "inmet_2020_south"
    metrics = [
        "RADIACAO GLOBAL (Kj/m²)",
        "PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)",
        "TEMPERATURA DO PONTO DE ORVALHO (°C)",
    ]

    steps = 12  # Simulation time steps (e.g., 12, 24, 168, etc.)
    virtual_sensors = 3  # Number of random virtual sensors whose values will be estimated

    # Specific experiment parameters (which are tested exhaustively)
    heuristics = [
        {"name": "proposed_heuristic", "k": False},
        {"name": "first_fit_proposal", "k": False},
        {"name": "idw", "k": True},
        {"name": "knn", "k": True},
    ]

    # Number of nearest neighbor physical sensors that will be used to estimate the value of virtual sensors
    k_values = [1, 2, 4, 8, 16, 32]

    # List that stores the experiments results
    results = []

    # Helper variable that stores the number of simulations performed
    execution_count = 1

    # Executing simulations
    for metric in metrics:
        for heuristic in heuristics:
            heuristic_name = heuristic["name"]
            if heuristic["k"]:
                for k in k_values:
                    # Executing simulation
                    result = run_simulation(dataset, metric, steps, virtual_sensors, k, heuristic_name)

                    # Storing results in the 'results' list
                    results.append(result)

                    if VERBOSE >= 1:
                        # Printing the results of the current simulation
                        print(f"{result}")

            else:
                # Executing simulation with a fixed value (i.e., 0) in the unused parameter k
                result = run_simulation(dataset, metric, steps, virtual_sensors, 0, heuristic_name)

                # Storing results in the 'results' list
                results.append(result)

                if VERBOSE >= 1:
                    # Printing the results of the current simulation
                    print(f"{result}")

    # Exporting results
    with open("sensitivity_analysis.csv", mode="w") as csv_file:

        # Writing CSV header
        field_names = ["heuristic", "metric", "k", "rmse", "mae"]
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        # Writing CSV body
        for row in results:
            writer.writerow(row)


if __name__ == "__main__":
    main()
