from simulator.misc.load_dataset import load_dataset
from simulator.topology import Topology
from simulator.sensor import Sensor


def main():
    load_dataset(target='inmet_2020_rs')

    print('== Sensors ==')
    for sensor in Sensor.all():
        print(f'    {sensor}')

    topo = Topology.first()

    sensor10 = Sensor.find_by_id(10)
    sensor39 = Sensor.find_by_id(39)
    sensor42 = Sensor.find_by_id(42)

    topo.add_edge(sensor10, sensor39)
    topo.add_edge(sensor39, sensor42)
    topo.add_edge(sensor42, sensor10)

    sensor35 = Sensor.find_by_id(35)
    inferred_value = None

    print('\n\n== Inference ==')
    print(f'    Expected Value: {sensor35.measurement}')
    print(f'    Inferred Value: {inferred_value}')

    topo.draw(showgui=False, savefig=True)


if __name__ == '__main__':
    main()
