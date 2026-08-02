from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame
from PySide6.QtCore import QTimer
import pyqtgraph as pg
from manager.core.api_client import api_client


class MonitoringPage(QWidget):
    """Real-Time Performance Monitoring Page powered by PyQtGraph dynamic plotting."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cpu_history = [0] * 60
        self.ram_history = [0] * 60
        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_charts)
        self.timer.start(1000)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        header = QLabel("Real-Time System Metrics (PyQtGraph)")
        header.setObjectName("HeaderTitle")
        layout.addWidget(header)

        # Plot Container Card
        chart_card = QFrame()
        chart_card.setObjectName("Card")
        chart_layout = QVBoxLayout(chart_card)

        # Configure PyQtGraph global options
        pg.setConfigOption('background', '#1E293B')
        pg.setConfigOption('foreground', '#F8FAFC')

        # CPU Plot
        self.cpu_plot = pg.PlotWidget(title="CPU Core Utilization (%)")
        self.cpu_plot.setYRange(0, 100)
        self.cpu_plot.showGrid(x=True, y=True, alpha=0.3)
        self.cpu_curve = self.cpu_plot.plot(pen=pg.mkPen(color='#38BDF8', width=2))

        # RAM Plot
        self.ram_plot = pg.PlotWidget(title="RAM Memory Usage (%)")
        self.ram_plot.setYRange(0, 100)
        self.ram_plot.showGrid(x=True, y=True, alpha=0.3)
        self.ram_curve = self.ram_plot.plot(pen=pg.mkPen(color='#10B981', width=2))

        chart_layout.addWidget(self.cpu_plot)
        chart_layout.addWidget(self.ram_plot)
        layout.addWidget(chart_card)

    def update_charts(self):
        data = api_client.get_system_status()
        if data:
            cpu = data.get("cpu", 0.0)
            ram = data.get("ram", 0.0)
        else:
            cpu, ram = 0.0, 0.0

        self.cpu_history.pop(0)
        self.cpu_history.append(cpu)

        self.ram_history.pop(0)
        self.ram_history.append(ram)

        self.cpu_curve.setData(self.cpu_history)
        self.ram_curve.setData(self.ram_history)
