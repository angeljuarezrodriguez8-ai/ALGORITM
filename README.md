# Proyecto de optimización y paralelismo

Estructura base para organizar los cinco ejercicios. Los scripts son plantillas: la implementación de los algoritmos y los experimentos queda pendiente.

## Estructura

```text
proyecto-optimizacion-paralelismo/
├── README.md
├── requirements.txt
├── ejecutar_todo.py
├── src/
│   ├── __init__.py
│   ├── ejercicio_1_pi_paralelo.py
│   ├── ejercicio_2_mochila_voraz.py
│   ├── ejercicio_3_busqueda_local_2opt.py
│   ├── ejercicio_4_recocido_simulado.py
│   └── ejercicio_5_aproximacion_mst.py
├── figuras/
│   ├── ejercicio_1_aceleracion.png
│   ├── ejercicio_2_comparacion_mochila.png
│   ├── ejercicio_3_comparacion_2opt.png
│   ├── ejercicio_4_convergencia_recocido.png
│   ├── ejercicio_4_tiempo_calidad.png
│   ├── ejercicio_5_razon_aproximacion_mst.png
│   └── ejercicio_5_comparacion_global.png
└── documentos/
    └── reporte_final.pdf
```

Las imágenes y el reporte se añadirán cuando realices los experimentos. `ejecutar_todo.py` será el punto de entrada para ejecutar los cinco ejercicios.
