# Python Libraries
import csv
import os
import re

VERBOSE = 0


def run_simulation(dataset, metric, steps, virtual_sensors, k, alpha, heuristic_name):
    """ Executes the simulation with specified parameters.
    """

    # Adjusting the simulation command based on the parameters
    cmd = f'python3 -B -m simulator -d "{dataset}" -m "{metric}" -s {steps} -n {virtual_sensors} -k {k} -t {alpha} -a "{heuristic_name}"'  # noqa: E501

    # Running the simulation with the specified parameters
    stream = os.popen(cmd)
    output = stream.read()

    # Parsing simulation results
    rmse = float(re.findall("\d+\.\d+", output.splitlines()[5])[0])  # noqa: W605
    mae = float(re.findall("\d+\.\d+", output.splitlines()[6])[0])  # noqa: W605
    result = {'heuristic': heuristic_name, 'metric': metric, 'k': k, 'alpha': alpha, 'rmse': rmse, 'mae': mae}

    return(result)


def main():
    # General (fixed) experiment parameters
    dataset = 'inmet_2020_south'
    metrics = ['TEMPERATURA DO PONTO DE ORVALHO (°C)',
               'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
               'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
               'RADIACAO GLOBAL (Kj/m²)',
               'UMIDADE RELATIVA DO AR, HORARIA (%)',
               'VENTO, VELOCIDADE HORARIA (m/s)']


    steps = 168  # Simulation time steps
    virtual_sensors = 10  # Number of random virtual sensors whose values will be estimated

    # Specific experiment parameters (which are tested exhaustively)
    heuristics = [{'name': 'idw', 'k': True, 'alpha': False},
                  {'name': 'knn', 'k': True, 'alpha': False},
                  {'name': 'first_fit_proposal', 'k': True, 'alpha': False},
                  {'name': 'proposed_heuristic', 'k': True, 'alpha': True}]
    k_values = range(1, 31)  # Number of nearest neighbor physical sensors that will be used to estimate the value of virtual sensors
    k_values = [3]  # Number of nearest neighbor physical sensors that will be used to estimate the value of virtual sensors
    alpha_values = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]  # Number of physical sensors that will be used to create triangles
    alpha_values = [10]  # Number of physical sensors that will be used to create triangles

    # List that stores the experiments results
    results = []
    execution_count = 1  # Helper variable that stores the number of simulations performed

    # Executing simulations
    for metric in metrics:
        for heuristic in heuristics:
            heuristic_name = heuristic['name']
            if heuristic['k']:
                for k in k_values:
                    if heuristic['alpha']:
                        for alpha in alpha_values:
                            # Executing simulation
                            result = run_simulation(dataset, metric, steps, virtual_sensors, k, alpha, heuristic_name)

                            if VERBOSE >= 1:
                                # Printing the results of the current simulation
                                print(f'[{execution_count}] {result}')

                            # Storing results in the 'results' list
                            results.append(result)
                            execution_count += 1
                    else:
                        # Executing simulation with a fixed value (i.e., 1) in the unused parameter alpha
                        result = run_simulation(dataset, metric, steps, virtual_sensors, k, 1, heuristic_name)

                        if VERBOSE >= 1:
                            # Printing the results of the current simulation
                            print(f'{result}')

                        # Storing results in the 'results' list
                        results.append(result)
            else:
                # Executing simulation with a fixed value (i.e., 1) in the unused parameters k and alpha
                result = run_simulation(dataset, metric, steps, virtual_sensors, 1, 1, heuristic_name)

                if VERBOSE >= 1:
                    # Printing the results of the current simulation
                    print(f'{result}')

                # Storing results in the 'results' list
                results.append(result)


    if VERBOSE >= 1:
        # Displaying the results of all executed simulations
        print('==== SIMULATION RESULTS ====')
        for result in results:
            print(f'    {result}')


    # Exporting results
    with open('sensitivity_analysis.csv', mode='w') as csv_file:

        # Writing CSV header
        field_names = ['heuristic', 'metric', 'k', 'alpha', 'rmse', 'mae']
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()

        # Writing CSV body
        for row in results:
            writer.writerow(row)


if __name__ == '__main__':
    main()
