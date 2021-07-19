import argparse
import pandas as pd
from scipy.interpolate import LinearNDInterpolator

from simulator.misc.load_dataset import load_dataset
from simulator.topology import Topology
from simulator.sensor import Sensor


def calculate_measurement(physical_sensors, logical_sensor):
    """ Infers the value of a logical sensor by triangulating the
    value of existing physical sensors positioned across a given area.
    """

    topo = Topology.first()

    if len(physical_sensors) == 3:

        line_physensor1_physensor2 = line(physical_sensors[0].coordinates, physical_sensors[1].coordinates)
        line_physensor1_physensor3 = line(physical_sensors[0].coordinates, physical_sensors[2].coordinates)
        line_physensor2_physensor3 = line(physical_sensors[1].coordinates, physical_sensors[2].coordinates)

        line_physensor1_logical_sensor = line(physical_sensors[0].coordinates, logical_sensor.coordinates)
        line_physensor2_logical_sensor = line(physical_sensors[1].coordinates, logical_sensor.coordinates)
        line_physensor3_logical_sensor = line(physical_sensors[2].coordinates, logical_sensor.coordinates)

        intersection_physensor1_physensor2 = intersection(line_physensor1_physensor2, line_physensor3_logical_sensor)
        intersection_physensor1_physensor3 = intersection(line_physensor1_physensor3, line_physensor2_logical_sensor)
        intersection_physensor2_physensor3 = intersection(line_physensor2_physensor3, line_physensor1_logical_sensor)

        aux_sensor1 = Sensor(coordinates=intersection_physensor1_physensor2, type='auxiliary')
        aux_sensor2 = Sensor(coordinates=intersection_physensor1_physensor3, type='auxiliary')
        aux_sensor3 = Sensor(coordinates=intersection_physensor2_physensor3, type='auxiliary')

        # https://stackoverflow.com/questions/8285599/is-there-a-formula-to-change-a-latitude-and-longitude-into-a-single-number
        # https://stackoverflow.com/questions/4637031/geospatial-indexing-with-redis-sinatra-for-a-facebook-app
        measurement_aux_sensor1 = aux_sensor1.interpolate_measurement(sensor1=physical_sensors[0],
                                                                      sensor2=physical_sensors[1])
        measurement_aux_sensor2 = aux_sensor2.interpolate_measurement(sensor1=physical_sensors[0],
                                                                      sensor2=physical_sensors[2])
        measurement_aux_sensor3 = aux_sensor3.interpolate_measurement(sensor1=physical_sensors[1],
                                                                      sensor2=physical_sensors[2])

        inferred_measurement = (measurement_aux_sensor1 + measurement_aux_sensor2 + measurement_aux_sensor3) / 3

        topo.add_node(aux_sensor1)
        topo.add_node(aux_sensor2)
        topo.add_node(aux_sensor3)

        return(inferred_measurement)


def calculate_measurement_scipy(physical_sensors, logical_sensor):
    """ Infers the value of a logical sensor by triangulating the
    value of existing physical sensors positioned across a given area.
    """

    data = {'x': [sensor.coordinates[0] for sensor in physical_sensors],
            'y': [sensor.coordinates[1] for sensor in physical_sensors],
            'measurement': [sensor.measurement for sensor in physical_sensors]}

    df = pd.DataFrame(data)
    f = LinearNDInterpolator(list(zip(df['x'], df['y'])), df['measurement'])

    x, y = logical_sensor.coordinates
    inferred_value = float(f(x, y))

    return(inferred_value)


def line(coordinates_a, coordinates_b):
    a = (coordinates_a[1] - coordinates_b[1])
    b = (coordinates_b[0] - coordinates_a[0])
    c = (coordinates_a[0]*coordinates_b[1] - coordinates_b[0]*coordinates_a[1])
    return(a, b, -c)


def intersection(line1, line2):
    d = line1[0] * line2[1] - line1[1] * line2[0]
    dx = line1[2] * line2[1] - line1[1] * line2[2]
    dy = line1[0] * line2[2] - line1[2] * line2[0]
    if d != 0:
        x = dx / d
        y = dy / d
        return(x, y)
    else:
        return(False)


def distance_from_expected(inferred, expected):
    """
    """

    dist = abs(inferred - expected)

    precision = 100 - (dist * 100 / expected)

    return(precision)


def main(physical_sensors, attribute, logical_sensor, inference_method, output):
    load_dataset(target='inmet_2020_rs')

    topo = Topology.first()

    ref_sensor1 = Sensor.find_by(attribute_name=attribute, attribute_value=physical_sensors[0])[0]
    ref_sensor2 = Sensor.find_by(attribute_name=attribute, attribute_value=physical_sensors[1])[0]
    ref_sensor3 = Sensor.find_by(attribute_name=attribute, attribute_value=physical_sensors[2])[0]
    physical_sensors = [ref_sensor2, ref_sensor3, ref_sensor1]

    # Removing sensor with id=43 (Bento Gonçalves) to ease the visualization
    sensor43 = Sensor.find_by_id(43)
    topo.remove_node(sensor43)

    topo.add_edge(ref_sensor1, ref_sensor2)
    topo.add_edge(ref_sensor2, ref_sensor3)
    topo.add_edge(ref_sensor3, ref_sensor1)

    logical_sensor = Sensor.find_by(attribute_name=attribute, attribute_value=logical_sensor)[0]
    logical_sensor.type = 'logical'

    if inference_method == 'proposal':
        inference = calculate_measurement(physical_sensors=physical_sensors, logical_sensor=logical_sensor)
    elif inference_method == 'scipy_qhull':
        inference = calculate_measurement_scipy(physical_sensors=physical_sensors, logical_sensor=logical_sensor)

    precision = distance_from_expected(inferred=inference, expected=logical_sensor.measurement)

    print('==== Reference Sensors ====')
    print(f'    {ref_sensor1}')
    print(f'    {ref_sensor2}')
    print(f'    {ref_sensor3}')

    print('\n==== Result ====')
    print(f'    Sensor_{logical_sensor.id}. Alias: {logical_sensor.alias}. Coordinates: {logical_sensor.coordinates}')
    print(f'    Expected Value: {logical_sensor.measurement}ºC')
    print(f'    Inferred Value: {round(inference, 1)}ºC')
    print(f'    Precision: {round(precision, 1)}%')

    topo.draw(showgui=False, savefig=True, figname=output)


if __name__ == '__main__':
    # python3 -B -m simulator -p 35 -r 10 39 42 -a "id" -m "proposal" -o "topo1.png"

    # Parsing named arguments from the command line
    parser = argparse.ArgumentParser()

    # parser.add_argument('--dataset', '-d', help='Dataset')
    parser.add_argument('--point-of-interest', '-p', help='Point of interest whose measurement will be inferred')
    parser.add_argument('--reference-points', '-r', help='Reference points to guide the inference', nargs='*')
    parser.add_argument('--attribute', '-a', help='Attribute used to find the points within the dataset')
    parser.add_argument('--inference-method', '-m', help='Inference method')
    parser.add_argument('--output', '-o', help='Output file name', default='topology.png')
    args = parser.parse_args()

    # Calling the main method
    main(physical_sensors=args.reference_points, attribute=args.attribute, logical_sensor=args.point_of_interest,
         inference_method=args.inference_method, output=args.output)


# == REFERENCES ==
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.interpolate.LinearNDInterpolator.html
# https://www.inf.usi.ch/hormann/papers/Hormann.2014.BI.pdf
# https://github.com/scipy/scipy/blob/17e6c0e9223e619a3b65d4ddf8b77ee9c0bd1614/scipy/interpolate/interpnd.pyx
# https://github.com/pmav99/interpolation
# https://en.wikipedia.org/wiki/Multivariate_interpolation
# https://stackoverflow.com/questions/64881351/python-geospatial-interpolation-meteorological-data
