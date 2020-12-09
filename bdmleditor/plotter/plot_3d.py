import matplotlib.pyplot as plt
import numpy as np
import h5py
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Slider


class Plot_3D:
    name = 1

    graph_2d_data_x = None
    graph_2d_data_y = None

    def __init__(self, data, hdfpath, object_id):
        self.data = data
        self.hdfpath = hdfpath
        self.object_id = object_id
        self.fig, self.ax, self.points = "", "", ""
        self.x_data, self.y_data, self.z_data = np.array([]), np.array([]), np.array([])
        self.editmode_flag = False
        self.update_value_x, self.update_value_y, self.update_value_z = None, None, None
        self.z_axis_number = None
        self.graph_2d_data_x, self.graph_2d_data_y  = np.array([]), np.array([])

    def run(self):
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        self.x_data = np.append(self.x_data, self.data['x'].astype(np.float))
        self.y_data = np.append(self.y_data, self.data['y'].astype(np.float))
        self.z_data = np.append(self.z_data, self.data['z'].astype(np.float))

        # slider intialize
        slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03])
        threshold_slider = Slider(slider_pos, 'time', 0, 100, valinit=0, valstep=1, dragging=True)
        threshold_slider.on_changed(self.update_time)

        self.points = self.ax.scatter(self.x_data, self.y_data, self.z_data, s=1, picker=10)
        # matplotlib backend's connect
        self.fig.canvas.mpl_connect('button_press_event', self.on_pressed)
        plt.show()

    def on_motion(self, event):
        if self.editmode_flag is not True:
            return
        print(event.xdata)
        if event.button:
            print("clicked!")
            self.update_value_x = event.xdata
            self.update_value_y = event.ydata
            self.editmode_flag = False
            self.update_graph_data()
            self.update_graph_drawing()
            return

    def on_pressed(self, event):
        if self.editmode_flag:
            return
        try:
            self.z_axis_number = int(input("enter z axis's value:"))
        except ValueError:
            print("please enter a value")
            return

        self.draw_2d_graph()

    def on_picked(self, event):
        print("ここ通ってる？")
#         if event.artist != self.points:
#             return
#         print(event.ind)
        print(self.graph_2d_data_x[event.ind[0]])
        self.before_x_value = self.graph_2d_data_x[event.ind[0]]
        self.before_y_value = self.graph_2d_data_y[event.ind[0]]
        self.fig_editmode.canvas.mpl_connect("motion_notify_event", self.on_motion)
        return

    def draw_2d_graph(self):
        print("Enter edit mode")
        self.fig_editmode, self.ax_editmode = plt.subplots(figsize=(6, 4))
        from bdmleditor.bootstrap import data_load
        info = data_load(self.hdfpath, ''.join(self.object_id))
        for data in info[0][0]:
            if data['z'].astype(np.float) == self.z_axis_number:
                self.graph_2d_data_x = np.append(self.graph_2d_data_x, data['x'].astype(np.float))
                self.graph_2d_data_y = np.append(self.graph_2d_data_y, data['y'].astype(np.float))

        self.ax_editmode.set_xlabel("x")
        self.ax_editmode.set_ylabel("y")
        self.points_editmode = self.ax_editmode.scatter(self.graph_2d_data_x,
                                                        self.graph_2d_data_y,
                                                        s=1, picker=10)

        self.fig_editmode.canvas.mpl_connect("pick_event", self.on_picked)
        self.editmode_flag = True
        plt.show()

    def update_graph_data(self):
        if self.update_value_x is None and self.update_value_y is None and \
                self.update_value_z is None:
            return
        f = h5py.File(self.hdfpath, 'r+')
        swap_datas = f[''.join(self.object_id)][()]
        for swap_data in swap_datas:
            if swap_data['z'].astype(np.float) == float(self.z_axis_number):
                if swap_data['x'].astype(np.float) == self.before_x_value and \
                        swap_data['y'].astype(np.float) == self.before_y_value:
                    print(swap_data['x'])
                    swap_data['x'] = self.update_value_x
                    swap_data['y'] = self.update_value_y
                    print(swap_data['x'])

        del f[''.join(self.object_id)]
        f.create_dataset(''.join(self.object_id), data=swap_datas)
        f.close()

    def update_graph_drawing(self):
        self.points.remove()
        f = h5py.File(self.hdfpath, 'r')
        data = f[''.join(self.object_id)]
        self.points = self.ax.scatter3D(data['x'].astype(np.float),
                                        data['y'].astype(np.float),
                                        data['z'].astype(np.float),
                                        s=1, picker=10)
        self.x_data, self.y_data = data["x"], data["y"]
        # 型が違う
        self.fig.canvas.draw()
        self.update_value_x, self.update_value_y = None, None
        self.ind = None

    def update_time(self, slider_val):
        from bdmleditor.bootstrap import data_load
        print(self.object_id)
        self.object_id[1] = str(slider_val)
        # init
        self.x_data, self.y_data, self.z_data = [], [], []
        info = data_load(self.hdfpath, ''.join(self.object_id))
        for data in info[0][0]:
            self.x_data = np.append(self.x_data, data['x'].astype(np.float))
            self.y_data = np.append(self.y_data, data['y'].astype(np.float))
            self.z_data = np.append(self.z_data, data['z'].astype(np.float))
        self.points.remove()
        self.points = self.ax.scatter(self.x_data, self.y_data, self.z_data,  s=1, picker=10)
        self.fig.canvas.draw()
