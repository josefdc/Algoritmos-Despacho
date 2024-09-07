from PyQt5 import QtWidgets, QtCore
from gantt_chart import GanttChart
from openai_client import ask_openai
from scheduler import fifo, sjf, priority_scheduling


class SchedulerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Algoritmos de Despacho de Procesos')
        self.setGeometry(100, 100, 1200, 800)

        # Layouts
        main_layout = QtWidgets.QVBoxLayout()
        input_layout = QtWidgets.QGridLayout()
        button_layout = QtWidgets.QHBoxLayout()

        # Data entry fields
        input_layout.addWidget(QtWidgets.QLabel('ID del Proceso'), 0, 0)
        input_layout.addWidget(QtWidgets.QLabel('Tiempo de Llegada'), 0, 1)
        input_layout.addWidget(QtWidgets.QLabel('Tiempo de Ejecución'), 0, 2)
        input_layout.addWidget(QtWidgets.QLabel('Prioridad'), 0, 3)

        self.process_id_input = QtWidgets.QLineEdit()
        self.arrival_time_input = QtWidgets.QLineEdit()
        self.burst_time_input = QtWidgets.QLineEdit()
        self.priority_input = QtWidgets.QLineEdit()

        input_layout.addWidget(self.process_id_input, 1, 0)
        input_layout.addWidget(self.arrival_time_input, 1, 1)
        input_layout.addWidget(self.burst_time_input, 1, 2)
        input_layout.addWidget(self.priority_input, 1, 3)

        # Buttons
        add_button = QtWidgets.QPushButton('Agregar Proceso')
        add_button.clicked.connect(self.add_process)
        button_layout.addWidget(add_button)

        self.algorithm_selection = QtWidgets.QComboBox()
        self.algorithm_selection.addItems(['FIFO', 'SJF', 'Prioridad'])
        button_layout.addWidget(self.algorithm_selection)

        generate_button = QtWidgets.QPushButton('Generar Diagrama')
        generate_button.clicked.connect(self.generate_gantt)
        button_layout.addWidget(generate_button)

        reset_button = QtWidgets.QPushButton('Reiniciar Todo')
        reset_button.clicked.connect(self.reset_all)
        button_layout.addWidget(reset_button)

        # Combined table for processes and results
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Llegada', 'Ejecución', 'Prioridad', 'Espera', 'Finalización'])

        # Add all layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)

        # Gantt chart widget
        self.gantt_chart = GanttChart(self)
        self.gantt_chart.setMinimumHeight(300)  # Set a minimum height for better visibility
        self.gantt_chart.mouseDoubleClickEvent = self.show_gantt_chart_fullscreen  # Connect double click to enlarge the chart
        main_layout.addWidget(self.gantt_chart)

        # Question input for GPT
        self.question_input = QtWidgets.QTextEdit()
        self.question_input.setPlaceholderText("Haz una pregunta sobre los resultados o funcionamiento...")
        main_layout.addWidget(self.question_input)

        ask_button = QtWidgets.QPushButton('Preguntar a GPT')
        ask_button.clicked.connect(self.ask_openai)
        main_layout.addWidget(ask_button)

        # Answer output for GPT responses using QTextBrowser for Markdown support
        self.answer_output = QtWidgets.QTextBrowser()
        self.answer_output.setReadOnly(True)
        main_layout.addWidget(self.answer_output)

        # Set the main layout
        self.setLayout(main_layout)

        # Initialize processes list
        self.processes = []

    def add_process(self):
        try:
            process_id = self.process_id_input.text()
            arrival_time = int(self.arrival_time_input.text())
            burst_time = int(self.burst_time_input.text())
            priority = int(self.priority_input.text())

            self.processes.append((process_id, arrival_time, burst_time, priority))
            self.update_table()
            self.clear_inputs()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Por favor, ingrese valores válidos.')

    def clear_inputs(self):
        self.process_id_input.clear()
        self.arrival_time_input.clear()
        self.burst_time_input.clear()
        self.priority_input.clear()

    def update_table(self):
        self.table.setRowCount(len(self.processes))
        for i, (pid, at, bt, pr) in enumerate(self.processes):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(pid))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(at)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(bt)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(pr)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(''))  # Clear waiting time
            self.table.setItem(i, 5, QtWidgets.QTableWidgetItem(''))  # Clear turnaround time

    def generate_gantt(self):
        if not self.processes:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No hay procesos para programar.')
            return

        algorithm = self.algorithm_selection.currentText()

        if algorithm == 'FIFO':
            schedule, metrics = fifo(self.processes)
        elif algorithm == 'SJF':
            schedule, metrics = sjf(self.processes)
        elif algorithm == 'Prioridad':
            schedule, metrics = priority_scheduling(self.processes)

        self.gantt_chart.plot_gantt(schedule)
        self.show_metrics(metrics)

    def show_metrics(self, metrics):
        total_waiting_time = 0
        total_turnaround_time = 0
        num_processes = len(metrics)

        for i, metric in enumerate(metrics):
            process_id, waiting_time, turnaround_time = metric
            # Find the corresponding process row
            for row in range(self.table.rowCount()):
                if self.table.item(row, 0).text() == process_id:
                    self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(waiting_time)))
                    self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(turnaround_time)))
                    total_waiting_time += waiting_time
                    total_turnaround_time += turnaround_time
                    break

        # Mostrar totales y promedios
        total_row = self.table.rowCount()
        self.table.insertRow(total_row)
        self.table.setItem(total_row, 0, QtWidgets.QTableWidgetItem('Totales / Promedios'))
        self.table.setItem(total_row, 4, QtWidgets.QTableWidgetItem(f'Suma: {total_waiting_time}, Promedio: {total_waiting_time / num_processes:.2f}'))
        self.table.setItem(total_row, 5, QtWidgets.QTableWidgetItem(f'Suma: {total_turnaround_time}, Promedio: {total_turnaround_time / num_processes:.2f}'))

    def reset_all(self):
        self.processes.clear()
        self.table.setRowCount(0)
        self.gantt_chart.ax.clear()
        self.gantt_chart.draw()
        QtWidgets.QMessageBox.information(self, 'Reiniciar', 'Todos los datos han sido reiniciados.')

    def ask_openai(self):
        """Handle interaction with OpenAI GPT."""
        question = self.question_input.toPlainText()
        if question.strip():
            context = self.generate_context()
            answer = ask_openai(context, question)
            # Set answer with Markdown support
            self.answer_output.setMarkdown(answer)
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Por favor, ingrese una pregunta.')

    def generate_context(self):
        """Generates a detailed description of the current context of the application."""
        context = "### Procesos Actuales en la Cola ###\n"

        # Incluir detalles de cada proceso en la cola
        for process in self.processes:
            process_id, arrival_time, burst_time, priority = process
            context += f"Proceso {process_id}: Llegada={arrival_time}, Ejecución={burst_time}, Prioridad={priority}\n"

        # Incluir resultados de la planificación actual si están disponibles
        if self.table.rowCount() > 0:
            context += "\n### Resultados del Último Algoritmo de Planificación ###\n"
            for row in range(self.table.rowCount() - 1):  # Excluir la última fila de totales/promedios
                process_id = self.table.item(row, 0).text()
                waiting_time = self.table.item(row, 4).text()
                turnaround_time = self.table.item(row, 5).text()
                context += f"Proceso {process_id}: Espera={waiting_time}, Finalización={turnaround_time}\n"

            total_waiting_time = self.table.item(self.table.rowCount() - 1, 4).text()
            total_turnaround_time = self.table.item(self.table.rowCount() - 1, 5).text()
            context += f"Totales / Promedios: Tiempo de Espera={total_waiting_time}, Tiempo de Finalización={total_turnaround_time}\n"

        # Incluir algoritmo de planificación utilizado
        context += "\n### Algoritmo de Planificación Utilizado ###\n"
        context += self.algorithm_selection.currentText()

        # Descripción de la gráfica de Gantt
        context += "\n\n### Descripción de la Gráfica de Gantt Actual ###\n"
        if self.gantt_chart.current_schedule:
            for process_id, start, end in self.gantt_chart.current_schedule:
                duration = end - start
                context += f"Proceso {process_id}: Inicio={start}, Fin={end}, Duración={duration} unidades de tiempo\n"
            total_time = max(end for _, _, end in self.gantt_chart.current_schedule)
            context += f"Tiempo total en el diagrama de Gantt: {total_time} unidades de tiempo.\n"
        else:
            context += "No hay un diagrama de Gantt generado actualmente.\n"

        return context

    def show_gantt_chart_fullscreen(self, event):
        """Show the Gantt chart in a larger window when double-clicked."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Diagrama de Gantt Ampliado")
        dialog.setGeometry(100, 100, 800, 600)
        gantt_chart_large = GanttChart(dialog)
        gantt_chart_large.plot_gantt(self.gantt_chart.current_schedule)  # Reutilizar el último horario generado
        dialog_layout = QtWidgets.QVBoxLayout()
        dialog_layout.addWidget(gantt_chart_large)
        dialog.setLayout(dialog_layout)
        dialog.exec_()
