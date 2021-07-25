# Python Libraries
import scipy.interpolate
from scipy.spatial import distance
from scipy.spatial import Delaunay
import itertools

# General-purpose Simulator Modules
from simulator.misc.object_collection import ObjectCollection

# Simulator Components
from simulator.components.topology import Topology

# Helper Methods
from simulator.misc.helper_methods import matrix_determinant
from simulator.misc.helper_methods import triangle_area
from simulator.misc.helper_methods import line
from simulator.misc.helper_methods import intersection


class Sensor(ObjectCollection):

    # Class attribute that allows the class to use ObjectCollection methods
    instances = []

    def __init__(self, coordinates=None, type='physical', timestamps=[], measurements=[], alias=''):
        """ Creates a new sensor.

        Parameters
        ==========
        coordinates : tuple
            Sensor coordinates

        type : string (optional)
            Sensor type ('physical' or 'logical')

        timestamp : datetime (optional)
            Timestamp for the sensor measurement

        measurements : float (optional)
            Sensor measurements

        alias : string (optional)
            Name that identifies the sensor
        """

        # Defining sensor attributes
        self.id = Sensor.count() + 1

        # Helper attribute that differs physical sensors from the virtual and auxiliary ones
        self.type = type

        # Basic sensor attributes
        self.alias = alias
        self.coordinates = coordinates
        self.measurements = measurements
        self.timestamps = timestamps

        # Sensor measurement at the current timestamp
        self.measurement = measurements[0] if len(measurements) > 0 else None
        self.timestamp = timestamps[0] if len(timestamps) > 0 else None

        # Inferred measurement
        self.inferred_measurement = None

        # NetworkX topology
        self.topology = None

        # Adding the new object to the list of instances of its class
        Sensor.instances.append(self)


    def __str__(self):
        """ Dictates the visual representation of sensors when they're printed.
        """

        return(f'Sensor_{self.id}. Type: {self.type}. Alias: {self.alias}. ' +
               f'Coordinates: {self.coordinates}. Value: {self.measurements}')


    @classmethod
    def create_delaunay_triangles(cls, physical_sensors):
        """ Creates a mesh of triangles using the delaunay algorithm.

        Parameters
        ==========
        physical_sensors : list
            Group of physical sensors that will form a mesh of triangles

        Returns
        ======
        triangles : list
            List of coordinates from sensors from 'physical_sensors' that comprise a mesh of triangles
        """

        topo = Topology.first()

        sensors = [sensor.coordinates for sensor in physical_sensors]
        triangles = [[Sensor.find_by(attribute_name='coordinates', attribute_value=sensors[i])[0] for i in list(triangle)]
                     for triangle in Delaunay(sensors).simplices]

        for triangle in triangles:
            topo.add_edge(triangle[2], triangle[0])
            for i in range(0, 2):
                topo.add_edge(triangle[i], triangle[i+1])

        return(triangles)


    def covered_by_triangles_mesh(self, sensors):
        """
        """

        if len(sensors) > 2:
            triangles = Sensor.create_delaunay_triangles(sensors)

            for triangle in triangles:
                if self.is_inside_triangle(triangle=triangle):
                    print(f'Sensor_{self.id} is inside triangle {[sensor.id for sensor in triangle]}')
                    return(True)
                else:
                    print(f'Sensor_{self.id} is NOT inside triangle {[sensor.id for sensor in triangle]}')

        return(False)


    def find_neighbors_sorted_by_distance(self):
        """ Finds all neighbor sensors sorted by their distance.

        Returns
        =======
        neighbors : list
            List of sensors sorted by their distance from 'self'
        """
        sensors = [sensor for sensor in Sensor.all() if sensor != self and sensor.type == 'physical']
        neighbors = sorted(sensors, key=lambda s: distance.euclidean(self.coordinates, s.coordinates))

        return(neighbors)


    def get_encoded_position(self):
        """ Encodes sensor's coordinates into a single number [1].

        Returns
        =======
        pos : int
            Encoded sensor coordinates

        [1] https://stackoverflow.com/questions/4637031/geospatial-indexing-with-redis-sinatra-for-a-facebook-app
        """

        pos = (self.coordinates[0]+90)*180+self.coordinates[1]
        return(pos)


    def interpolate_measurement_aligned_sensors(self, sensor1, sensor2):
        """ Infers the measurement of a sensor based on
        the measurements of two other inlined sensors.

        Parameters
        ==========
        sensor1 : Sensor
            Sensor that forms a line with sensor2 and is used to infer the measurement
        sensor2 : Sensor
            Sensor that forms a line with sensor1 and is used to infer the measurement

        Returns
        =======
        inferred_measurement : float
            Inferred sensor measurement
        """
        positions = [sensor1.get_encoded_position(), sensor2.get_encoded_position()]
        measurements = [sensor1.measurement, sensor2.measurement]

        interpolation = scipy.interpolate.interp1d(positions, measurements)

        inferred_measurement = interpolation(self.get_encoded_position())
        return(inferred_measurement)


    def calculate_measurement(self, physical_sensors):
        """ Infers the value of a logical sensor by triangulating the
        value of existing physical sensors positioned across a given area.

        Parameters
        ==========
        physical_sensors : list
            List of physical sensors used to triangulate the logical sensor

        logical_sensor : Sensor
            Logical sensor whose measurement will be inferred

        Returns
        =======
        inferred_measurement : float
            Inferred measurement of the logical sensor
        """

        line_physensor1_physensor2 = line(physical_sensors[0].coordinates, physical_sensors[1].coordinates)
        line_physensor1_physensor3 = line(physical_sensors[0].coordinates, physical_sensors[2].coordinates)
        line_physensor2_physensor3 = line(physical_sensors[1].coordinates, physical_sensors[2].coordinates)

        line_with_physensor1 = line(physical_sensors[0].coordinates, self.coordinates)
        line_with_physensor2 = line(physical_sensors[1].coordinates, self.coordinates)
        line_with_physensor3 = line(physical_sensors[2].coordinates, self.coordinates)

        intersection_physensor1_physensor2 = intersection(line_physensor1_physensor2, line_with_physensor3)
        intersection_physensor1_physensor3 = intersection(line_physensor1_physensor3, line_with_physensor2)
        intersection_physensor2_physensor3 = intersection(line_physensor2_physensor3, line_with_physensor1)

        aux_sensor1 = Sensor(coordinates=intersection_physensor1_physensor2, type='auxiliary')
        aux_sensor2 = Sensor(coordinates=intersection_physensor1_physensor3, type='auxiliary')
        aux_sensor3 = Sensor(coordinates=intersection_physensor2_physensor3, type='auxiliary')

        # https://stackoverflow.com/questions/8285599/is-there-a-formula-to-change-a-latitude-and-longitude-into-a-single-number
        # https://stackoverflow.com/questions/4637031/geospatial-indexing-with-redis-sinatra-for-a-facebook-app
        value_aux_sensor1 = aux_sensor1.interpolate_measurement_aligned_sensors(sensor1=physical_sensors[0],
                                                                                sensor2=physical_sensors[1])
        value_aux_sensor2 = aux_sensor2.interpolate_measurement_aligned_sensors(sensor1=physical_sensors[0],
                                                                                sensor2=physical_sensors[2])
        value_aux_sensor3 = aux_sensor3.interpolate_measurement_aligned_sensors(sensor1=physical_sensors[1],
                                                                                sensor2=physical_sensors[2])

        inferred_measurement = (value_aux_sensor1 + value_aux_sensor2 + value_aux_sensor3) / 3

        return(inferred_measurement)


    def is_inside_line(self, sensor1, sensor2):
        """ Checks if sensor is inside a line.

        Parameters
        ==========
        sensor1 : Sensor
            First sensor that forms the line

        sensor2 : Sensor
            Second sensor that forms the line
        """

        encoded_position1 = sensor1.get_encoded_position()
        encoded_position2 = self.get_encoded_position()
        encoded_position3 = sensor2.get_encoded_position()

        return((encoded_position2 > encoded_position1 and encoded_position2 < encoded_position3) or
               (encoded_position2 < encoded_position1 and encoded_position2 > encoded_position3))


    def crossed_by_line(self, sensors):
        """ Checks if sensor is crossed by a line formed by two physical sensors.

        Parameters
        ==========
        sensors : list
            List of physical sensors

        Returns
        =======
        Tuple of sensors of 'False'
            Indication of whether a sensor is crossed by two physical sensors or not
        """

        combinations = itertools.combinations(sensors, 2)
        for pair in combinations:

            # Calculating the matrix determinant to check if the virtual sensor is aligned with two physical sensors
            determinant = matrix_determinant(coord1=pair[0].coordinates, coord2=self.coordinates, coord3=pair[1].coordinates)

            # Checking if the sensor is inside the line formed by the two physical sensors
            inside_line = self.is_inside_line(sensor1=pair[0], sensor2=pair[1])

            if determinant == 0 and inside_line:
                return(pair)

        return(False)


    def is_inside_triangle(self, triangle):
        """
        """

        sensor1 = triangle[0]
        sensor2 = triangle[1]
        sensor3 = triangle[2]

        # Calculate area of triangle ABC
        A = triangle_area(sensor1.coordinates[0], sensor1.coordinates[1],
                          sensor2.coordinates[0], sensor2.coordinates[1],
                          sensor3.coordinates[0], sensor3.coordinates[1])

        # Calculate area of triangle PBC
        A1 = triangle_area(self.coordinates[0], self.coordinates[1],
                           sensor2.coordinates[0], sensor2.coordinates[1],
                           sensor3.coordinates[0], sensor3.coordinates[1])
        # Calculate area of triangle PAC
        A2 = triangle_area(sensor1.coordinates[0], sensor1.coordinates[1],
                           self.coordinates[0], self.coordinates[1],
                           sensor3.coordinates[0], sensor3.coordinates[1])
        # Calculate area of triangle PAB
        A3 = triangle_area(sensor1.coordinates[0], sensor1.coordinates[1],
                           sensor2.coordinates[0], sensor2.coordinates[1],
                           self.coordinates[0], self.coordinates[1])

        # Calculating the minimum precision (number of decimal) of the sensors' coordinates. We use
        # the minimum precision instead of the maximum to avoid misleading calculations of whether
        # a point lies inside the triangle of not (in case the coordinates of a sensor has a higher precision
        # than the coordinates of other sensor that comprises the triangle).
        triangle_coordinates_precision = min([min([str(sensor.coordinates[0])[::-1].find('.'),
                                             str(sensor.coordinates[1])[::-1].find('.')]) for sensor in triangle])

        # Check if sum of A1, A2 and A3 is same as A. We are rounding both
        # float values to 'triangle_coordinates_precision' decimal places
        if(round(A, triangle_coordinates_precision) == round(A1 + A2 + A3, triangle_coordinates_precision)):
            return(True)
        else:
            return(False)


    def can_be_triangulated(self, sensors):
        """ Creates a mesh of triangles using the Delaunay algorithm and checks if triangle (self)
        is covered by any of thee created triangles in such a way its value could be triangulated.

        Parameters
        ==========
        sensors : list
            List of physical sensors

        Returns
        =======
        List or 'False'
            Indication of whether a sensor measurement could be triangulated base on a mesh of triangles or not
        """

        triangles_that_cover_the_sensor = []

        if len(sensors) >= 3:

            # Creates a mesh of triangles using the Delaunay algorithm
            triangles = Sensor.create_delaunay_triangles(physical_sensors=sensors)

            for triangle in triangles:
                if self.is_inside_triangle(triangle=triangle):
                    triangles_that_cover_the_sensor.append(triangle)

            if len(triangles_that_cover_the_sensor) > 0:
                return(triangles_that_cover_the_sensor)

        else:
            return(False)