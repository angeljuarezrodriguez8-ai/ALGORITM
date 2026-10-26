import os
import time
import math
import random
import numpy as np
import matplotlib.pyplot as plt

SEMILLA = 42
random.seed(SEMILLA)
np.random.seed(SEMILLA)


def compute_distance_matrix(coords):
    """Calcula la matriz de distancias euclidianas entre todas las ciudades."""
    diff = coords[:, np.newaxis, :] - coords[np.newaxis, :, :]
    return np.sqrt(np.sum(diff ** 2, axis=-1))


def tour_cost(tour, dist_matrix):
    """Calcula el costo total cerrado de un recorrido TSP."""
    n = len(tour)
    return sum(dist_matrix[tour[i], tour[(i + 1) % n]] for i in range(n))


def simulated_annealing_tsp(dist_matrix, schedule="exponential", max_iter=6000, t_init=100.0, t_min=1e-3):
    """
    Implementa Recocido Simulado usando 2-opt sobre una solucion inicial aleatoria.
    Esquemas soportados: 'exponential', 'linear', 'logarithmic'
    """
    n = len(dist_matrix)
    current_tour = list(range(n))
    random.shuffle(current_tour)
    current_cost = tour_cost(current_tour, dist_matrix)

    best_tour = list(current_tour)
    best_cost = current_cost
    history_best = [best_cost]

    start_time = time.perf_counter()

    for k in range(1, max_iter + 1):
        if schedule == "exponential":
            alpha = (t_min / t_init) ** (1.0 / max_iter)
            temp = t_init * (alpha ** k)
        elif schedule == "linear":
            temp = max(t_min, t_init - k * ((t_init - t_min) / max_iter))
        elif schedule == "logarithmic":
            temp = t_init / (1.0 + 0.05 * math.log(1 + k))
        else:
            raise ValueError("Esquema desconocido.")

        i, j = sorted(random.sample(range(1, n), 2))
        if j - i == 1:
            history_best.append(best_cost)
            continue

        a, b = current_tour[i - 1], current_tour[i]
        c, d = current_tour[j], current_tour[(j + 1) % n]
        delta = (dist_matrix[a, c] + dist_matrix[b, d]) - (dist_matrix[a, b] + dist_matrix[c, d])

        # Criterio de aceptacion de Metropolis
        if delta < 0 or random.random() < math.exp(-delta / max(temp, 1e-12)):
            current_tour[i:j + 1] = reversed(current_tour[i:j + 1])
            current_cost += delta
            if current_cost < best_cost:
                best_cost = current_cost
                best_tour = list(current_tour)

        history_best.append(best_cost)

    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    return best_tour, best_cost, history_best, elapsed_ms


def main():
    os.makedirs("figures", exist_ok=True)
    plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3, "font.size": 11})

    print("EJERCICIO 4: AJUSTE DE PARAMETROS (SIMULATED ANNEALING)")
    print("-" * 60)

    n_cities = 30
    coords = np.random.uniform(0, 100, size=(n_cities, 2))
    dist_matrix = compute_distance_matrix(coords)

    schedules = [
        ("exponential", "Exponencial (T_k = T_0 * alpha^k)", "#2ecc71"),
        ("linear",      "Lineal (T_k = T_0 - beta * k)",     "#3498db"),
        ("logarithmic", "Logaritmico (T_k = T_0 / (1 + c*ln k))", "#e74c3c")
    ]

    max_iter = 6000
    n_trials = 20
    summary_stats = {}

    # Grafica 1: Curvas de convergencia
    plt.figure(figsize=(10, 5.5))

    for sched_key, sched_label, color in schedules:
        all_histories = []
        costs, times = [], []
        for _ in range(n_trials):
            _, b_cost, hist, elapsed = simulated_annealing_tsp(
                dist_matrix, schedule=sched_key, max_iter=max_iter
            )
            all_histories.append(hist)
            costs.append(b_cost)
            times.append(elapsed)

        mean_history = np.mean(all_histories, axis=0)
        summary_stats[sched_key] = (sched_label, color, costs, times)
        plt.plot(mean_history, label=sched_label, color=color, linewidth=2.2)

        print(f"Esquema {sched_key:12s} | Costo Final Prom: {np.mean(costs):6.2f} +/- {np.std(costs):5.2f} | "
              f"Tiempo Prom: {np.mean(times):5.2f} ms")

    plt.title("Ejercicio 4: Curvas de Convergencia Promedio por Esquema de Enfriamiento")
    plt.xlabel("Iteraciones")
    plt.ylabel("Mejor Costo del Recorrido TSP")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/ej4_sa_convergencia.png", dpi=300)
    plt.close()

    # Grafica 2: Tiempo de Ejecucion vs. Calidad de la Solucion Final
    plt.figure(figsize=(9, 5.5))
    for sched_key, (sched_label, color, costs, times) in summary_stats.items():
        plt.scatter(times, costs, color=color, alpha=0.65, s=60, label=sched_label)
        plt.scatter([np.mean(times)], [np.mean(costs)], color=color, edgecolor="black",
                    s=200, marker="X", zorder=5)

    plt.title("Ejercicio 4: Tiempo de Ejecucion vs. Calidad Final (Marcador 'X' = Media)")
    plt.xlabel("Tiempo de Ejecucion (ms)")
    plt.ylabel("Costo de la Solucion Final (Menor es mejor)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/ej4_sa_tiempo_calidad.png", dpi=300)
    plt.close()

    print("\n-> Graficas generadas exitosamente en:")
    print("   - figures/ej4_sa_convergencia.png")
    print("   - figures/ej4_sa_tiempo_calidad.png")


if __name__ == "__main__":
    main()