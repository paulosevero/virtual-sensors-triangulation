import networkx as nx
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

from simulator.misc.object_collection import ObjectCollection


class Topology(ObjectCollection, nx.Graph):

    # Class attribute that allows the class to use ObjectCollection methods
    instances = []

    def __init__(self):
        """Creates a NetworkX topology"""

        nx.Graph.__init__(self)

        # Adding the new object to the list of instances of its class
        Topology.instances.append(self)

    def draw(self, showgui=True, savefig=True, figname="topology.jpg", dpi=200):
        """Draws the network topology."""

        fig = plt.figure()

        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        ax.add_feature(cfeature.STATES)

        pos = {}
        colors = []
        labels = {}
        for sensor in self.nodes():
            pos[sensor] = (sensor.coordinates[1], sensor.coordinates[0])
            labels[sensor] = sensor.id

            if sensor.type == "physical":
                colors.append("black")
            elif sensor.type == "virtual":
                colors.append("red")
            elif sensor.type == "auxiliary":
                colors.append("green")

        nx.draw(
            self,
            pos=pos,
            labels=labels,
            node_size=60,
            font_size=4,
            font_color="white",
            node_color=colors,
            font_weight="bold",
        )

        if savefig:
            fig.savefig(figname, dpi=dpi)

        if showgui:
            plt.show()
