import unittest
import sys
import os

# Agregar el directorio raíz del proyecto al PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.scheduler import fifo, sjf, priority_scheduling
from src.openai_client import ask_openai
from src.gantt_chart import GanttChart
import matplotlib.pyplot as plt
class TestSchedulerAlgorithms(unittest.TestCase):

    def setUp(self):
        # Datos de la imagen proporcionada
        self.processes = [
            ('P1', 0, 2, 1),  # Proceso P1, Llegada=0, Ráfaga=2, Prioridad=1
            ('P2', 1, 8, 2),  # Proceso P2, Llegada=1, Ráfaga=8, Prioridad=2
            ('P3', 2, 6, 3),  # Proceso P3, Llegada=2, Ráfaga=6, Prioridad=3
            ('P4', 2, 7, 4),  # Proceso P4, Llegada=2, Ráfaga=7, Prioridad=4
            ('P5', 3, 4, 5),  # Proceso P5, Llegada=3, Ráfaga=4, Prioridad=5
            ('P6', 4, 6, 6)   # Proceso P6, Llegada=4, Ráfaga=6, Prioridad=6
        ]

    def test_fifo(self):
        # Probar el algoritmo de planificación FIFO
        schedule, metrics = fifo(self.processes)

        # Verificar el orden correcto de los procesos según FIFO
        self.assertEqual(schedule[0][0], 'P1')  # P1 debe estar primero
        self.assertEqual(schedule[1][0], 'P2')  # P2 debe estar segundo
        self.assertEqual(schedule[2][0], 'P3')  # P3 debe estar tercero
        
        # Verificar los tiempos de espera y de sistema (finalización)
        # Calcula los tiempos basados en los resultados esperados
        expected_waiting_times = [0, 1, 7, 12, 19, 20]  # Valores esperados para FIFO
        expected_turnaround_times = [2, 9, 13, 19, 23, 26]  # Valores esperados para FIFO

        for i, metric in enumerate(metrics):
            self.assertEqual(metric[1], expected_waiting_times[i])  # Verifica el tiempo de espera
            self.assertEqual(metric[2], expected_turnaround_times[i])  # Verifica el tiempo de sistema

    def test_sjf(self):
        # Probar el algoritmo de planificación SJF
        schedule, metrics = sjf(self.processes)

        # Verificar el orden correcto de los procesos según SJF
        self.assertEqual(schedule[0][0], 'P1')  # P1 debe estar primero
        self.assertEqual(schedule[1][0], 'P5')  # P5 debe estar segundo
        self.assertEqual(schedule[2][0], 'P3')  # P3 debe estar tercero
        
        # Verificar los tiempos de espera y de sistema
        # Añadir los cálculos esperados aquí basados en el orden de SJF
        expected_waiting_times = [0, 0, 6, 10, 11, 17]  # Valores esperados para SJF
        expected_turnaround_times = [2, 4, 12, 17, 19, 23]  # Valores esperados para SJF

        for i, metric in enumerate(metrics):
            self.assertEqual(metric[1], expected_waiting_times[i])
            self.assertEqual(metric[2], expected_turnaround_times[i])

    def test_priority_scheduling(self):
        # Probar el algoritmo de planificación por prioridad
        schedule, metrics = priority_scheduling(self.processes)

        # Verificar el orden correcto de los procesos según la prioridad
        self.assertEqual(schedule[0][0], 'P1')  # P1 debe estar primero (mayor prioridad)
        self.assertEqual(schedule[1][0], 'P2')  # P2 debe estar segundo (siguiente mayor prioridad)
        
        # Verificar los tiempos de espera y de sistema
        # Añadir los cálculos esperados aquí basados en el orden de prioridades
        expected_waiting_times = [0, 2, 10, 11, 13, 20]  # Valores esperados para Prioridad
        expected_turnaround_times = [2, 10, 16, 18, 19, 25]  # Valores esperados para Prioridad

        for i, metric in enumerate(metrics):
            self.assertEqual(metric[1], expected_waiting_times[i])
            self.assertEqual(metric[2], expected_turnaround_times[i])

class TestOpenAIClient(unittest.TestCase):

    def test_ask_openai(self):
        # Simulación de interacción con la API de OpenAI (reemplazar con una clave API válida para pruebas reales)
        context = "Contexto de prueba"
        question = "¿Qué es un algoritmo FIFO?"
        response = ask_openai(context, question)
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, '')

class TestGanttChart(unittest.TestCase):

    def test_plot_gantt(self):
        # Crear un objeto GanttChart
        fig, ax = plt.subplots()
        gantt_chart = GanttChart()

        # Ejemplo de programación para graficar
        schedule = [('P1', 0, 2), ('P2', 2, 10), ('P3', 10, 16)]

        # Llamar al método plot_gantt
        gantt_chart.plot_gantt(schedule)

        # Verificar si el gráfico se ha creado (esto es una verificación simple)
        self.assertTrue(gantt_chart.ax.has_data())


if __name__ == '__main__':
    unittest.main()