import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.widgets import Slider
import os
from bdmleditor.load_yaml import load_yamlinfo


class Plot_2D:

    def __init__(self, data, hdfpath, object_id):
        self.data = data
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.fig, self.ax, self.points = "", "", ""
        self.x_data, self.y_data = [], []

    def run(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        for data in self.data:
            self.x_data = np.append(self.x_data, data[4])
            self.y_data = np.append(self.y_data, data[5])

        slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03])
        self.points = self.ax.scatter(self.x_data, self.y_data, s=1, picker=10)
        self.fig.canvas.mpl_connect('pick_event', self.onclick)
        slider_maxmin_values = load_yamlinfo(os.path.expanduser("~/.bdmleditorrc.yml"))
        threshold_slider = Slider(slider_pos, 'time',
                                  slider_maxmin_values['minimum'],
                                  slider_maxmin_values['maximum'],
                                  valinit=0, valstep=1, dragging=True)
        threshold_slider.on_changed(self.update)
        plt.show()

    def onclick(self, event):
        f = h5py.File(self.hdfpath, 'r+')
        swap_data = f[self.object_id[0]][()]
        ind = event.ind[0]

        print('x: {0}'.format(self.x_data[ind]),
              'y: {0}'.format(self.y_data[ind]),)
        try:
            update_value_x, update_value_y = map(float, input('Enter value: ').split())
        except ValueError:
            print('Error')
            return

        swap_data[ind][4] = update_value_x
        swap_data[ind][5] = update_value_y
        del f[self.object_id[0]]
        f.create_dataset(self.object_id[0], data=swap_data)
        f.close()
        self.points.remove()
        f = h5py.File(self.hdfpath, 'r')
        data = f[self.object_id[0]]
        self.points = self.ax.scatter(data['x'], data['y'], s=1, picker=10, color="red")
        self.x_data, self.y_data = data['x'], data['y']
        self.fig.canvas.draw()

    def update(self, slider_val):
        from bdmleditor.bootstrap import data_load
        self.object_id[0] = 'data/%s/object/0' %slider_val
        # init
        self.x_data, self.y_data = [], []
        info = data_load(self.hdfpath, self.object_id)
        for data in info[0][0]:
            self.x_data = np.append(self.x_data, data['x'])
            self.y_data = np.append(self.y_data, data['y'])
        # # cast
        self.points.remove()
        self.points = self.ax.scatter(self.x_data, self.y_data, s=1, picker=10)
        self.fig.canvas.draw()
