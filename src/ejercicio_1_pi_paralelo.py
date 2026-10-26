import os
import time
import random
import multiprocessing as mp
import matplotlib.pyplot as plt


def contar_puntos(n):
    dentro = 0
    for _ in range(n):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            dentro += 1
    return dentro


def estimate_pi(total_muestras, num_procesos):
    inicio = time.time()
    muestras_por_proc = total_muestras // num_procesos

    if num_procesos == 1:
        total_dentro = contar_puntos(total_muestras)
    else:
        with mp.Pool(num_procesos) as pool:
            resultados = pool.map(contar_puntos, [muestras_por_proc] * num_procesos)
        total_dentro = sum(resultados)

    tiempo = time.time() - inicio
    pi_est = 4.0 * total_dentro / total_muestras
    return pi_est, tiempo


if __name__ == "__main__":
    os.makedirs("figures", exist_ok=True)
    procesos = [1, 2, 4, 8]
    tiempos = []
    speedups = []
    N = 10_000_000

    for p in procesos:
        pi_val, t = estimate_pi(N, p)
        tiempos.append(t)
        s = tiempos[0] / t
        speedups.append(s)
        print(f"Procesos: {p} | Pi: {pi_val:.5f} | Tiempo: {t:.3f}s | Speedup: {s:.2f}x")

    plt.plot(procesos, procesos, "--", label="Speedup Ideal")
    plt.plot(procesos, speedups, "-o", label="Speedup Real")
    plt.xlabel("Número de Procesos")
    plt.ylabel("Speedup")
    plt.title("Ejercicio 1: Speedup vs. Número de Procesos")
    plt.xticks(procesos)
    plt.grid(True)
    plt.legend()
    plt.savefig("figures/ej1_speedup.png")
    plt.close()