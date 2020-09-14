import matplotlib.pyplot as plt
import numpy as np
import h5py


class Plot_3D:

    def __init__(self, data, hdfpath, object_id):
        self.data = data
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.fig, self.ax, self.points = "", "", ""
        self.x_data, self.y_data, self.z_data = [], [], []

    def run(self):
        self.fig = plt.figure()
        self.ax = self.Axes3D(self.fig)
        for data in self.data:
            self.x_data = np.append(self.x_data, data[4])
            self.y_data = np.append(self.y_data, data[5])
            self.z_data = np.append(self.z_data, data[6])

        self.points = self.ax.scatter3D(self.x_data, self.y_data, self.z_data)
        self.fig.canvas.mpl_connect('pick_event', self.onclick)
        self.plt.draw()

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

        swap_data[ind][4] = update_value_x
        swap_data[ind][5] = update_value_y
        swap_data[ind][6] = update_value_z

        del f[self.object_id[0]]
        f.cleate_dataset(self.object_id[0], data=swap_data)
        data = f[self.object_id[0]]
        self.points = self.ax.scatter(data['x'], data['y'], data['z'], picker=10)
        self.fig.canvas.draw()
