from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from tkinter import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import cv2
from PIL import Image, ImageTk

class pltMap:
    def __init__(self, minX, minY, maxX, maxY):
        """
        This class show the map of Brest port
        """
        self.m = Basemap(llcrnrlon=minX, llcrnrlat=minY, urcrnrlon=maxX, urcrnrlat=maxY,
                         resolution='h', projection='cass', lon_0=-2.107, lat_0=47.83)

    def plot_gap_points_with_traj(self, points, gap_points, size=2):  # LAT verticale [1] #LONG orizzontale [0]
        """
        This function creates an image with map of Brest port and the trajectory of the vessel with any events of Gap.
        """
        fig = plt.figure()
        axs = plt.subplot(111)
        self.m.drawcoastlines()
        self.m.fillcontinents(color='green', lake_color='coral')
        self.m.drawmapboundary(fill_color='coral')
        plt.title("Map")

        lon = []
        lat = []
        x, y = self.m(-4.49,48.38)
        axs.plot(x,y, color='cyan', markersize=7, marker='o',label='Brest')

        end_point = None
        for i,point in enumerate(points):

            x, y = self.m(point[0], point[1])
            lon.append(x)
            lat.append(y)
            if i!=len(points)-1:
                if point in gap_points:
                    axs.plot(x, y, color='blue', markersize=size, marker='o')
                else:
                    axs.plot(x, y, color='yellow', markersize=size, marker='o')
            elif i==len(points)-1:
                end_point = point
                axs.plot(x, y, color='purple', markersize=7, marker='o', label="End point")

        pts = np.c_[lon[:-1], lat[:-1], lon[1:], lat[1:]].reshape(len(lon) - 1, 2, 2)
        plt.gca().add_collection(LineCollection(pts, color='yellow', label="Tajectory Lines"))

        lon1 = []
        lat1 = []
        lon2 = []
        lat2 = []
        if len(gap_points)!= 0:
            for i, point in enumerate(gap_points):
                if point!=end_point:
                    x, y = self.m(point[0], point[1])
                    if i % 2:
                        lon1.append(x)
                        lat1.append(y)

                    else:
                        lon2.append(x)
                        lat2.append(y)


            pts = np.c_[lon1[:], lat1[:], lon2[:], lat2[:]].reshape(len(lon1), 2, 2)
            plt.gca().add_collection(LineCollection(pts, color='blue', label="Gap Lines"))

        plt.legend()

        #plt.show()

        canvas = FigureCanvas(fig)
        canvas.draw()
        img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # img is rgb, convert to opencv's default bgr
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        img = img[30:430, 120:-100]
        # display image with opencv or any operation you like
        #cv2.imshow("plot", img)
        #cv2.waitKey(0)

        return img
