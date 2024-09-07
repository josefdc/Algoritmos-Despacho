import unittest
from src.scheduler import fifo, sjf, priority_scheduling
from src.openai_client import ask_openai
from src.gantt_chart import GanttChart
import matplotlib.pyplot as plt

class TestSchedulerAlgorithms(unittest.TestCase):

    def setUp(self):
        # Example data to use in multiple tests
        self.processes = [
            ('P1', 0, 3, 2),
            ('P2', 1, 5, 1),
            ('P3', 2, 2, 3)
        ]

    def test_fifo(self):
        # Test FIFO scheduling algorithm
        schedule, metrics = fifo(self.processes)
        self.assertEqual(len(schedule), len(self.processes))
        self.assertEqual(schedule[0][0], 'P1')  # P1 should be scheduled first
        self.assertEqual(metrics[0][1], 0)  # Waiting time for P1 should be 0

    def test_sjf(self):
        # Test SJF scheduling algorithm
        schedule, metrics = sjf(self.processes)
        self.assertEqual(len(schedule), len(self.processes))
        # Check if processes are sorted by burst time after arrival time consideration
        self.assertEqual(schedule[0][0], 'P1')  # P1 should be scheduled first because it has the shortest job

    def test_priority_scheduling(self):
        # Test Priority scheduling algorithm
        schedule, metrics = priority_scheduling(self.processes)
        self.assertEqual(len(schedule), len(self.processes))
        # Check if processes are sorted by priority (lower number is higher priority)
        self.assertEqual(schedule[0][0], 'P2')  # P2 has the highest priority

class TestOpenAIClient(unittest.TestCase):

    def test_ask_openai(self):
        # Mock OpenAI API interaction (Replace with a valid API key for real testing)
        context = "Contexto de prueba"
        question = "¿Qué es un algoritmo FIFO?"
        response = ask_openai(context, question)
        # Check if the response is a non-empty string
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, '')

class TestGanttChart(unittest.TestCase):

    def test_plot_gantt(self):
        # Create a GanttChart object
        fig, ax = plt.subplots()
        gantt_chart = GanttChart()

        # Example schedule to plot
        schedule = [('P1', 0, 3), ('P2', 3, 5), ('P3', 8, 2)]

        # Call the plot_gantt method
        gantt_chart.plot_gantt(schedule)

        # Check if the plot is created (this is a simple check)
        self.assertTrue(gantt_chart.ax.has_data())


if __name__ == '__main__':
    unittest.main()
