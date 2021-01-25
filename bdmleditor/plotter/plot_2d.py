import numpy as np
import matplotlib.pyplot as plt
import h5py
from matplotlib.widgets import Slider
import time


class Plot_2D:

    def __init__(self, data, hdfpath, object_id, load_time):
        self.data = data
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.fig, self.ax, self.points = "", "", ""
        self.x_data, self.y_data = np.array([]), np.array([])
        # flag event's value
        self.is_picking_object = False
        self.update_value_x, self.update_value_y = None, None
        self.ind = None
        self.load_time = load_time

    def run(self):
        start = time.time()
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.x_data = np.append(self.x_data, self.data['x'])
        self.y_data = np.append(self.y_data, self.data['y'])

        slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03])
        self.points = self.ax.scatter(self.x_data, self.y_data, s=1, picker=10)
        self.fig.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.fig.canvas.mpl_connect('pick_event', self.on_picked)
        threshold_slider = Slider(slider_pos, 'time', 0, 100, valinit=0, valstep=1, dragging=True)
        threshold_slider.on_changed(self.update_time)
        elapsed_time = time.time() - start + self.load_time
        print("\nelapsed_time:{0}".format(elapsed_time) + "[sec]")
        plt.show(block=False)

    def on_motion(self, event):
        if self.is_picking_object is not True:
            return
        print('x: {0}'.format(event.xdata),
              'y: {0}'.format(event.ydata))
        # こいつが動いたり動かなかったりする。困りましたねお客様
        if event.button:
            print("clicked!")
            # 参照渡し
            self.update_value_x, self.update_value_y = event.xdata, event.ydata
            # フラグを入れ替える
            self.is_picking_object = False
            self.update_graph_data()
            self.update_graph_drawing()
            return

    def on_picked(self, event):
        if event.artist != self.points:
            return
        self.is_picking_object = True
        self.ind = event.ind[0]

    def update_graph_data(self):
        if self.update_value_x is None or self.update_value_y is None:
            return
        f = h5py.File(self.hdfpath, 'r+')
        swap_data = f[''.join(self.object_id)][()]
        swap_data[self.ind]['x'] = self.update_value_x
        swap_data[self.ind]['y'] = self.update_value_y
        del f[''.join(self.object_id)]
        f.create_dataset(''.join(self.object_id), data=swap_data)
        f.close()

    def update_graph_drawing(self):
        self.points.remove()
        f = h5py.File(self.hdfpath, 'r')
        data = f[''.join(self.object_id)]
        self.points = self.ax.scatter(data['x'], data['y'], s=1, picker=10)
        self.x_data, self.y_data = data['x'], data['y']
        self.fig.canvas.draw()
        self.update_value_x, self.update_value_y = None, None
        self.ind = None

    def update_time(self, slider_val):
        from bdmleditor.bootstrap import data_load
        print(self.object_id)
        # object id is ['data/', str(data_time), '/object/', str(object_def)]
        self.object_id[1] = str(slider_val)
        self.x_data, self.y_data = [], []
        info = data_load(self.hdfpath, ''.join(self.object_id))
        for data in info[0][0]:
            self.x_data = np.append(self.x_data, data['x'])
            self.y_data = np.append(self.y_data, data['y'])
        self.points.remove()
        self.points = self.ax.scatter(self.x_data, self.y_data, s=1, picker=10)
        self.fig.canvas.draw()
