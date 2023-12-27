import matplotlib.pyplot as plt

def fcfs(processos):
    n = len(processos)
    tiempo_espera = [0] * n

    # Calcular el tiempo de espera para cada proceso
    for i in range(1, n):
        tiempo_espera[i] = tiempo_espera[i - 1] + processos[i - 1][1]

    # Calcular el tiempo promedio de espera
    tiempo_espera_promedio = sum(tiempo_espera) / n

    # Imprimir resultados con tiempo de ráfaga y tiempo de espera
    print("Proceso\tTiempo de Ráfaga\tTiempo de Espera")
    for i in range(n):
        print(f"{processos[i][0]}\t\t{processos[i][1]}\t\t{tiempo_espera[i]}")

    print(f"\nTiempo promedio de espera: {tiempo_espera_promedio:.2f}")

    # Crear el diagrama de Gantt
    diagrama_gantt(processos, tiempo_espera, "FCFS", tiempo_espera_promedio)

def sjf(processos):
    n = len(processos)
    # Ordenar los procesos por tiempo de ráfaga
    processos_ordenados = sorted(processos, key=lambda x: x[1])
    tiempo_espera = [0] * n

    # Calcular el tiempo de espera para cada proceso
    for i in range(1, n):
        tiempo_espera[i] = tiempo_espera[i - 1] + processos_ordenados[i - 1][1]

    # Calcular el tiempo promedio de espera
    tiempo_espera_promedio = sum(tiempo_espera) / n

    # Imprimir resultados con tiempo de ráfaga y tiempo de espera
    print("Proceso\tTiempo de Ráfaga\tTiempo de Espera")
    for i in range(n):
        print(f"{processos_ordenados[i][0]}\t\t{processos_ordenados[i][1]}\t\t{tiempo_espera[i]}")

    print(f"\nTiempo promedio de espera: {tiempo_espera_promedio:.2f}")

    # Crear el diagrama de Gantt
    diagrama_gantt(processos_ordenados, tiempo_espera, "SJF", tiempo_espera_promedio)

def diagrama_gantt(processos, tiempo_espera, titulo, tiempo_espera_promedio):
    fig, gnt = plt.subplots()

    # Configurar el eje y
    gnt.set_ylim(0, 1)
    gnt.set_xlim(0, sum(p[1] for p in processos))

    # Colores distintivos para cada proceso
    colores = plt.cm.get_cmap('tab10', len(processos))

    # Dibujar el diagrama de Gantt con etiquetas
    tiempo_actual = 0
    for i in range(len(processos)):
        nombre_proceso, tiempo_proceso = processos[i]
        gnt.broken_barh([(tiempo_actual, tiempo_proceso)], (0, 1), facecolors=[colores(i)], label=nombre_proceso)

        # Añadir etiquetas al centro de cada barra
        etiqueta_x = tiempo_actual + tiempo_proceso / 2
        etiqueta_y = 0.5
        gnt.text(etiqueta_x, etiqueta_y, nombre_proceso, ha='center', va='center', color='white', fontsize=8)

        tiempo_actual += tiempo_proceso

    # Agregar texto con el tiempo promedio de espera
    plt.text(0.5, -0.1, f'Tiempo promedio de espera: {tiempo_espera_promedio:.2f}', ha='center', va='center', transform=gnt.transAxes, fontsize=10)

    # Etiquetas y título
    gnt.set_xlabel('Tiempo')
    gnt.set_yticks([])
    gnt.set_title(f'Diagrama de Gantt - {titulo}')
    gnt.legend()

    plt.show()

def main():
    while True:
        print("\nMenú:")
        print("1. Planificación First-Come, First-Served (FCFS)")
        print("2. Planificación Shortest-Job-First (SJF)")
        print("3. Salir")

        opcion = input("Seleccione una opción (1/2/3): ")

        if opcion == '1':
            procesos = obtener_procesos()
            fcfs(procesos)
        elif opcion == '2':
            procesos = obtener_procesos()
            sjf(procesos)
        elif opcion == '3':
            break
        else:
            print("Opción no válida. Por favor, seleccione 1, 2 o 3.")

def obtener_procesos():
    procesos = []
    cantidad = int(input("Ingrese la cantidad de procesos: "))
    for i in range(1, cantidad + 1):
        tiempo_rafaga = int(input(f"Ingrese el tiempo de ráfaga para el proceso P{i}: "))
        procesos.append((f"P{i}", tiempo_rafaga))
    return procesos

if __name__ == "__main__":
    main()
