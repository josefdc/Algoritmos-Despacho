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
        # Datos del ejemplo en la imagen
        self.processes = [
            ('P1', 0, 2, 0),
            ('P2', 1, 8, 1),
            ('P3', 6, 2, 2),
            ('P4', 2, 7, 3),
            ('P5', 3, 4, 4),
            ('P6', 4, 6, 5)
        ]

    def test_fifo(self):
        # Resultados esperados para FIFO
        expected_gantt = [('P1', 0, 2), ('P2', 2, 10), ('P3', 10, 12), ('P4', 12, 19), ('P5', 19, 23), ('P6', 23, 29)]
        expected_metrics = [('P1', 0, 2), ('P2', 1, 9), ('P3', 4, 6), ('P4', 10, 17), ('P5', 16, 20), ('P6', 19, 25)]
        
        # Test FIFO scheduling algorithm
        schedule, metrics = fifo(self.processes)
        self.assertEqual(schedule, expected_gantt)
        self.assertEqual(metrics, expected_metrics)

    def test_sjf(self):
        # Resultados esperados para SJF
        expected_gantt = [('P1', 0, 2), ('P3', 2, 4), ('P5', 4, 8), ('P6', 8, 14), ('P4', 14, 21), ('P2', 21, 29)]
        expected_metrics = [('P1', 0, 2), ('P3', 0, 2), ('P5', 1, 5), ('P6', 4, 10), ('P4', 12, 19), ('P2', 20, 28)]

        # Test SJF scheduling algorithm
        schedule, metrics = sjf(self.processes)
        self.assertEqual(schedule, expected_gantt)
        self.assertEqual(metrics, expected_metrics)

    def test_priority_scheduling(self):
        # Resultados esperados para Prioridad
        expected_gantt = [('P1', 0, 2), ('P2', 2, 10), ('P3', 10, 12), ('P4', 12, 19), ('P5', 19, 23), ('P6', 23, 29)]
        expected_metrics = [('P1', 0, 2), ('P2', 1, 9), ('P3', 4, 6), ('P4', 10, 17), ('P5', 16, 20), ('P6', 19, 25)]
        
        # Test Priority scheduling algorithm
        schedule, metrics = priority_scheduling(self.processes)
        self.assertEqual(schedule, expected_gantt)
        self.assertEqual(metrics, expected_metrics)

if __name__ == '__main__':
    unittest.main()
