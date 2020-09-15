import numpy as np
import matplotlib.pyplot as plt
import h5py


class Plot_2D:

    def __init__(self, data, hdfpath, object_id):
        self.data = data
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.fig, self.ax, self.points = "", "", ""
        self.x_data, self.y_data = [[] * 0 for i in range(len(self.data))],\
                                   [[] * 0 for i in range(len(self.data))],

    def run(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))

        for i in range(len(self.data)):
            for data in self.data[i]:
                self.x_data[i] = np.append(self.x_data[i], data['x'])
                self.y_data[i] = np.append(self.y_data[i], data['y'])

        for i in range(len(self.data)):
            self.points = self.ax.scatter(self.x_data[i], self.y_data[i], s=1, picker=10)

        self.fig.canvas.mpl_connect('pick_event', self.onclick)
        plt.show()

    def onclick(self, event):
        f = h5py.File(self.hdfpath, 'r+')
        swap_data = f[self.object_id[0]].value
        ind = event.ind[0]
        # バグ: 値が更新されない（グラフ上は更新される）
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
        self.fig.canvas.draw()
