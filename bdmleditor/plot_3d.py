import matplotlib.pyplot as plt
import numpy as np
import h5py
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider


class Plot_3D:

    def __init__(self, data, hdfpath, object_id):
        self.data = data
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.fig, self.ax, self.points = "", "", ""
        self.x_data, self.y_data, self.z_data = [], [], []

    def run(self):
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        self.x_data = np.append(self.x_data, self.data['x'].astype(np.float))
        self.y_data = np.append(self.y_data, self.data['y'].astype(np.float))
        self.z_data = np.append(self.z_data, self.data['z'].astype(np.float))

        slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03])
        self.points = self.ax.scatter3D(self.x_data, self.y_data, self.z_data, picker=10)
        self.fig.canvas.mpl_connect('pick_event', self.onclick)
        threshold_slider = Slider(slider_pos, 'time', 0, 100, valinit=0, valstep=1, dragging=True)
        threshold_slider.on_changed(self.update)
        plt.show()

    def onclick(self, event):
        f = h5py.File(self.hdfpath, 'r+')
        swap_data = f[self.object_id[0]].value
        ind = event.ind[0]
        print('x: {0}'.format(self.x_data[ind]),
              'y: {0}'.format(self.y_data[ind]),
              'z: {0}'.format(self.z_data[ind]))

        try:
            update_value_x, \
                update_value_y, \
                update_value_z = map(int, input('Enter value: ').split())
        except ValueError:
            print('Error')
            return
        self.points.remove()
        swap_data[ind][4] = update_value_x
        swap_data[ind][5] = update_value_y
        swap_data[ind][6] = update_value_z

        del f[self.object_id[0]]
        f.create_dataset(self.object_id[0], data=swap_data)
        data = f[self.object_id[0]]
        self.points = self.ax.scatter3D(data['x'].astype(np.float), data['y'].astype(np.float), data['z'].astype(np.float), picker=10)
        self.fig.canvas.draw()

    def update(self, slider_val):
        from bdmleditor.bootstrap import data_load
        self.object_id[0] = 'data/%s/object/0' %slider_val
        # init
        self.x_data, self.y_data, self.z_data = [], [], []
        info = data_load(self.hdfpath, self.object_id)
        for data in info[0][0]:
            self.x_data = np.append(self.x_data, data['x'].astype(np.float))
            self.y_data = np.append(self.y_data, data['y'].astype(np.float))
            self.z_data = np.append(self.z_data, data['z'].astype(np.float))
        self.points.remove()
        self.points = self.ax.scatter(self.x_data, self.y_data, self.z_data,  s=1, picker=10)
        self.fig.canvas.draw()
