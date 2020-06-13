import h5py
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

hdfpath = '../data/sample.h5'

x_data = []
y_data = []
z_data = []


def data_input(num):
    with h5py.File(hdfpath, 'r') as f:
        data = []
        data.append(f[num].value)
    return data


def data_load(num):
    object_id = 'data/' + str(num) + '/object/0'
    test_data = data_input(object_id)
    # numpy.ndarray型が返ってくる
    test_data = test_data[0]
    return test_data


def onclick(event):
    # init
    ind = event.ind[0]
    # error point
    x, y, z = event.artist._offsets3d
    print('x: {0}'.format(x[ind]), 'y: {0}'.format(y[ind]), 'z: {0}'.format(z[ind]))
    try:
        update_value_x = float(input('Enter x: '))
    except ValueError:
        print('Error')
        return
    global points, x_data, y_data, z_data
    list_x = list(x)
    list_x[ind] = update_value_x
    points.remove()
    ax.scatter3D(list_x, y_data, z_data, picker=10, color="blue")
    fig.canvas.draw()

# main

if __name__ == '__main__':
    fig = plt.figure()
    ax = Axes3D(fig)
    data_number = int(input('Enter time:'))
    for data in data_load(data_number):
        x_data.append(float(data[4].decode('utf-8')))
        y_data.append(float(data[5].decode('utf-8')))
        z_data.append(float(data[6].decode('utf-8')))

    points = ax.scatter3D(x_data, y_data, z_data, picker=10, color="red")
    fig.canvas.mpl_connect('pick_event', onclick)
    plt.show()
