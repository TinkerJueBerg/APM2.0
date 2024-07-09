import sys
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import pyqtgraph as pg
import pynput
from PyQt5.QtGui import *


        
class MainWindow(QMainWindow):
    def __init__(self,parent=None):
        super().__init__()
        super(MainWindow, self).__init__(parent)
        
        # 布局函数 def layout 
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setRenderHint(QPainter.Antialiasing)
        self.layout.addWidget(self.graphWidget)
       # self.plot_graph()
        
        # APM计算属性 APM calculator
        self.x = 0
        self.count = 0
        self.queue_60 = []
        self.apm = 0
        self.x_values = []
        self.y_values = []
        
        # x_axis length
        self.duration = 1800
        
        # 时间控制器 time contorller
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(1000)  

        # 监听器 listener
        #self.closeEvent = self.on_close
        self.mouse_listener = pynput.mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = pynput.keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.keyboard_listener.start()
        
           
    def update_plot(self):
        if self.x < self.duration:
            self.x += 1
            self.x_values.append(self.x)
        else:   
            self.y_values.pop(0)
        
        if self.x <= 60:
            pass
        else:
            self.apm -= self.queue_60[0]
            self.queue_60.pop(0)
            
        self.queue_60.append(self.count)
        self.apm += self.count      
        self.y_values.append(self.apm)
        # reset count
        self.count = 0 
        self.plot_graph()
        
    def plot_graph(self):
        
        pen1 = pg.mkPen(color=(85, 159, 236), width=2)  
        pen2 = pg.mkPen(color=(42, 74, 118), width=2)  
        
        self.graphWidget.setBackground('w')
        self.graphWidget.setTitle('APM统计,现在的APM是{}'.format(self.apm),font='30',color='black')  # 设置标题
        self.graphWidget.setLabel('left', 'APMs', font='Arial, 20')  # 设置 Y 轴标签
        self.graphWidget.setLabel('bottom', 'Times', font='Arial, 20')  # 设置 X 轴标签
        self.graphWidget.showGrid(x=True, y=True)  # 显示网格
        self.graphWidget.addLegend()
        self.graphWidget.plot(self.x_values, self.y_values, pen=pen1, clear=True,name="total_APM")

        
        
    def on_click(self, x, y, button, pressed):
        if pressed:
            self.count += 1

    def on_press(self, key):
        self.count += 1

    def on_close(self, event):
        # 停止定时器
        self.timer.stop()
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("APM统计器")
    window.show()
    sys.exit(app.exec_())
