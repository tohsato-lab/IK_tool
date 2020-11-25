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
        self.x_data, self.y_data, self.z_data = np.array([]), np.array([]), np.array([])
        self.editmode_flag = False
        self.update_value_x, self.update_value_y, self.update_value_z = None, None, None
        self.graph_axis_list = ""

    def run(self):
        self.fig = plt.figure()
        self.ax = Axes3D(self.fig)

        self.x_data = np.append(self.x_data, self.data['x'].astype(np.float))
        self.y_data = np.append(self.y_data, self.data['y'].astype(np.float))
        self.z_data = np.append(self.z_data, self.data['z'].astype(np.float))

        slider_pos = plt.axes([0.1, 0.01, 0.8, 0.03])
        self.points = self.ax.scatter(self.x_data, self.y_data, self.z_data, s=1, picker=10)
        self.fig.canvas.mpl_connect('pick_event', self.on_picked)
        threshold_slider = Slider(slider_pos, 'time', 0, 100, valinit=0, valstep=1, dragging=True)
        threshold_slider.on_changed(self.update_time)
        plt.show()

    def on_motion(self, event):
        if self.editmode_flag is not True:
            return
        print(event.xdata)
        if event.button:
            print("clicked!")
            # 値の参照渡し、この方法はうまくいくのか怪しい（ハードコーディング）
            exec("self.update_value_%s = %s" % (self.graph_axis_list[0], "event.xdata"))
            exec("self.update_value_%s = %s" % (self.graph_axis_list[1], "event.ydata"))
            self.editmode_flag = False
            self.update_graph_data()
            self.update_graph_drawing()
            return

    def on_picked(self, event):
        if event.artist != self.points:
            return
        # ここで軸を入力させる（x, yみたいな感じで）
        self.graph_axis_list = list(map(str, input('Enter value: ').split()))
        self.ind = event.ind[0]
        self.draw_2d_graph()
# f = h5py.File(self.hdfpath, 'r+')
#         swap_data = f[''.join(self.object_id)][()]
#         ind = event.ind[0]
#         print('x: {0}'.format(self.x_data[ind]),
#               'y: {0}'.format(self.y_data[ind]),
#               'z: {0}'.format(self.z_data[ind]))
#
#         try:
#             update_value_x, \
#                 update_value_y, \
#                 update_value_z = map(int, input('Enter value: ').split())
#         except ValueError:
#             print('Error')
#             return
#         self.points.remove()
#         swap_data[ind][4] = update_value_x
#         swap_data[ind][5] = update_value_y
#         swap_data[ind][6] = update_value_z
#
#         del f[''.join(self.object_id)]
#         f.create_dataset(''.join(self.object_id), data=swap_data)
#         data = f[''.join(self.object_id)]
#         self.points = self.ax.scatter3D(data['x'].astype(np.float),
#                                         data['y'].astype(np.float),
#                                         data['z'].astype(np.float), picker=10)
#         self.fig.canvas.draw()

    def draw_2d_graph(self):
        print("Enter edit mode")
        self.fig_editmode, self.ax_editmode = plt.subplots(figsize=(6, 4))
        from bdmleditor.bootstrap import data_load
        info = data_load(self.hdfpath, ''.join(self.object_id))
        data_1, data_2 = np.array([]), np.array([])
        for data in info[0][0]:
            data_1 = np.append(data_1, data[self.graph_axis_list[0]].astype(np.float))
            data_2 = np.append(data_2, data[self.graph_axis_list[1]].astype(np.float))
        self.ax_editmode.set_xlabel(self.graph_axis_list[0])
        self.ax_editmode.set_ylabel(self.graph_axis_list[1])
        self.points_editmode = self.ax_editmode.scatter(data_1, data_2, s=1, picker=10)
        self.fig_editmode.canvas.mpl_connect("motion_notify_event", self.on_motion)
        self.editmode_flag = True
        # showだと動く
        plt.show()
        # self.fig_editmode.canvas.draw()

    def update_graph_data(self):
        if self.update_value_x is None and self.update_value_y is None and \
                self.update_value_z is None:
            return
        f = h5py.File(self.hdfpath, 'r+')
        swap_data = f[''.join(self.object_id)][()]
        # ここで文字列を連結したい
#         swap_data[self.ind][self.graph_axis_list[0]] = self.update_value_ + self.graph_axis_list[0]
        exec("swap_data[self.ind][self.graph_axis_list[0]] = self.update_value_%s" % (self.graph_axis_list[0]))
        exec("swap_data[self.ind][self.graph_axis_list[1]] = self.update_value_%s" % (self.graph_axis_list[1]))
        del f[''.join(self.object_id)]
        f.create_dataset(''.join(self.object_id), data=swap_data)
        f.close()

    def update_graph_drawing(self):
        self.points.remove()
        f = h5py.File(self.hdfpath, 'r')
        data = f[''.join(self.object_id)]
        self.points = self.ax.scatter3D(data['x'].astype(np.float),
                                        data['y'].astype(np.float),
                                        data['z'].astype(np.float),
                                        s=1, picker=10)
        self.x_data, self.y_data = data[self.graph_axis_list[0]], data[self.graph_axis_list[1]]
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
