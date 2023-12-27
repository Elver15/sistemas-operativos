import matplotlib.pyplot as plt

def round_robin(processes, quantum):
    # 1. Inicialización de variables
    n = len(processes)
    waiting_time = [0] * n

    remaining_time = [burst_time for _, burst_time in processes]

    current_time = 0
    
    # 2. Ejecución del algoritmo Round Robin
    while any(remaining_time):
        for i in range(n):
            if remaining_time[i] > 0:
                if remaining_time[i] <= quantum:
                    # Proceso completo antes de agotar el quantum
                    waiting_time[i] += current_time
                    current_time += remaining_time[i]
                    remaining_time[i] = 0
                else:
                    # Agotado el quantum, el proceso se vuelve al final de la cola
                    waiting_time[i] += current_time
                    current_time += quantum
                    remaining_time[i] -= quantum

    # 3. Cálculo del tiempo promedio de espera
    average_waiting_time = sum(waiting_time) / n

    # 4. Impresión de resultados
    print("Proceso\tTiempo de Ráfaga\tTiempo de Espera")
    for i in range(n):
        print(f"{processes[i][0]}\t\t{processes[i][1]}\t\t{waiting_time[i]}")

    # 5. Creación del diagrama de Gantt
    gantt_chart_rr(processes, waiting_time, quantum, average_waiting_time)

def gantt_chart_rr(processes, waiting_time, quantum, average_waiting_time):
    # 6. Configuración del gráfico de Gantt
    fig, gnt = plt.subplots()

    gnt.set_ylim(0, 1)
    end_times = [waiting_time[i] + processes[i][1] for i in range(len(waiting_time))]
    gnt.set_xlim(0, end_times[-1])

    colors = plt.cm.get_cmap('tab10', len(processes))

    current_time = 0
    
    # 7. Dibujo del diagrama de Gantt
    for i in range(len(processes)):
        process_name, process_time = processes[i]
        gnt.broken_barh([(waiting_time[i], process_time)], (0, 1), facecolors=[colors(i)], label=process_name)

        label_x = waiting_time[i] + process_time / 2
        label_y = 0.5
        gnt.text(label_x, label_y, process_name, ha='center', va='center', color='white', fontsize=8)

    # 8. Agregado de texto con información adicional
    plt.text(0.5, -0.15, f'Tiempo promedio de espera: {average_waiting_time:.2f}', ha='center', va='center', transform=gnt.transAxes, fontsize=10)
    plt.text(0.5, -0.2, f'Quantum: {quantum}', ha='center', va='center', transform=gnt.transAxes, fontsize=10)

    # 9. Configuración final y visualización del gráfico
    gnt.set_xlabel('Tiempo')
    gnt.set_yticks([])
    gnt.set_title(f'Diagrama de Gantt - Round Robin')
    gnt.legend()

    plt.show()

# 10. Entrada de datos mediante usuario
processes = []
n = int(input("Ingrese la cantidad de procesos: "))
for i in range(1, n + 1):
    burst_time = int(input(f"Ingrese el tiempo de ráfaga para el proceso P{i}: "))
    processes.append((f"P{i}", burst_time))

quantum = int(input("Ingrese el quantum para Round Robin: "))

# 11. Llamada a la función Round Robin con los valores proporcionados
round_robin(processes, quantum)
