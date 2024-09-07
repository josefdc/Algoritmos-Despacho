# scheduler.py

def fifo(processes):
    """
    Algoritmo de planificación FIFO (First In, First Out).

    Args:
        processes (list): Lista de tuplas (ID, tiempo_llegada, tiempo_ejecucion).

    Returns:
        gantt_chart (list): Diagrama de Gantt con tuplas (ID, tiempo_inicio, tiempo_fin).
        metrics (list): Métricas con tuplas (ID, tiempo_espera, tiempo_retorno).
    """
    # Ordenar los procesos por tiempo de llegada
    sorted_processes = sorted(processes, key=lambda x: x[1])
    start_time = 0
    gantt_chart = []
    metrics = []

    for process in sorted_processes:
        pid, arrival_time, burst_time = process
        
        # Ajustar el tiempo de inicio si el proceso llega después del tiempo actual
        if start_time < arrival_time:
            start_time = arrival_time
        
        end_time = start_time + burst_time
        gantt_chart.append((pid, start_time, end_time))
        
        # Calcular tiempos de espera y de retorno
        waiting_time = start_time - arrival_time
        turnaround_time = waiting_time + burst_time
        metrics.append((pid, waiting_time, turnaround_time))
        
        # Actualizar el tiempo de inicio para el siguiente proceso
        start_time = end_time

    return gantt_chart, metrics


def sjf(processes):
    """
    Algoritmo de planificación SJF (Shortest Job First).

    Args:
        processes (list): Lista de tuplas (ID, tiempo_llegada, tiempo_ejecucion).

    Returns:
        gantt_chart (list): Diagrama de Gantt con tuplas (ID, tiempo_inicio, tiempo_fin).
        metrics (list): Métricas con tuplas (ID, tiempo_espera, tiempo_retorno).
    """
    # Ordenar los procesos por tiempo de llegada
    sorted_processes = sorted(processes, key=lambda x: x[1])
    remaining_processes = sorted_processes.copy()
    start_time = 0
    gantt_chart = []
    metrics = []

    while remaining_processes:
        # Filtrar los procesos que ya han llegado
        available_processes = [p for p in remaining_processes if p[1] <= start_time]
        
        # Si no hay procesos disponibles, avanzar al tiempo de llegada del siguiente proceso
        if not available_processes:
            start_time = min(p[1] for p in remaining_processes)
            continue

        # Seleccionar el proceso con el menor tiempo de ejecución
        next_process = min(available_processes, key=lambda x: x[2])
        remaining_processes.remove(next_process)
        
        pid, arrival_time, burst_time = next_process
        end_time = start_time + burst_time
        gantt_chart.append((pid, start_time, end_time))
        
        # Calcular tiempos de espera y de retorno
        waiting_time = start_time - arrival_time
        turnaround_time = waiting_time + burst_time
        metrics.append((pid, waiting_time, turnaround_time))
        
        # Actualizar el tiempo de inicio
        start_time = end_time

    return gantt_chart, metrics


def priority_scheduling(processes):
    """
    Algoritmo de planificación por Prioridad.

    Args:
        processes (list): Lista de tuplas (ID, tiempo_llegada, tiempo_ejecucion, prioridad).

    Returns:
        gantt_chart (list): Diagrama de Gantt con tuplas (ID, tiempo_inicio, tiempo_fin).
        metrics (list): Métricas con tuplas (ID, tiempo_espera, tiempo_retorno).
    """
    # Ordenar los procesos por tiempo de llegada
    sorted_processes = sorted(processes, key=lambda x: x[1])
    remaining_processes = sorted_processes.copy()
    start_time = 0
    gantt_chart = []
    metrics = []

    while remaining_processes:
        # Filtrar los procesos que ya han llegado
        available_processes = [p for p in remaining_processes if p[1] <= start_time]
        
        # Si no hay procesos disponibles, avanzar al tiempo de llegada del siguiente proceso
        if not available_processes:
            start_time = min(p[1] for p in remaining_processes)
            continue

        # Seleccionar el proceso con la mayor prioridad (menor número)
        next_process = min(available_processes, key=lambda x: x[3])
        remaining_processes.remove(next_process)
        
        pid, arrival_time, burst_time, priority = next_process
        end_time = start_time + burst_time
        gantt_chart.append((pid, start_time, end_time))
        
        # Calcular tiempos de espera y de retorno
        waiting_time = start_time - arrival_time
        turnaround_time = waiting_time + burst_time
        metrics.append((pid, waiting_time, turnaround_time))
        
        # Actualizar el tiempo de inicio
        start_time = end_time

    return gantt_chart, metrics
