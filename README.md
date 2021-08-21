## Motivation

Virtual sensors are software entities that allow the estimation, through models, of critical variables in a given environment. Implementing virtual sensors in IoT environments is emerging to address a significant limitation in smart farms — the inability to place physical sensors in specific locations or the logical replacement of faulty physical sensors.

For that, metrics can be modeled computationally to estimate the values measured by a sensor without installing it physically in the specified location. The monitoring and control of its variables are of great importance, as they are directly related to increased productivity, production quality, as well as the safety of equipment and employees involved in the smart farm operation.

We introduce a new approach to estimate values of a virtual position (so-called virtual sensor) based on values collected from physical sensors within the same region. More specifically, our method creates a mesh of well-conditioned triangles using the sensors with known observations. From that point, we pick the triangle closer to the virtual sensor and impute the measurement of virtual sensors based on interpolated values of nearby reference points within that triangle.

## Usage Instructions


Please note that this tutorial is based on Debian-based Linux distributions. Therefore, you may have to make some adjustments to follow the instructions below in other operating systems. Also, we assume you already have Python3 (>=3.7.1) installed.

### Prerequisites

We use some Python libraries to improve the readability and consistency of our code. Also, some visualization features depend on couple of Linux packages that must be installed too. Therefore, a good starting point is installing these dependencies:

```bash
sudo apt install libgeos-dev libproj-dev proj-data proj-bin libbz2-dev libblas3 liblapack3 liblapack-dev libblas-dev libatlas-base-dev gfortran

pip3 install poetry
pip3 install black
```

From now on, we can use Poetry to automatically install any other dependency our project needs automatically inside a virtual environment. To do so, enter inside our project's directory (e.g.: `cd [path-to-project]`) and type the following commands:

```bash
poetry shell
poetry install
```

Once the installation is finished, we're good to go!

### Running

To execute a single experiment, we can run the following command:

```bash
python3 -B -m simulator -d [dataset_file] -m [metric_of_interest] -s [timespan] -n [n_sensors] -k [n_neighbors] -a [technique]
```

Conversely, you can run all experiments with the same experiments used in the paper with the following command (that will output a CSV file with the results of our proposal, the simple triangulation method, and the sensitivity analysis of kNN and IDW):

```bash
python3 -B run_experiments.py
```
