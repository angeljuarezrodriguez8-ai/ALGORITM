import os
import matplotlib.pyplot as plt


def greedy_knapsack(lista_objetos, capacidad_maxima, criterio_seleccion="ratio"):
    
    if criterio_seleccion == "min_weight":
        objetos_ordenados = sorted(lista_objetos, key=lambda x: (x["weight"], -x["value"]))
    elif criterio_seleccion == "ratio":
        objetos_ordenados = sorted(lista_objetos, key=lambda x: x["value"] / x["weight"], reverse=True)
    else:
        raise ValueError("Modo no valido. Usa 'min_weight' o 'ratio'.")

    objetos_seleccionados = []
    peso_acumulado = 0
    valor_acumulado = 0

    for item in objetos_ordenados:
        if peso_acumulado + item["weight"] <= capacidad_maxima:
            objetos_seleccionados.append(item["id"])
            peso_acumulado += item["weight"]
            valor_acumulado += item["value"]

    return objetos_seleccionados, peso_acumulado, valor_acumulado


def main():
    os.makedirs("figures", exist_ok=True)
    plt.rcParams.update({"axes.grid": True, "grid.alpha": 0.3, "font.size": 11})

    print("EJERCICIO 2: ANALISIS ALGORITMICO (GREEDY KNAPSACK)")
    print("-" * 55)

    # Instancia donde el criterio de 'Menor Peso' obtiene un resultado mucho peor
    capacidad_maxima = 10
    lista_objetos = [
        {"id": "Obj_A (Chatarra)", "weight": 2, "value": 3},   # Ratio = 1.50
        {"id": "Obj_B (Cobre)",    "weight": 3, "value": 4},   # Ratio = 1.33
        {"id": "Obj_C (Plata)",    "weight": 4, "value": 5},   # Ratio = 1.25
        {"id": "Obj_D (Oro Puro)", "weight": 9, "value": 90},  # Ratio = 10.00
    ]

    seleccion_peso, peso_usado_peso, valor_total_peso = greedy_knapsack(lista_objetos, capacidad_maxima, criterio_seleccion="min_weight")
    seleccion_ratio, peso_usado_ratio, valor_total_ratio = greedy_knapsack(lista_objetos, capacidad_maxima, criterio_seleccion="ratio")

    # Convertimos las listas a texto limpio sin corchetes
    texto_objetos_peso = ", ".join(seleccion_peso)
    texto_objetos_ratio = ", ".join(seleccion_ratio)

    print(f"Capacidad maxima de la mochila: {capacidad_maxima} kg\n")
    print(f"Criterio: Menor Peso Primero")
    print(f"  - Objetos seleccionados : {texto_objetos_peso}")
    print(f"  - Capacidad utilizada   : {peso_usado_peso} / {capacidad_maxima} kg")
    print(f"  - Valor total obtenido  : ${valor_total_peso}\n")

    print(f"Criterio: Mayor Valor/Peso")
    print(f"  - Objetos seleccionados : {texto_objetos_ratio}")
    print(f"  - Capacidad utilizada   : {peso_usado_ratio} / {capacidad_maxima} kg")
    print(f"  - Valor total obtenido  : ${valor_total_ratio}")

    # Generacion de la grafica comparativa
    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    etiquetas_metodos = ["Voraz: Menor Peso", "Voraz: Valor / Peso"]

    # Subgrafica 1: Valor Total
    bars_valor = axes[0].bar(etiquetas_metodos, [valor_total_peso, valor_total_ratio], color=["#e74c3c", "#2ecc71"],
                            width=0.5, edgecolor="black")
    axes[0].set_title("Valor Total Obtenido ($)")
    axes[0].set_ylabel("Valor Acumulado")
    axes[0].set_ylim(0, max(valor_total_peso, valor_total_ratio) * 1.2)
    for bar in bars_valor:
        yval = bar.get_height()
        axes[0].text(bar.get_x() + bar.get_width() / 2, yval + 2, f"${yval}",
                     ha="center", fontweight="bold")

    # Subgrafica 2: Capacidad Utilizada
    bars_capacidad = axes[1].bar(etiquetas_metodos, [peso_usado_peso, peso_usado_ratio], color=["#3498db", "#9b59b6"],
                            width=0.5, edgecolor="black")
    axes[1].axhline(capacidad_maxima, color="black", linestyle="--",
                    label=f"Capacidad Maxima ({capacidad_maxima} kg)")
    axes[1].set_title("Capacidad de Mochila Utilizada (kg)")
    axes[1].set_ylabel("Peso (kg)")
    axes[1].set_ylim(0, capacidad_maxima * 1.25)
    axes[1].legend()
    for bar in bars_capacidad:
        yval = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width() / 2, yval + 0.3, f"{yval} kg",
                     ha="center", fontweight="bold")

    plt.suptitle("Ejercicio 2: Comparacion de Criterios Voraces en la Mochila",
                 fontweight="bold")
    plt.tight_layout()
    plt.savefig("figures/ej2_knapsack_comparacion.png", dpi=300)
    plt.close()
    print("\n-> Grafica generada exitosamente en: figures/ej2_knapsack_comparacion.png")


if __name__ == "__main__":
    main()