from PyQt5 import QtWidgets, QtCore, QtGui
from gantt_chart import GanttChart
from openai_client import ask_openai
from scheduler import fifo, sjf, priority_scheduling


class SchedulerApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Algoritmos de Despacho de Procesos')
        self.setGeometry(100, 100, 1200, 800)

        # Configuración de layouts
        main_layout = QtWidgets.QVBoxLayout()
        input_layout = QtWidgets.QGridLayout()
        button_layout = QtWidgets.QHBoxLayout()

        # Campos de entrada de datos
        input_layout.addWidget(QtWidgets.QLabel('ID del Proceso'), 0, 0)
        input_layout.addWidget(QtWidgets.QLabel('Tiempo de Llegada'), 0, 1)
        input_layout.addWidget(QtWidgets.QLabel('Tiempo de Ejecución'), 0, 2)
        input_layout.addWidget(QtWidgets.QLabel('Prioridad'), 0, 3)

        self.process_id_input = QtWidgets.QLineEdit()
        self.arrival_time_input = QtWidgets.QLineEdit()
        self.burst_time_input = QtWidgets.QLineEdit()
        self.priority_input = QtWidgets.QLineEdit()
        self.priority_input.setPlaceholderText("Ignorado en FIFO/SJF")

        input_layout.addWidget(self.process_id_input, 1, 0)
        input_layout.addWidget(self.arrival_time_input, 1, 1)
        input_layout.addWidget(self.burst_time_input, 1, 2)
        input_layout.addWidget(self.priority_input, 1, 3)

        # Botones
        add_button = QtWidgets.QPushButton('Agregar Proceso')
        add_button.clicked.connect(self.add_process)
        button_layout.addWidget(add_button)

        self.algorithm_selection = QtWidgets.QComboBox()
        self.algorithm_selection.addItems(['FIFO', 'SJF', 'Prioridad'])
        self.algorithm_selection.currentIndexChanged.connect(self.toggle_priority_input)
        button_layout.addWidget(self.algorithm_selection)

        generate_button = QtWidgets.QPushButton('Generar Diagrama')
        generate_button.clicked.connect(self.generate_gantt)
        button_layout.addWidget(generate_button)

        reset_button = QtWidgets.QPushButton('Reiniciar Todo')
        reset_button.clicked.connect(self.reset_all)
        button_layout.addWidget(reset_button)

        # Tabla para procesos y resultados
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(['ID', 'Llegada', 'Ejecución', 'Prioridad', 'Espera', 'Finalización'])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget::item:selected {
                background-color: #B3E5FC;
            }
            QTableWidget {
                background-color: #F5F5F5;
                alternate-background-color: #E0F7FA;
                selection-background-color: #B2EBF2;
            }
            QHeaderView::section {
                background-color: #0288D1;
                color: white;
                font-weight: bold;
            }
        """)

        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table, stretch=3)

        # Gráfico de Gantt
        self.gantt_chart = GanttChart(self)
        self.gantt_chart.setMinimumHeight(300)
        self.gantt_chart.setMinimumWidth(800)
        self.gantt_chart.mouseDoubleClickEvent = self.show_gantt_chart_fullscreen
        main_layout.addWidget(self.gantt_chart, stretch=3)

        # Entrada de preguntas para GPT
        gpt_layout = QtWidgets.QHBoxLayout()
        self.question_input = QtWidgets.QTextEdit()
        self.question_input.setPlaceholderText("Haz una pregunta sobre los resultados o funcionamiento...")
        self.question_input.setMaximumHeight(100)
        gpt_layout.addWidget(self.question_input)

        ask_button = QtWidgets.QPushButton('Preguntar a GPT')
        ask_button.clicked.connect(self.ask_openai)
        gpt_layout.addWidget(ask_button)

        main_layout.addLayout(gpt_layout)

        # Salida de respuestas de GPT
        self.answer_output = QtWidgets.QTextBrowser()
        self.answer_output.setReadOnly(True)
        main_layout.addWidget(self.answer_output, stretch=1)

        self.setLayout(main_layout)

        # Inicializar lista de procesos y historial de resultados
        self.processes = []
        self.history = []

    def toggle_priority_input(self):
        """Habilita o deshabilita el campo de prioridad dependiendo del algoritmo seleccionado."""
        algorithm = self.algorithm_selection.currentText()
        if algorithm in ['FIFO', 'SJF']:
            self.priority_input.setDisabled(True)
            self.priority_input.setText('0')
        else:
            self.priority_input.setDisabled(False)
            self.priority_input.clear()

    def add_process(self):
        """Agregar un nuevo proceso a la lista de procesos."""
        try:
            process_id = self.process_id_input.text()
            arrival_time = int(self.arrival_time_input.text())
            burst_time = int(self.burst_time_input.text())

            if self.algorithm_selection.currentText() == 'Prioridad':
                priority = int(self.priority_input.text())
            else:
                priority = 0

            self.processes.append((process_id, arrival_time, burst_time, priority))
            self.update_table()
            self.clear_inputs()
        except ValueError:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Por favor, ingrese valores válidos.')

    def clear_inputs(self):
        """Limpiar los campos de entrada de datos."""
        self.process_id_input.clear()
        self.arrival_time_input.clear()
        self.burst_time_input.clear()
        self.priority_input.clear()

    def update_table(self):
        """Actualizar la tabla de procesos con los datos ingresados."""
        self.table.setRowCount(len(self.processes))
        for i, (pid, at, bt, pr) in enumerate(self.processes):
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(pid))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(str(at)))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(str(bt)))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(pr)))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(''))
            self.table.setItem(i, 5, QtWidgets.QTableWidgetItem(''))

    def generate_gantt(self):
        """Generar el diagrama de Gantt y mostrar métricas según el algoritmo seleccionado."""
        if not self.processes:
            QtWidgets.QMessageBox.warning(self, 'Error', 'No hay procesos para programar.')
            return

        self.gantt_chart.ax.clear()
        self.table.setRowCount(len(self.processes))

        algorithm = self.algorithm_selection.currentText()

        if algorithm == 'FIFO':
            schedule, metrics = fifo(self.processes)
        elif algorithm == 'SJF':
            schedule, metrics = sjf(self.processes)
        elif algorithm == 'Prioridad':
            schedule, metrics = priority_scheduling(self.processes)

        self.history.append({
            'algorithm': algorithm,
            'processes': self.processes.copy(),
            'schedule': schedule,
            'metrics': metrics
        })

        self.gantt_chart.plot_gantt(schedule)
        self.show_metrics(metrics)

    def show_metrics(self, metrics):
        """Mostrar las métricas de los procesos en la tabla."""
        total_waiting_time = 0
        total_turnaround_time = 0
        num_processes = len(metrics)

        for i, metric in enumerate(metrics):
            process_id, waiting_time, turnaround_time = metric
            for row in range(self.table.rowCount()):
                if self.table.item(row, 0).text() == process_id:
                    self.table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(waiting_time)))
                    self.table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(turnaround_time)))
                    total_waiting_time += waiting_time
                    total_turnaround_time += turnaround_time
                    break

        total_row = self.table.rowCount()
        self.table.insertRow(total_row)
        self.table.setItem(total_row, 0, QtWidgets.QTableWidgetItem('Totales / Promedios'))
        self.table.item(total_row, 0).setBackground(QtGui.QColor('#FFEB3B'))
        self.table.setItem(total_row, 4, QtWidgets.QTableWidgetItem(f'Suma: {total_waiting_time}, Promedio: {total_waiting_time / num_processes:.2f}'))
        self.table.item(total_row, 4).setBackground(QtGui.QColor('#FFEB3B'))
        self.table.setItem(total_row, 5, QtWidgets.QTableWidgetItem(f'Suma: {total_turnaround_time}, Promedio: {total_turnaround_time / num_processes:.2f}'))
        self.table.item(total_row, 5).setBackground(QtGui.QColor('#FFEB3B'))

    def reset_all(self):
        """Reiniciar todos los datos y la interfaz."""
        self.processes.clear()
        self.history.clear()
        self.table.setRowCount(0)
        self.gantt_chart.ax.clear()
        self.gantt_chart.draw()
        QtWidgets.QMessageBox.information(self, 'Reiniciar', 'Todos los datos han sido reiniciados.')

    def ask_openai(self):
        """Manejar la interacción con OpenAI GPT."""
        question = self.question_input.toPlainText()
        if question.strip():
            context = self.generate_context()
            answer = ask_openai(context, question)
            self.answer_output.setMarkdown(answer)
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Por favor, ingrese una pregunta.')

    def generate_context(self):
        """Generar una descripción detallada del contexto actual de la aplicación."""
        context = "### Historial Completo de Ejecuciones ###\n"

        for entry in self.history:
            context += f"\n--- Algoritmo: {entry['algorithm']} ---\n"
            for process in entry['processes']:
                pid, at, bt, pr = process
                context += f"Proceso {pid}: Llegada={at}, Ejecución={bt}, Prioridad={pr}\n"

            context += "\nResultados:\n"
            for pid, wait, turnaround in entry['metrics']:
                context += f"Proceso {pid}: Espera={wait}, Finalización={turnaround}\n"

            context += "\nDescripción de la Gráfica de Gantt:\n"
            for pid, start, end in entry['schedule']:
                duration = end - start
                context += f"Proceso {pid}: Inicio={start}, Fin={end}, Duración={duration}\n"

        return context

    def show_gantt_chart_fullscreen(self, event):
        """Mostrar el diagrama de Gantt en una ventana más grande al hacer doble clic."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Diagrama de Gantt Ampliado")
        dialog.setGeometry(50, 50, 1000, 700)
        gantt_chart_large = GanttChart(dialog)
        gantt_chart_large.setMinimumWidth(950)
        gantt_chart_large.plot_gantt(self.gantt_chart.current_schedule)
        dialog_layout = QtWidgets.QVBoxLayout()
        dialog_layout.addWidget(gantt_chart_large)
        dialog.setLayout(dialog_layout)
        dialog.exec_()
