import os
import math
import random
import itertools
import matplotlib.pyplot as plt

SEMILLA = 42
random.seed(SEMILLA)


def calcular_distancia(punto_1, punto_2):
    return math.hypot(punto_1[0] - punto_2[0], punto_1[1] - punto_2[1])


def calcular_costo_tour(tour, ciudades):
    n = len(tour)
    return sum(calcular_distancia(ciudades[tour[i]], ciudades[tour[(i + 1) % n]]) for i in range(n))


def calcular_optimo_exacto(ciudades):
    n = len(ciudades)
    mejor_costo = float("inf")
    for permutacion in itertools.permutations(range(1, n)):
        costo_actual = calcular_costo_tour([0] + list(permutacion), ciudades)
        if costo_actual < mejor_costo:
            mejor_costo = costo_actual
    return mejor_costo


def aproximacion_mst(ciudades):
    n = len(ciudades)
    visitados = [0]
    por_visitar = list(range(1, n))
    lista_adyacencia = {i: [] for i in range(n)}

    # Algoritmo de Prim sencillo
    while por_visitar:
        mejor_u, mejor_v, distancia_minima = -1, -1, float("inf")
        for u in visitados:
            for v in por_visitar:
                d = calcular_distancia(ciudades[u], ciudades[v])
                if d < distancia_minima:
                    distancia_minima, mejor_u, mejor_v = d, u, v
        visitados.append(mejor_v)
        por_visitar.remove(mejor_v)
        lista_adyacencia[mejor_u].append(mejor_v)

    # Recorrido en Preorden (DFS)
    tour = []
    def dfs(nodo):
        tour.append(nodo)
        for hijo in lista_adyacencia[nodo]:
            dfs(hijo)

    dfs(0)
    return tour, calcular_costo_tour(tour, ciudades)


def busqueda_local_2opt(tour, ciudades):
    ruta = list(tour)
    n = len(ruta)
    hubo_mejora = True
    while hubo_mejora:
        hubo_mejora = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                nueva_ruta = ruta[:i] + ruta[i:j + 1][::-1] + ruta[j + 1:]
                if calcular_costo_tour(nueva_ruta, ciudades) < calcular_costo_tour(ruta, ciudades) - 1e-6:
                    ruta = nueva_ruta
                    hubo_mejora = True
    return ruta, calcular_costo_tour(ruta, ciudades)


def recocido_simulado_rapido(ciudades):
    n = len(ciudades)
    actual = list(range(n))
    random.shuffle(actual)
    mejor_costo = calcular_costo_tour(actual, ciudades)
    temperatura = 80.0
    for _ in range(400):
        i, j = sorted(random.sample(range(1, n), 2))
        vecino = actual[:i] + actual[i:j + 1][::-1] + actual[j + 1:]
        delta = calcular_costo_tour(vecino, ciudades) - calcular_costo_tour(actual, ciudades)
        if delta < 0 or random.random() < math.exp(-delta / max(temperatura, 0.01)):
            actual = vecino
            mejor_costo = min(mejor_costo, calcular_costo_tour(actual, ciudades))
        temperatura *= 0.98
    return mejor_costo


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    
    print("EJERCICIO 5: RAZON DE APROXIMACION MST (100 instancias N=9)")
    print("-" * 65)

    n_instancias = 100
    n_ciudades = 9

    razones_aproximacion = []
    costos_optimos, costos_mst, costos_mst_2opt, costos_2opt_aleatorio, costos_sa = [], [], [], [], []

    for _ in range(n_instancias):
        ciudades = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n_ciudades)]

        optimo = calcular_optimo_exacto(ciudades)
        tour_mst, costo_mst = aproximacion_mst(ciudades)
        _, costo_mst_2opt = busqueda_local_2opt(tour_mst, ciudades)

        tour_aleatorio = list(range(n_ciudades))
        random.shuffle(tour_aleatorio)
        _, costo_aleatorio_2opt = busqueda_local_2opt(tour_aleatorio, ciudades)
        
        costo_simulated = recocido_simulado_rapido(ciudades)

        costos_optimos.append(optimo)
        costos_mst.append(costo_mst)
        costos_mst_2opt.append(costo_mst_2opt)
        costos_2opt_aleatorio.append(costo_aleatorio_2opt)
        costos_sa.append(costo_simulated)
        razones_aproximacion.append(costo_mst / optimo)

    print(f"Razon promedio MST / Optimo: {sum(razones_aproximacion)/n_instancias:.4f} (Max: {max(razones_aproximacion):.4f})")
    print(f"Costo promedio Optimo    : {sum(costos_optimos)/n_instancias:.2f}")
    print(f"Costo promedio MST Puro  : {sum(costos_mst)/n_instancias:.2f}")
    print(f"Costo promedio MST + 2opt: {sum(costos_mst_2opt)/n_instancias:.2f}")

    # Grafica 1: Histograma de razon de aproximacion
    plt.figure(figsize=(7, 4.5))
    plt.hist(razones_aproximacion, bins=12, color="skyblue", edgecolor="black")
    plt.axvline(2.0, color="red", linestyle="--", label="Limite Teorico (2.0)")
    plt.title("Ejercicio 5: Razon de Aproximacion (C_obtenido / C_optimo)")
    plt.xlabel("Razon de Aproximacion")
    plt.ylabel("Frecuencia")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/ej5_mst_razon_aprox.png", dpi=300)
    plt.close()

    # Grafica 2: Comparativa de costos
    plt.figure(figsize=(9, 4.5))
    datos_boxplot = [costos_optimos, costos_mst, costos_mst_2opt, costos_2opt_aleatorio, costos_sa]
    nombres_etiquetas = ["Optimo", "MST Puro", "MST + 2-opt", "2-opt Aleat", "Sim. Annealing"]
    plt.boxplot(datos_boxplot, tick_labels=nombres_etiquetas, patch_artist=True)
    plt.title("Ejercicio 5: Comparacion de Costos en 100 Instancias (9 Ciudades)")
    plt.ylabel("Costo del Tour")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("figures/ej5_comparativa_global.png", dpi=300)
    plt.close()

    print("\n-> Graficas generadas exitosamente en:")
    print("   - figures/ej5_mst_razon_aprox.png")
    print("   - figures/ej5_comparativa_global.png")