import numpy as np
import h5py
import matplotlib.pyplot as plt


class Figure:
    def __init__(self, hdfpath, object_id, data_number):
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.data_number = data_number
        self.points = ""
        self.x_data, self.y_data = [], []
        self.fig = ""
        self.ax = ""

    def run(self):
        self.fig, self.ax = plt.subplots(figsize=(6, 4))

        for data in self.data_load():
            self.x_data = np.append(self.x_data, data[4])
            self.y_data = np.append(self.y_data, data[5])

        self.points = self.ax.scatter(self.x_data, self.y_data, s=1, picker=10)
        self.fig.canvas.mpl_connect('pick_event', self.onclick)
        plt.show()

    def onclick(self, event):
        f = h5py.File(self.hdfpath, 'r+')
        swap_data = f[self.object_id[0]].value
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
        self.fig.canvas.draw()

    def data_load(self):
        with h5py.File(self.hdfpath, 'r') as f:
            data = []
            data.append(f[self.object_id[0]].value)
            f.close()
        return data[0]


if __name__ == '__main__':
    data_time = int(input('Enter time:'))
    figure = Figure('../data/sample2.h5',
                    ['data/' + str(data_time) + '/object/0'],
                    data_time)
    figure.run()
