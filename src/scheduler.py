def fifo(processes):
    """
    Algoritmo de planificación FIFO (First In, First Out).

    Args:
        processes (list): Lista de tuplas (ID, tiempo_llegada, tiempo_ejecucion, prioridad).

    Returns:
        gantt_chart (list): Diagrama de Gantt con tuplas (ID, tiempo_inicio, tiempo_fin).
        metrics (list): Métricas con tuplas (ID, tiempo_espera, tiempo_retorno).
    """
    sorted_processes = sorted(processes, key=lambda x: x[1])  # Ordenar por tiempo de llegada
    start_time = 0
    gantt_chart = []
    metrics = []

    for process in sorted_processes:
        pid, arrival_time, burst_time, _ = process
        
        if start_time < arrival_time:
            start_time = arrival_time
        
        end_time = start_time + burst_time
        waiting_time = start_time - arrival_time
        turnaround_time = end_time - arrival_time
        
        gantt_chart.append((pid, start_time, end_time))
        metrics.append((pid, waiting_time, turnaround_time))
        
        start_time = end_time  # Actualizar tiempo de inicio para el siguiente proceso

    return gantt_chart, metrics
def sjf(processes):
    """
    Algoritmo de planificación SJF (Shortest Job First).

    Args:
        processes (list): Lista de tuplas (ID, tiempo_llegada, tiempo_ejecucion, prioridad).

    Returns:
        gantt_chart (list): Diagrama de Gantt con tuplas (ID, tiempo_inicio, tiempo_fin).
        metrics (list): Métricas con tuplas (ID, tiempo_espera, tiempo_retorno).
    """
    sorted_processes = sorted(processes, key=lambda x: x[1])
    remaining_processes = sorted_processes.copy()
    start_time = 0
    gantt_chart = []
    metrics = []

    while remaining_processes:
        available_processes = [p for p in remaining_processes if p[1] <= start_time]
        
        if not available_processes:
            start_time = min(p[1] for p in remaining_processes)
            continue

        next_process = min(available_processes, key=lambda x: x[2])
        remaining_processes.remove(next_process)
        
        pid, arrival_time, burst_time, _ = next_process
        end_time = start_time + burst_time
        waiting_time = start_time - arrival_time
        turnaround_time = end_time - arrival_time
        
        gantt_chart.append((pid, start_time, end_time))
        metrics.append((pid, waiting_time, turnaround_time))
        
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
    sorted_processes = sorted(processes, key=lambda x: x[1])
    remaining_processes = sorted_processes.copy()
    start_time = 0
    gantt_chart = []
    metrics = []

    while remaining_processes:
        available_processes = [p for p in remaining_processes if p[1] <= start_time]
        
        if not available_processes:
            start_time = min(p[1] for p in remaining_processes)
            continue

        next_process = min(available_processes, key=lambda x: x[3])
        remaining_processes.remove(next_process)
        
        pid, arrival_time, burst_time, priority = next_process
        end_time = start_time + burst_time
        waiting_time = start_time - arrival_time
        turnaround_time = end_time - arrival_time
        
        gantt_chart.append((pid, start_time, end_time))
        metrics.append((pid, waiting_time, turnaround_time))
        
        start_time = end_time

    return gantt_chart, metrics
