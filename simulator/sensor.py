import scipy.interpolate

from simulator.misc.object_collection import ObjectCollection


class Sensor(ObjectCollection):

    # Class attribute that allows the class to use ObjectCollection methods
    instances = []

    def __init__(self, coordinates, type='physical', timestamp=None, measurement=None, metric='', alias=''):
        """ Creates a new sensor.

        Parameters
        ==========
        coordinates : tuple
            Sensor coordinates

        type : string (optional)
            Sensor type ('physical' or 'logical')

        timestamp : datetime (optional)
            Timestamp for the sensor measurement

        measurement : float (optional)
            Sensor measurement

        metric : string (optional)
            Metric collected by the sensor

        alias : string (optional)
            Name that identifies the sensor
        """

        # Defining sensor attributes
        self.id = Sensor.count() + 1
        self.type = type
        self.coordinates = coordinates
        self.timestamp = timestamp
        self.measurement = measurement
        self.metric = metric
        self.alias = alias

        self.topology = None

        # Adding the new object to the list of instances of its class
        Sensor.instances.append(self)


    def __str__(self):
        """ Dictates the visual representation of sensors when they're printed.
        """

        return(f'Sensor_{self.id}. Type: {self.type}. Alias: {self.alias}. ' +
               f'Coordinates: {self.coordinates}. Value: {self.measurement}')


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


    def interpolate_measurement(self, sensor1, sensor2):
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
