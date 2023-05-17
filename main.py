import sys
from typing import Optional
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow, QDialog, QVBoxLayout, QLabel
import PyQt6.QtWidgets as QtWidgets
from matplotlib.backend_bases import FigureCanvasBase
from ui import Ui_MainWindow
from algorithm import *
from asyncqt import QEventLoop, asyncSlot
from PyQt6.QtCore import QThread, pyqtSignal, pyqtSlot, QObject, QRunnable, QThreadPool, QCoreApplication
import qtinter
import asyncio
import random
import numpy as np
import pyqtgraph as pg
from decimal import Decimal
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class AlertDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setFixedWidth(300)
        self.setFixedHeight(100)
        self.setModal(True)
        self.layout = QVBoxLayout()
        if message == None:
            self.message = QLabel("Please enter the number of destinations")
        else:
            self.message = QLabel(message)
        self.layout.addWidget(self.message)
        self.setLayout(self.layout)

class Core(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isRunning = False
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btStart.clicked.connect(self.start)
        self.ui.btStop.clicked.connect(self.stop)
        self.task = None
        self.G = None
    
    def start(self):
        if self.isRunning == False:
            self.isRunning = True
            self.ui.canvaFrame.setVisible(True)
            print("Start")
            tsp = create_distance_matrix(int(self.ui.spinBox.value()))
            hill = HillClimbing(int(self.ui.spinBox.value()))
            a = hill.solve()
            self.ui.tbResult.setText(hill.result)
            self.ui.canvaFrame.canvas.axes.clear()
            distance = np.array(hill.matrix)
            G = nx.from_numpy_array(distance)
            print(G)
            pos = nx.spring_layout(G)
            # Vẽ các đỉnh và cạnh của đồ thị bằng Matplotlib
            nx.draw_networkx_nodes(G, pos, node_color='r')
            nx.draw_networkx_labels(G, pos)
            G.remove_edges_from(list(G.edges()))
            for i in range(len(a)-1):
                G.add_edge(a[i], a[i+1])
            nx.draw_networkx_edges(G, pos)
            self.G = G
            self.ui.canvaFrame.canvas.draw()
        else:
            dlg = AlertDialog("Please stop the current process")
            dlg.exec()
    def stop(self):
        if self.isRunning == True:
            self.isRunning = False
            print("Stop")
            self.ui.tbResult.setText("")
            self.ui.canvaFrame.setVisible(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Core()
    plt.axis('off')
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    with qtinter.using_qt_from_asyncio():
        window.show()
        sys.exit(app.exec())