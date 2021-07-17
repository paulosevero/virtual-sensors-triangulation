# https://math.stackexchange.com/questions/2841445/all-the-possible-combinations-to-create-triangles-in-a-determined-graph
# https://stackoverflow.com/questions/2049582/how-to-determine-if-a-point-is-in-a-2d-triangle
# https://www.geeksforgeeks.org/check-whether-a-given-point-lies-inside-a-triangle-or-not/

# External libraries
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt


######################
## HELPER FUNCTIONS ##
######################
def define_rectangular_map_dimensions(map_partitions):
    """ Finds a pair of values for X and Y that
    form a rectangular map of size 'map_partitions'.
    """

    x = float('-inf')
    y = float('inf')

    for i in range(1, map_partitions+1):
        for j in range(1, map_partitions+1):
            if i * j == map_partitions and abs(i - j) < abs(x - y):
                x = i
                y = j

    return([x, y])


def create_cartesian_plane(x_size, y_size):
    """ Creates a map representation using
    the cartesian plane coordinates system.
    """

    map_coordinates = []

    for x in range(0, x_size):
        for y in range(0, y_size):
            map_coordinates.append((x, y))

    return(map_coordinates)


def draw_network_topology():
    """ Creates an image of the network topology.
    """

    fig = plt.figure()
    plt.margins(0.06)

    sensor1 = find_sensor(key='id', value=1)
    sensor2 = find_sensor(key='id', value=2)
    sensor3 = find_sensor(key='id', value=3)
    logical_sensor = find_sensor(key='id', value=4)
    print(sensor1)
    print(sensor2)
    print(sensor3)
    print(logical_sensor)

    aux_sensor1 = intersection(line(sensor1[1]['coordinates'], sensor1[1]['coordinates']), line(sensor2[1]['coordinates'], logical_sensor[1]['coordinates']))
    aux_sensor2 = intersection(line(sensor2[1]['coordinates'], sensor1[1]['coordinates']), line(sensor3[1]['coordinates'], logical_sensor[1]['coordinates']))
    aux_sensor3 = intersection(line(sensor2[1]['coordinates'], sensor3[1]['coordinates']), line(sensor1[1]['coordinates'], logical_sensor[1]['coordinates']))

    aux_sensor1 = add_sensor(coordinates=aux_sensor1, type='auxiliary')
    aux_sensor2 = add_sensor(coordinates=aux_sensor2, type='auxiliary')
    aux_sensor3 = add_sensor(coordinates=aux_sensor3, type='auxiliary')
    case1(physical_sensors=[sensor1, sensor3], logical_sensor=aux_sensor1)
    case1(physical_sensors=[sensor2, sensor1], logical_sensor=aux_sensor2)
    case1(physical_sensors=[sensor2, sensor3], logical_sensor=aux_sensor3)

    inferred_temp = (aux_sensor1[1]['temperature'] + aux_sensor2[1]['temperature'] + aux_sensor3[1]['temperature']) / 3

    logical_sensor[1]['temperature'] = round(inferred_temp, 2)

    print(f'sensor1 = {sensor1}')
    print(f'sensor2 = {sensor2}')
    print(f'sensor3 = {sensor3}')

    print(f'aux_sensor1 = {aux_sensor1}')
    print(f'aux_sensor2 = {aux_sensor2}')
    print(f'aux_sensor3 = {aux_sensor3}')

    s = (sensor1[1]['temperature'] + sensor2[1]['temperature'] + sensor3[1]['temperature'])/3
    print(f'{logical_sensor}. Expected Temperature: 0.3. Simple temp: {s}')
    aux_sensor1[1]['temperature'] = round(aux_sensor1[1]['temperature'], 2)
    aux_sensor2[1]['temperature'] = round(aux_sensor2[1]['temperature'], 2)
    aux_sensor3[1]['temperature'] = round(aux_sensor3[1]['temperature'], 2)


    # plt.scatter(aux_sensor1[1]['coordinates'][0], aux_sensor1[1]['coordinates'][1], s=200, c='#008000')
    # plt.scatter(aux_sensor2[1]['coordinates'][0], aux_sensor2[1]['coordinates'][1], s=200, c='#008000')
    # plt.scatter(aux_sensor3[1]['coordinates'][0], aux_sensor3[1]['coordinates'][1], s=200, c='#008000')


    # abs_coord1 = (coord1[0] * 10 + coord1[1])
    # abs_coord2 = (coord2[0] * 10 + coord2[1])
    # abs_coord3 = (coord3[0] * 10 + coord3[1])
    # inferred_temperature = (physical_sensor1[1]['temperature'] + (abs_coord2 - abs_coord1) *
            # ((physical_sensor2[1]['temperature'] - physical_sensor1[1]['temperature'])/(abs_coord3 - abs_coord1)))



    pos = {}
    colors = []
    labels = {}
    for sensor in TOPOLOGY.nodes(data=True):
        pos[sensor[0]] = sensor[1]['coordinates']

        sensor_id = sensor[1]['id']
        sensor_coordinates = f'Lat:{round(sensor[1]["coordinates"][0], 2)}\nLong:{round(sensor[1]["coordinates"][1], 2)}'
        sensor_temperature = f'Temp:{sensor[1]["temperature"]}ºC'
        labels[sensor[0]] = f'ID:{sensor_id}\n{sensor_coordinates}\n{sensor_temperature}'

        if sensor[1]['type'] == 'physical':
            colors.append('black')
        elif sensor[1]['type'] == 'logical':
            colors.append('red')
        elif sensor[1]['type'] == 'auxiliary':
            colors.append('green')

    nx.draw(TOPOLOGY, pos=pos, labels=labels, node_size=600, font_size=3, font_color='white', node_color=colors, font_weight='bold')

    fig.savefig('topology.png', dpi=200)
    # plt.show()


def create_topology(sensors):
    """
    """

    topology = nx.Graph()

    # Creating nodes
    for sensor in sensors:
        topology.add_node(len(topology.nodes())+1, id=len(topology.nodes())+1, coordinates=sensor['coordinates'],
            temperature=sensor['temperature'], type=sensor['type'], name=sensor['name'])

    # Creating links between nodes
    # if len(sensors) == 2:
    #     points = list(topology.nodes(data=True))
    # else:
    #     points = list(topology.nodes(data=True)) + [list(topology.nodes(data=True))[0]]

    # for i in range(0, len(points)-1):
    #     topology.add_edge(points[i][0], points[i+1][0])

    return(topology)


def add_sensor(coordinates, temperature=float('inf'), type='logical'):
    """
    """

    TOPOLOGY.add_node(len(TOPOLOGY.nodes())+1, id=len(TOPOLOGY.nodes())+1,
        coordinates=coordinates, temperature=temperature, type=type)

    sensor = find_sensor(key='coordinates', value=coordinates)
    return(sensor)


def find_sensor(key, value):
    """
    """

    sensor = next((sensor for sensor in TOPOLOGY.nodes(data=True)
            if sensor[1][key] == value), None)

    return(sensor)


####################
## MATH FUNCTIONS ##
####################
def matrix_determinant(coord1, coord2, coord3):
    """
    """

    matrix = [[coord1[0], coord1[1], 1], [coord2[0], coord2[1], 1], [coord3[0], coord3[1], 1]]

    a = matrix[0][0] * matrix[1][1] * matrix[2][2]
    b = matrix[0][1] * matrix[1][2] * matrix[2][0]
    c = matrix[0][2] * matrix[1][0] * matrix[2][1]
    d1 = a + b + c

    d = matrix[0][2] * matrix[1][1] * matrix[2][0]
    e = matrix[0][0] * matrix[1][2] * matrix[2][1]
    f = matrix[0][1] * matrix[1][0] * matrix[2][2]
    d2 = d + e + f

    determinant = d1 - d2

    return(determinant)


def triangle_area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def sensor_is_inside_triangle(triangle, logical_sensor):

    x1 = triangle[0][1]['coordinates'][0]
    y1 = triangle[0][1]['coordinates'][1]

    x2 = triangle[1][1]['coordinates'][0]
    y2 = triangle[1][1]['coordinates'][1]

    x3 = triangle[2][1]['coordinates'][0]
    y3 = triangle[2][1]['coordinates'][1]

    x = logical_sensor[1]['coordinates'][0]
    y = logical_sensor[1]['coordinates'][1]

    # Calculate area of triangle ABC
    A = triangle_area(x1, y1, x2, y2, x3, y3)

    # Calculate area of triangle PBC
    A1 = triangle_area(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PAC
    A2 = triangle_area(x1, y1, x, y, x3, y3)

    # Calculate area of triangle PAB
    A3 = triangle_area(x1, y1, x2, y2, x, y)

    return(A == A1 + A2 + A3)


def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return(A, B, -C)


def intersection(L1, L2):
    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        return(x,y)
    else:
        return(False)


def case1(physical_sensors, logical_sensor):
    """
    """

    physical_sensor1 = physical_sensors[0]
    physical_sensor2 = physical_sensors[1]

    coord1 = physical_sensor1[1]['coordinates']
    coord2 = logical_sensor[1]['coordinates']
    coord3 = physical_sensor2[1]['coordinates']

    determinant = matrix_determinant(coord1, coord2, coord3)
    
    abs_coord1 = coord1[0] * 1000000 * (-(coord1[1] * 1000000))
    abs_coord2 = coord2[0] * 1000000 * (-(coord2[1] * 1000000))
    abs_coord3 = coord3[0] * 1000000 * (-(coord3[1] * 1000000))
    
    point_within_line = ((abs_coord2 > abs_coord1 and abs_coord2 < abs_coord3) or
        (abs_coord2 < abs_coord1 and abs_coord2 > abs_coord3))

    # print(f'Coordinates: {coord2}. Matrix Determinant: {determinant}. Point within Line: {point_within_line}')
    # print(f'    abs_coord1 = {abs_coord1}')
    # print(f'    abs_coord2 = {abs_coord2}')
    # print(f'    abs_coord3 = {abs_coord3}')

    if determinant == 0 and point_within_line:
        inferred_temperature = (physical_sensor1[1]['temperature'] + (abs_coord2 - abs_coord1) *
            ((physical_sensor2[1]['temperature'] - physical_sensor1[1]['temperature'])/(abs_coord3 - abs_coord1)))

        # print(f'inferred_temperature = {inferred_temperature}')

        logical_sensor[1]['temperature'] = inferred_temperature

        return(logical_sensor[1]['temperature'])

    else:
        return(float('inf'))


# Specs for the physical sensors
# sensors = [{'coordinates': (0,0), 'temperature': 40, 'type': 'physical'},
#            {'coordinates': (2,2), 'temperature': 60, 'type': 'physical'},
#            {'coordinates': (1.5,0), 'temperature': 49, 'type': 'physical'},
#            {'coordinates': (1,4), 'temperature': 55, 'type': 'physical'}]

sensors = [
    { 'coordinates': (-30.34, -54.31), 'temperature': 21.5, 'type': 'physical', 'name': 'São Gabriel' }, # são gabriel
    { 'coordinates': (-30.54, -52.52), 'temperature': 15.3, 'type': 'physical', 'name': 'Encruzilhada do Sul' }, # encruzilhada do sul
    { 'coordinates': (-28.63, -53.61), 'temperature': 16.4, 'type': 'physical', 'name': 'Cruz Alta' }, # cruz alta

]




# Creating topology with physical sensors
TOPOLOGY = create_topology(sensors=sensors)

# Adding coordinates of logical sensor
logical_sensor = add_sensor(coordinates=(-29.72, -53.72)) # santa maria (15.6)

# Checking if the logical sensor is collinear to two physical sensors
# physical_sensors = [find_sensor(key='coordinates', value=(0,0)), find_sensor(key='coordinates', value=(2,2))]
# inferred_temperature = case1(physical_sensors=physical_sensors, logical_sensor=logical_sensor)

# Creating triangles between physical sensors
# for node_a in TOPOLOGY.nodes(data=True):
#     for node_b in TOPOLOGY.nodes(data=True):
#         if node_a != node_b and node_a[1]['type'] == 'physical' and node_b[1]['type'] == 'physical':
#             TOPOLOGY.add_edge(node_a[0], node_b[0])


# triangles = []
# for (i, j) in TOPOLOGY.edges():
#     for k in TOPOLOGY.neighbors(i):
#         if k in TOPOLOGY.neighbors(j):
#             sensor1 = find_sensor(key='id', value=i)
#             sensor2 = find_sensor(key='id', value=j)
#             sensor3 = find_sensor(key='id', value=k)

#             sensors = sorted([sensor1, sensor2, sensor3], key=lambda s: s[1]['id'])

#             if sensors not in triangles:
#                 triangles.append(sensors)

# # Removing all edges
# TOPOLOGY.remove_edges_from(list(TOPOLOGY.edges))

# print(f'Triangles: {len(triangles)}')
# for triangle in triangles:
#     print([sensor[1]['coordinates'] for sensor in triangle])

#     if sensor_is_inside_triangle(triangle=triangle, logical_sensor=logical_sensor):
#         print(f'    Sensor {logical_sensor[1]["coordinates"]} is inside this triangle')




draw_network_topology()
