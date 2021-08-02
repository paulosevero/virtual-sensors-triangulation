# Python Libraries
import math
from scipy.spatial import distance
from sklearn.metrics import mean_squared_error


def line(coordinates_a, coordinates_b):
    """ Creates a line between two given coordinates.

    Parameters
    ==========
    coordinates_a : tuple
        Coordinates that represent the beginning of the line
    coordinates_b : tuple
        Coordinates that represent the end of the line

    Returns
    =======
    Line specs
    """

    a = coordinates_a[1] - coordinates_b[1]
    b = coordinates_b[0] - coordinates_a[0]
    c = coordinates_a[0] * coordinates_b[1] - coordinates_b[0] * coordinates_a[1]

    return(a, b, -c)


def intersection(line1, line2):
    """ Finds the intersection between two lines.

    Parameters
    ==========
    line1 : tuple
        Line in the plane
    line2 : tuple
        Line in the plane

    Returns
    =======
    coordinates tuple or False
        Intersection coordinates or False in case the two lines do not cross each other
    """

    d = line1[0] * line2[1] - line1[1] * line2[0]
    dx = line1[2] * line2[1] - line1[1] * line2[2]
    dy = line1[0] * line2[2] - line1[2] * line2[0]

    if d != 0:
        x = dx / d
        y = dy / d
        return(x, y)
    else:
        return(False)


def triangle_area(triangle):
    """ Calculates the area of a triangle.

    Parameters
    ==========
    triangle : list
        List of sensors that form a triangle

    Returns
    =======
    area : float
        Area of the triangle
    """

    x1 = triangle[0].coordinates[0]
    y1 = triangle[0].coordinates[1]
    x2 = triangle[1].coordinates[0]
    y2 = triangle[1].coordinates[1]
    x3 = triangle[2].coordinates[0]
    y3 = triangle[2].coordinates[1]

    area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
    return(area)


def matrix_determinant(coord1, coord2, coord3):
    """ Calculates the determinant of a matrix.

    Parameters
    ==========
    coord1 : tuple
        First set of coordinates the form a matrix whose determinant will be calculated
    coord2 : tuple
        Second set of coordinates the form a matrix whose determinant will be calculated
    coord3 : tuple
        Third set of coordinates the form a matrix whose determinant will be calculated

    Returns
    =======
    determinant : float
        Determinant of the matrix formed by coord1, coord2, and coord3
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


def triangle_angles(triangle):
    """ Calculates the angles of a given triangle.

    Parameters
    ==========
    triangle : list
        List of sensors that form a triangle

    Returns
    =======
    angles : list
        List of angles of 'triangle'
    """

    A = triangle[0].coordinates
    B = triangle[1].coordinates
    C = triangle[2].coordinates

    # Square of lengths (a2, b2, c2)
    def length_square(X, Y):
        xDiff = X[0] - Y[0] 
        yDiff = X[1] - Y[1] 
        return(xDiff ** 2 + yDiff ** 2)

    a2 = length_square(B, C) 
    b2 = length_square(A, C) 
    c2 = length_square(A, B) 
  
    # length of sides be a, b, c 
    a = math.sqrt(a2)
    b = math.sqrt(b2)
    c = math.sqrt(c2)
  
    # From Cosine law 
    alpha = math.acos((b2 + c2 - a2) / (2 * b * c))
    beta = math.acos((a2 + c2 - b2) / (2 * a * c))
    gamma = math.acos((a2 + b2 - c2) / (2 * a * b))
  
    # Converting to degree 
    alpha = alpha * 180 / math.pi
    beta = beta * 180 / math.pi
    gamma = gamma * 180 / math.pi

    angles = [alpha, beta, gamma]
    return(angles)


def triangle_weight(virtual_sensor, triangle):
    """ Cost function that helps the proposed heuristic to choose the best triangle
    to estimate the value of a virtual sensor. The cost (i.e., weight) of a triangle
    is given by the average distance of its sensors to the virtual sensor.

    Parameters
    ==========
    virtual_sensor : Sensor
        Virtual sensor whose measurement will be inferred

    triangle : list
        List of sensors that form a triangle

    Returns
    =======
    weight : float
        Weight (or cost) of 'triangle' that denotes how suitable it is to estimate the value of 'virtual_sensor'
    """


    auxiliary_sensors = virtual_sensor.create_auxiliary_sensors(physical_sensors=triangle)

    dist_auxsensor1_logical_sensor = distance.euclidean(virtual_sensor.coordinates, auxiliary_sensors[0].coordinates)
    dist_auxsensor2_logical_sensor = distance.euclidean(virtual_sensor.coordinates, auxiliary_sensors[1].coordinates)
    dist_auxsensor3_logical_sensor = distance.euclidean(virtual_sensor.coordinates, auxiliary_sensors[2].coordinates)

    weight = (dist_auxsensor1_logical_sensor + dist_auxsensor2_logical_sensor + dist_auxsensor3_logical_sensor) / 3

    return(weight)


def is_well_conditioned_triangle(triangle):
    """ Checks if a group of physical sensors form a well-conditioned triangle.

    Parameters
    ==========
    triangle : list
        List of physical sensors that form a triangle

    Returns
    =======
    True or False : boolean
        Response that informs if whether the physical sensors form a well-conditioned triangle or not
    """

    angles = triangle_angles(triangle)
    return(min(angles) >= 30 and max(angles) <= 120)


def show_triangle_info(virtual_sensor, triangle):
    """ Prints out the details of a given triangle.

    Parameters
    ==========
    virtual_sensor : Sensor
        Virtual sensor whose measurement will be inferred

    triangle : list
        List of sensors that form a triangle
    """

    # Auxiliary sensors within the triangle
    auxiliary_sensors = virtual_sensor.create_auxiliary_sensors(physical_sensors=triangle)
    dist_auxsensor1_logical_sensor = round(distance.euclidean(virtual_sensor.coordinates, auxiliary_sensors[0].coordinates), 4)
    dist_auxsensor2_logical_sensor = round(distance.euclidean(virtual_sensor.coordinates, auxiliary_sensors[1].coordinates), 4)
    dist_auxsensor3_logical_sensor = round(distance.euclidean(virtual_sensor.coordinates, auxiliary_sensors[2].coordinates), 4)

    # General properties of the triangle
    area = triangle_area(triangle)
    distance_from_virtual_sensor = round(triangle_weight(virtual_sensor=virtual_sensor, triangle=triangle), 4)

    # Triangle inference
    inference = round(virtual_sensor.calculate_measurement(physical_sensors=triangle), 1)
    mse = round(mean_squared_error([virtual_sensor.measurement], [inference]), 2)

    print(f'        Triangle = {sorted([sensor.id for sensor in triangle], key=lambda i: i)}')
    print(f'            Aux. Sensor 1: {auxiliary_sensors[0].inferred_measurement} (dist={dist_auxsensor1_logical_sensor})')
    print(f'            Aux. Sensor 2: {auxiliary_sensors[1].inferred_measurement} (dist={dist_auxsensor2_logical_sensor})')
    print(f'            Aux. Sensor 3: {auxiliary_sensors[2].inferred_measurement} (dist={dist_auxsensor3_logical_sensor})')
    print(f'            Average Distance from Virtual Sensor: {distance_from_virtual_sensor}')
    print(f'            Triangle Area: {area}')
    print(f'            Inference: {inference} (MSE={mse})')


def create_edges_and_draw_topo(triangles, figname='topology.jpg'):
    """ Creates the edges of all triangle in 'triangles' and output the NetworkX topology to a figure.

    Parameters
    ==========
    triangles : list
        List of triangles formed by physical sensors

    figname : string (optional)
        Name of the output image
    """

    topology = triangles[0][0].topology

    # Removing any links used to triangulate measurements of a logical sensor
    topology.remove_edges_from(list(topology.edges()))

    # Adding the edges that form the triangles
    for triangle in triangles:
        topology.add_edge(triangle[2], triangle[0])
        for i in range(0, 2):
            topology.add_edge(triangle[i], triangle[i + 1])

    # Outputing useful information
    topology.draw(showgui=False, savefig=True, dpi=170, figname=figname)
