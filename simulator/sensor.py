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
