from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt


class Simulator():
    def __init__(self, loader):
        self.map = loader

    def draw(self):
        '''
              Plot obstacles, waypoints, and boundary fearures onto a matplotlib grid.
        '''
        self.plot_obstacles()
        self.plot_way_points()
        self.plot_boundary()

    def simulate(self, algorithm, headless=False):
        '''
              Execute path planning algorithim in a headless or dynamic mode. 
        '''
        if headless:
            segments = algorithm.run()
            return segments
        else:
            plt.grid(True)
            segments = algorithm.run(self.dinamic_plot)
            self.plot_final_path(segments)
            return segments

    def dinamic_plot(self, x, y, color):
        '''
              Callback function used to plot coordinates while an algorithim is running.
        '''
        plt.plot(x, y, color)
        plt.pause(0.001)

    def plot_boundary(self):
        '''
              Plot map obstacles onto the grid.
        '''
        x_coords, y_coords = self.map.boundary()
        plt.plot(x_coords, y_coords)
        plt.grid(True)
        plt.axis("equal")

    def plot_way_points(self):
        '''
              Plot map waypoints onto the grid.
        '''
        x_coords, y_coords = self.map.way_points()
        plt.plot(x_coords, y_coords)
        plt.grid(True)
        plt.axis("equal")

    def plot_obstacles(self):
        '''
              Plot map obstacles onto the grid.
        '''
        x_coords, y_coords, radii = self.map.obstacles()
        _, ax = plt.subplots()
        for i in range(len(radii)):
            circle = plt.Circle((x_coords[i], y_coords[i]), radii[i])
            ax.set_aspect(1)
            ax.add_artist(circle)

    def plot_final_path(self, segments):
        '''
              Plot the final mission path using the created segments from an algorithim.
        '''
        for line in segments:
            for point in line:
                plt.plot(point[0], point[1], 'xc')
                plt.pause(0.001)
