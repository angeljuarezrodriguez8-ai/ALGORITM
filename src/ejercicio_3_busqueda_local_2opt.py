import os
import random
import numpy as np
import matplotlib.pyplot as plt

SEMILLA = 42
random.seed(SEMILLA)
np.random.seed(SEMILLA)


def calcular_matriz_distancias(coordenadas):
    """Calcula la matriz de distancias euclidianas entre todas las ciudades."""
    diff = coordenadas[:, np.newaxis, :] - coordenadas[np.newaxis, :, :]
    return np.sqrt(np.sum(diff ** 2, axis=-1))


def calcular_costo_recorrido(recorrido, matriz_distancias):
    """Calcula el costo total cerrado de un recorrido TSP."""
    n = len(recorrido)
    return sum(matriz_distancias[recorrido[i], recorrido[(i + 1) % n]] for i in range(n))


def recorrido_vecino_mas_cercano(matriz_distancias, nodo_inicio=None):
    """Construye una solucion inicial usando la heuristica del Vecino Mas Cercano."""
    n = len(matriz_distancias)
    if nodo_inicio is None:
        nodo_inicio = random.randrange(n)
    ciudades_no_visitadas = set(range(n))
    ciudades_no_visitadas.remove(nodo_inicio)
    recorrido = [nodo_inicio]
    nodo_actual = nodo_inicio

    while ciudades_no_visitadas:
        siguiente_ciudad = min(ciudades_no_visitadas, key=lambda ciudad: matriz_distancias[nodo_actual, ciudad])
        recorrido.append(siguiente_ciudad)
        ciudades_no_visitadas.remove(siguiente_ciudad)
        nodo_actual = siguiente_ciudad
    return recorrido


def busqueda_local_2opt(recorrido_inicial, matriz_distancias):
    """
    Aplica busqueda local 2-opt hasta alcanzar un optimo local.
    Retorna: (mejor_recorrido, mejor_costo, numero_de_mejoras)
    """
    n = len(recorrido_inicial)
    mejor_recorrido = list(recorrido_inicial)
    mejor_costo = calcular_costo_recorrido(mejor_recorrido, matriz_distancias)
    total_mejoras = 0
    hubo_mejora = True

    while hubo_mejora:
        hubo_mejora = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                if j - i == 1:
                    continue
                a, b = mejor_recorrido[i - 1], mejor_recorrido[i]
                c, d = mejor_recorrido[j], mejor_recorrido[(j + 1) % n]
                aristas_actuales = matriz_distancias[a, b] + matriz_distancias[c, d]
                nuevas_aristas = matriz_distancias[a, c] + matriz_distancias[b, d]

                if nuevas_aristas < aristas_actuales - 1e-9:
                    mejor_recorrido[i:j + 1] = reversed(mejor_recorrido[i:j + 1])
                    mejor_costo += (nuevas_aristas - aristas_actuales)
                    total_mejoras += 1
                    hubo_mejora = True
    return mejor_recorrido, mejor_costo, total_mejoras


def main():
    os.makedirs("figures", exist_ok=True)
    plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3, "font.size": 11})

    print("EJERCICIO 3: BUSQUEDA LOCAL (2-opt: Aleatorio vs. Vecino Mas Cercano)")
    print("-" * 65)

    cantidad_ciudades = 30
    total_ejecuciones = 30
    coordenadas_ciudades = np.random.uniform(0, 100, size=(cantidad_ciudades, 2))
    matriz_distancias = calcular_matriz_distancias(coordenadas_ciudades)

    mejoras_aleatorio, costos_aleatorio = [], []
    mejoras_vecino, costos_vecino = [], []

    for _ in range(total_ejecuciones):
        # Escenario 1: Solucion inicial aleatoria
        recorrido_aleatorio_inicial = list(range(cantidad_ciudades))
        random.shuffle(recorrido_aleatorio_inicial)
        _, costo_rand, mejoras_rand = busqueda_local_2opt(recorrido_aleatorio_inicial, matriz_distancias)
        mejoras_aleatorio.append(mejoras_rand)
        costos_aleatorio.append(costo_rand)

        # Escenario 2: Solucion inicial con Vecino Mas Cercano (nodo inicial aleatorio)
        nodo_inicio_aleatorio = random.randrange(cantidad_ciudades)
        recorrido_vecino_inicial = recorrido_vecino_mas_cercano(matriz_distancias, nodo_inicio=nodo_inicio_aleatorio)
        _, costo_nn, mejoras_nn = busqueda_local_2opt(recorrido_vecino_inicial, matriz_distancias)
        mejoras_vecino.append(mejoras_nn)
        costos_vecino.append(costo_nn)

    print(f"Resultados sobre {total_ejecuciones} ejecuciones ({cantidad_ciudades} ciudades):\n")
    print(f"[Inicio Aleatorio + 2-opt]")
    print(f"  - Mejoras promedio : {np.mean(mejoras_aleatorio):6.2f} +/- {np.std(mejoras_aleatorio):5.2f}")
    print(f"  - Costo promedio   : {np.mean(costos_aleatorio):6.2f} +/- {np.std(costos_aleatorio):5.2f}\n")

    print(f"[Vecino Mas Cercano + 2-opt]")
    print(f"  - Mejoras promedio : {np.mean(mejoras_vecino):6.2f} +/- {np.std(mejoras_vecino):5.2f}")
    print(f"  - Costo promedio   : {np.mean(costos_vecino):6.2f} +/- {np.std(costos_vecino):5.2f}")

    # Generacion de diagramas de caja
    fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
    etiquetas_grafica = ["Inicio Aleatorio\n+ 2-opt", "Vecino Mas Cercano\n+ 2-opt"]

    bplot1 = axes[0].boxplot([mejoras_aleatorio, mejoras_vecino], tick_labels=etiquetas_grafica,
                             patch_artist=True, widths=0.45)
    axes[0].set_title("Numero de Mejoras (Swaps 2-opt) hasta Converger")
    axes[0].set_ylabel("Cantidad de Mejoras Realizadas")

    bplot2 = axes[1].boxplot([costos_aleatorio, costos_vecino], tick_labels=etiquetas_grafica,
                             patch_artist=True, widths=0.45)
    axes[1].set_title("Calidad del Optimo Local Alcanzado (Costo)")
    axes[1].set_ylabel("Distancia Euclidiana Total")

    colores_cajas = ["#ff9999", "#66b3ff"]
    for bplot in (bplot1, bplot2):
        for patch, color in zip(bplot["boxes"], colores_cajas):
            patch.set_facecolor(color)

    plt.suptitle("Ejercicio 3: Comparacion de Convergencia y Calidad en Busqueda Local 2-opt",
                 fontweight="bold")
    plt.tight_layout()
    plt.savefig("figures/ej3_2opt_comparacion.png", dpi=300)
    plt.close()
    print("\n-> Grafica generada exitosamente en: figures/ej3_2opt_comparacion.png")


if __name__ == "__main__":
    main()