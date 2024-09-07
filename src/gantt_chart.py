import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class GanttChart(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)
        plt.style.use('ggplot')

        # Para almacenar el horario actual
        self.current_schedule = []

    def plot_gantt(self, schedule):
        """Dibuja el diagrama de Gantt basado en el horario proporcionado."""
        self.current_schedule = schedule  # Almacena el horario actual
        self.ax.clear()
        self.ax.set_xlabel('Tiempo')
        self.ax.set_ylabel('Procesos')

        yticks = []
        ylabels = []

        colors = plt.cm.Paired(np.linspace(0, 1, len(schedule)))

        for i, (process_id, start, end) in enumerate(schedule):
            self.ax.broken_barh([(start, end - start)], (10 * i, 9), facecolors=(colors[i]))
            yticks.append(10 * i + 4.5)
            ylabels.append(process_id)
            self.ax.text(start + (end - start) / 2, 10 * i + 4.5, process_id,
                        ha='center', va='center', color='white', fontsize=10, weight='bold')

        self.ax.set_yticks(yticks)
        self.ax.set_yticklabels(ylabels)
        self.ax.grid(True, linestyle='--', alpha=0.6)
        self.ax.set_xticks(np.arange(0, max(end for _, _, end in schedule) + 1, 1))

        self.draw()
