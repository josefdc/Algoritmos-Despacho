from PyQt5 import QtWidgets, QtCore
from gantt_chart import GanttChart
from openai_client import ask_openai
from scheduler import fifo, sjf, priority_scheduling


class SchedulerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Algoritmos de Despacho de Procesos')
        self.setGeometry(100, 100, 1000, 700)

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

        # Tables for processes and results
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(['ID', 'Llegada', 'Ejecución', 'Prioridad'])

        self.result_table = QtWidgets.QTableWidget()
        self.result_table.setColumnCount(3)
        self.result_table.setHorizontalHeaderLabels(['ID', 'Tiempo de Espera', 'Tiempo de Finalización'])

        # Gantt chart widget
        self.gantt_chart = GanttChart(self)

        # Question input for GPT
        self.question_input = QtWidgets.QTextEdit()
        self.question_input.setPlaceholderText("Haz una pregunta sobre los resultados o funcionamiento...")
        main_layout.addWidget(self.question_input)

        ask_button = QtWidgets.QPushButton('Preguntar a GPT')
        ask_button.clicked.connect(self.ask_openai)
        main_layout.addWidget(ask_button)

        # Answer output for GPT responses
        self.answer_output = QtWidgets.QTextEdit()
        self.answer_output.setReadOnly(True)
        main_layout.addWidget(self.answer_output)

        # Add all layouts to main layout
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table)
        main_layout.addWidget(self.result_table)
        main_layout.addWidget(self.gantt_chart)
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
        self.result_table.setRowCount(len(metrics) + 1)
        total_waiting_time = 0
        total_turnaround_time = 0

        for i, metric in enumerate(metrics):
            process_id, waiting_time, turnaround_time = metric
            self.result_table.setItem(i, 0, QtWidgets.QTableWidgetItem(process_id))
            self.result_table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(waiting_time)))
            self.result_table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(turnaround_time)))

            total_waiting_time += waiting_time
            total_turnaround_time += turnaround_time

        self.result_table.setItem(len(metrics), 0, QtWidgets.QTableWidgetItem('Totales / Promedios'))
        self.result_table.setItem(len(metrics), 1, QtWidgets.QTableWidgetItem(f'Suma: {total_waiting_time} / Promedio: {total_waiting_time / len(metrics):.2f}'))
        self.result_table.setItem(len(metrics), 2, QtWidgets.QTableWidgetItem(f'Suma: {total_turnaround_time} / Promedio: {total_turnaround_time / len(metrics):.2f}'))

    def reset_all(self):
        self.processes.clear()
        self.table.setRowCount(0)
        self.result_table.setRowCount(0)
        self.gantt_chart.ax.clear()
        self.gantt_chart.draw()
        QtWidgets.QMessageBox.information(self, 'Reiniciar', 'Todos los datos han sido reiniciados.')

    def ask_openai(self):
        """Handle interaction with OpenAI GPT."""
        question = self.question_input.toPlainText()
        if question.strip():
            context = self.generate_context()
            answer = ask_openai(context, question)
            self.answer_output.setText(answer)
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Por favor, ingrese una pregunta.')

    def generate_context(self):
        """Generates a description of the current context of the application."""
        context = "Procesos actuales en la cola:\n"

        for process in self.processes:
            process_id, arrival_time, burst_time, priority = process
            context += f"- Proceso {process_id}: Tiempo de Llegada={arrival_time}, Tiempo de Ejecución={burst_time}, Prioridad={priority}\n"

        if self.result_table.rowCount() > 0:
            context += "\nResultados del último algoritmo de planificación:\n"
            for row in range(self.result_table.rowCount() - 1):
                process_id = self.result_table.item(row, 0).text()
                waiting_time = self.result_table.item(row, 1).text()
                turnaround_time = self.result_table.item(row, 2).text()
                context += f"- Proceso {process_id}: Tiempo de Espera={waiting_time}, Tiempo de Finalización={turnaround_time}\n"

            total_waiting_time = self.result_table.item(self.result_table.rowCount() - 1, 1).text()
            total_turnaround_time = self.result_table.item(self.result_table.rowCount() - 1, 2).text()
            context += f"Totales / Promedios: Tiempo de Espera={total_waiting_time}, Tiempo de Finalización={total_turnaround_time}\n"

        context += "\nAlgoritmo de planificación utilizado: " + self.algorithm_selection.currentText()

        return context
