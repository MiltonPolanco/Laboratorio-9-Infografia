# Laboratorio 9 Visualización estática

Avance del documento de explicación para la infografía sobre el flujo migratorio y turístico de Guatemala entre enero de 2009 y junio de 2026.

## Integrantes

- Milton Polanco
- Osman de León

## Estructura

- `data/raw/`: base original de migración utilizada en el Laboratorio 1.
- `data/processed/`: indicadores y tablas resumidas producidas por el notebook.
- `notebooks/`: notebook principal ejecutado del avance.
- `reporte/figuras/`: prototipos gráficos generados desde el notebook.
- `reporte/avance_lab9.tex`: fuente editable del documento de explicación.
- `reporte/avance_lab9.pdf`: avance compilado desde LaTeX.

## Ejecución

1. Crear un entorno virtual de Python.
2. Instalar las dependencias con `pip install -r requirements.txt`.
3. Ejecutar `notebooks/avance_lab9.ipynb` de principio a fin.

El notebook parte de la base original, filtra `Turista` y `Excursionista`, construye las series mensuales, calcula los indicadores y genera las figuras. La infografía final de una página queda pendiente para la entrega final.

## Fuente

Base de Migración 2009-2026, INGUAT e Instituto Guatemalteco de Migración. El archivo se utiliza exclusivamente con fines académicos.

