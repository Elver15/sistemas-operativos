import matplotlib.pyplot as plt
from collections import deque

def priority_round_robin(processes, quantum):
    n = len(processes)
    waiting_time = [0] * n
    turnaround_time = [0] * n

    # Convertir la lista de procesos en una cola
    queue = deque(processes)

    current_time = 0
    while queue:
        # Ordenar la cola por prioridad y tiempo de llegada
        queue = deque(sorted(queue, key=lambda x: (x[2], x[3])))

        process_name, burst_time, priority, arrival_time = queue.popleft()

        if burst_time <= quantum:
            # El proceso se completa antes de agotar el quantum
            current_time += burst_time
            turnaround_time[processes.index((process_name, burst_time, priority, arrival_time))] = current_time
        else:
            # Se agota el quantum, el proceso vuelve al final de la cola
            current_time += quantum
            queue.append((process_name, burst_time - quantum, priority, arrival_time))

    # Calcular el tiempo de espera para cada proceso
    for i in range(n):
        waiting_time[i] = turnaround_time[i] - processes[i][1]

    # Calcular el tiempo promedio de espera
    average_waiting_time = sum(waiting_time) / n

    # Imprimir resultados con tiempo de ráfaga, prioridad, tiempo de espera y tiempo de retorno
    print("Proceso\tTiempo de Ráfaga\tPrioridad\tTiempo de Espera\tTiempo de Retorno")
    for i in range(n):
        print(f"{processes[i][0]}\t\t{processes[i][1]}\t\t{processes[i][2]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}")

    # Crear el diagrama de Gantt
    gantt_chart_priority_rr(processes, turnaround_time, quantum, average_waiting_time)

def gantt_chart_priority_rr(processes, turnaround_time, quantum, average_waiting_time):
    fig, gnt = plt.subplots()

    gnt.set_ylim(0, 1)
    end_times = [turnaround_time[i] for i in range(len(turnaround_time))]
    gnt.set_xlim(0, end_times[-1])

    colors = plt.cm.get_cmap('tab10', len(processes))

    current_time = 0
    for i in range(len(processes)):
        process_name, process_time, _, _ = processes[i]
        gnt.broken_barh([(0, turnaround_time[i])], (0, 1), facecolors=[colors(i)], label=process_name)

        label_x = turnaround_time[i] / 2
        label_y = 0.5
        gnt.text(label_x, label_y, process_name, ha='center', va='center', color='white', fontsize=8)

    plt.text(0.5, -0.15, f'Tiempo promedio de espera: {average_waiting_time:.2f}', ha='center', va='center', transform=gnt.transAxes, fontsize=10)
    plt.text(0.5, -0.2, f'Quantum: {quantum}', ha='center', va='center', transform=gnt.transAxes, fontsize=10)

    gnt.set_xlabel('Tiempo')
    gnt.set_yticks([])
    gnt.set_title(f'Diagrama de Gantt - Priority Round Robin')
    gnt.legend()

    plt.show()

# Menú de entrada
processes = []
n = int(input("Ingrese la cantidad de procesos: "))
for i in range(1, n + 1):
    burst_time = int(input(f"Ingrese el tiempo de ráfaga para el proceso P{i}: "))
    priority = int(input(f"Ingrese la prioridad para el proceso P{i}: "))
    arrival_time = int(input(f"Ingrese el tiempo de llegada para el proceso P{i}: "))
    processes.append((f"P{i}", burst_time, priority, arrival_time))

quantum = int(input("Ingrese el quantum para Priority Round Robin: "))

# Llamar a la función Priority Round Robin con los valores proporcionados
priority_round_robin(processes, quantum)
