from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import socket
import json

# Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

# Define a top-level widget to hold everything
w = pg.GraphicsLayoutWidget()
plot_flux = w.addPlot(row=0, col=0)
plot_dose = w.addPlot(row=1, col=0)

# Add widgets to the layout in their proper positions
curve_flux = plot_flux.plot(pen=1)
curve_dose = plot_dose.plot(pen=2)
pg.setConfigOptions(antialias=True)
plot_flux.showGrid(True, True, 0.3)

# Display the widget as a new window
w.show()

# socket
locaddr = ('127.0.0.1', 50008)
sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)
sock.setblocking(False)
sock.bind(locaddr)
M_SIZE = 20000
data1 = [0] * 100


def update():
    try:
        global curve_flux, curve_dose, data1
        message, cli_addr = sock.recvfrom(M_SIZE)
        data = json.loads(message)
        # データ更新
        print(data)
        curve_flux.setData(data["energy"], data["flux"])

        data1[:-1] = data1[1:]
        data1[-1] = data["dose"]
        curve_dose.setData(data1)
        curve_dose.setPos(data["time"], 0)
    except:
        pass


fps = 10
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(int(1 / fps * 1000))

# Start the Qt event loop
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        app.exec()
