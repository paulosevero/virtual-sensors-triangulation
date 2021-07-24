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
    c = coordinates_a[0]*coordinates_b[1] - coordinates_b[0]*coordinates_a[1]

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


def triangle_area(x1, y1, x2, y2, x3, y3):
    """ Calculates the area of a triangle.

    Parameters
    ==========
    x1 : float
        X coordinates of first point of the triangle

    y1 : float
        Y coordinates of first point of the triangle

    x2 : float
        X coordinates of second point of the triangle

    y2 : float
        Y coordinates of second point of the triangle

    x3 : float
        X coordinates of third point of the triangle

    y3 : float
        Y coordinates of third point of the triangle

    Returns
    =======
    area : float
        Area of the triangle
    """

    area = abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
    return(area)
