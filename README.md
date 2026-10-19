# Laboratorio 9 – Visualización Estática del Turismo en Guatemala

**Universidad del Valle de Guatemala**  
Facultad de Ingeniería  
CC3084 – Data Science  
Semestre II – 2026

**Integrantes:**
- Osman de León
- Milton Polanco

## Descripción del proyecto

Este proyecto corresponde al Laboratorio 9 del curso Data Science. Su objetivo es transformar los resultados del análisis de series temporales desarrollado en el Laboratorio 1 en una infografía estática, profesional y comprensible para un público no técnico.

Se analiza el flujo de turistas y excursionistas hacia Guatemala durante el período comprendido entre enero de 2009 y junio de 2026, utilizando la base de datos migratorios proporcionada con fines académicos.

La infografía presenta el comportamiento histórico, los patrones estacionales, los principales mercados turísticos, los resultados del modelado predictivo y recomendaciones estratégicas dirigidas al Instituto Guatemalteco de Turismo (INGUAT).

## Objetivos

- Visualizar la evolución histórica del turismo en Guatemala.
- Identificar patrones de estacionalidad y eventos que afectan el flujo migratorio.
- Comparar el comportamiento de las principales series temporales.
- Presentar resultados de modelos predictivos mediante métricas de error.
- Visualizar estimaciones con intervalos de confianza.
- Formular recomendaciones estratégicas basadas en los resultados.
- Comunicar información estadística mediante una infografía de una sola página.

## Estructura del proyecto

```text
Laboratorio-9-Infografia/
│
├── data/
│   ├── raw/
│   │   └── Base_Migracion_2009-2026jun.xlsx
│   │
│   └── processed/
│       ├── serie_mensual_verificada.csv
│       └── pronostico_prueba_intervalo80.csv
│
├── notebooks/
│   ├── avance_lab9.ipynb
│   └── entrega_final_lab9.ipynb
│
├── scripts/
│   └── generar_entrega.py
│
├── reporte/
│   ├── avance_lab9.pdf
│   ├── infografia_corregida.png
│   ├── infografia_corregida.pdf
│   ├── NOTAS_VALIDACION.txt
│   └── figuras/
│
├── requirements.txt
├── README.md
└── .gitignore
```

*La estructura muestra los archivos principales. Pueden existir otros archivos generados durante el análisis.*

## Tecnologías utilizadas

El proyecto se desarrolla principalmente en Python y utiliza las siguientes bibliotecas:

| Biblioteca | Utilización |
|---|---|
| Pandas | Limpieza, transformación y agrupación de datos |
| NumPy | Operaciones numéricas |
| Matplotlib | Gráficas y visualización estática |
| Seaborn | Visualización estadística |
| Statsmodels | Modelos SARIMA y análisis de series temporales |
| Prophet | Modelado de tendencias y estacionalidad |
| Scikit-learn | Evaluación mediante MAE y RMSE |
| OpenPyXL | Lectura de archivos Excel |
| ReportLab | Exportación de la infografía a PDF |
| Jupyter | Desarrollo y ejecución de notebooks |

## Instalación y configuración

### 1. Clonar el repositorio

```bash
git https://github.com/MiltonPolanco/Laboratorio-9-Infografia.git
cd Laboratorio-9-Infografia
```

### 2. Crear un entorno virtual

Se recomienda utilizar Python 3.11.

```bash
python -m venv .venv
```

En Windows:

```powershell
.venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
python -m pip install -r requirements.txt
```

### 4. Preparar la base de datos

Colocar el archivo original:

`Base_Migracion_2009-2026jun.xlsx`

Dentro de:

`data/raw/`

El archivo debe conservar su estructura original y la hoja denominada `Datos`.

## Ejecución del análisis

Abrir Jupyter Notebook:

```bash
jupyter notebook
```

Ejecutar el archivo:

`notebooks/entrega_final_lab9.ipynb`

Seleccionar **Run All** para ejecutar todas las celdas.

El notebook está destinado al análisis exploratorio, la identificación de patrones temporales, la evaluación de modelos y la preparación de resultados para la infografía.

Se conserva `avance_lab9.ipynb` como evidencia del desarrollo previo.

## Generación de la infografía

Una vez preparado el entorno y ubicada la base de datos, ejecutar desde la raíz del proyecto:

```bash
python scripts/generar_entrega.py
```

El script realiza las siguientes operaciones:

1. Carga la base de datos migratorios.
2. Filtra los registros de turistas y excursionistas.
3. Construye la serie temporal mensual.
4. Calcula indicadores históricos y patrones estacionales.
5. Ajusta un modelo SARIMA de referencia.
6. Genera predicciones sobre el conjunto de prueba.
7. Calcula las métricas MAE y RMSE.
8. Obtiene intervalos predictivos nominales del 80 %.
9. Genera la infografía en formatos PNG y PDF.
10. Exporta los datos procesados y las notas de validación.

Los archivos generados se almacenan en las carpetas `data/processed/` y `reporte/`.

## Metodología de análisis

### Preparación de los datos

Se utilizan las categorías **Turista** y **Excursionista** para mantener una definición comparable del flujo turístico a lo largo del período estudiado.

Los registros se agrupan mensualmente, obteniendo una serie temporal con frecuencia de inicio de mes.

### Análisis histórico y estacional

Se estudian los cambios en el flujo de visitantes, prestando especial atención a:

- Crecimiento anterior a 2020.
- Impacto de la pandemia de COVID-19.
- Recuperación posterior a la reapertura de fronteras.
- Variaciones mensuales y períodos de alta demanda.
- Principales regiones y vías de ingreso.

### Modelado predictivo

El Laboratorio 1 evaluó distintas familias de modelos de series temporales, entre ellas SARIMA, Prophet, Holt-Winters, suavizamiento exponencial simple y Seasonal Naive.

Para la infografía reproducible se utiliza como referencia:

**SARIMA(1,1,1)(1,1,1,12)**

La validación implementada en el script utiliza:

| Parámetro | Configuración |
|---|---|
| Entrenamiento | Enero 2009 – diciembre 2023 |
| Prueba | Enero 2024 – junio 2026 |
| Modelo | SARIMA estacional |
| Métricas | MAE y RMSE |
| Intervalo predictivo | 80 % |

Las métricas de esta validación no deben compararse directamente con las del Laboratorio 1, porque utilizan diferentes períodos de entrenamiento y prueba.

La selección definitiva de un modelo ganador requiere evaluar todos los algoritmos bajo condiciones equivalentes.

## Contenido de la infografía

La visualización está organizada en cinco bloques temáticos.

### Bloque 1. Titular estratégico e indicadores

Presenta el contexto del turismo en Guatemala y los principales indicadores del conjunto de datos.

### Bloque 2. Panorama histórico

Muestra la evolución mensual del flujo turístico entre 2009 y 2026, destacando el impacto de la pandemia y la recuperación posterior.

### Bloque 3. Estacionalidad y mercados

Incluye el comportamiento estacional, la distribución por regiones y un cuadrante comparativo con hallazgos del Laboratorio 1.

### Bloque 4. Modelos y pronósticos

Presenta la estimación SARIMA sobre el conjunto de prueba, las observaciones reales y el intervalo predictivo del 80 %.

### Bloque 5. Recomendaciones para INGUAT

Se proponen acciones relacionadas con:

- Gestión de capacidad en fronteras terrestres.
- Promoción turística diferenciada por mercado.
- Preparación institucional ante interrupciones del turismo.
- Actualización periódica de pronósticos para apoyar decisiones.

## Archivos de salida

| Archivo | Descripción |
|---|---|
| `infografia_corregida.png` | Infografía digital de alta resolución |
| `infografia_corregida.pdf` | Infografía de una página, 11 × 17 pulgadas |
| `serie_mensual_verificada.csv` | Serie mensual reconstruida |
| `pronostico_prueba_intervalo80.csv` | Observaciones, estimaciones y límites predictivos |
| `NOTAS_VALIDACION.txt` | Resumen técnico y advertencias metodológicas |

## Decisiones de visualización

La infografía utiliza una distribución vertical que guía al lector desde el contexto histórico hasta las recomendaciones estratégicas.

Se emplea una paleta de colores sobria:

- **Azul oscuro (`#17354C`):** información principal, estructura y datos observados.
- **Turquesa (`#087E8B`):** indicadores y patrones históricos.
- **Naranja (`#EF9950`):** eventos relevantes, estimaciones e intervalos predictivos.

El contraste entre los colores permite diferenciar información histórica y estimada, evitando elementos decorativos innecesarios.

Los gráficos utilizan etiquetas, títulos descriptivos y escalas cuantitativas para facilitar su interpretación.

## Limitaciones

Los datos se proporcionan exclusivamente para fines académicos y no deben presentarse como estadísticas oficiales publicadas.

El análisis utiliza la información disponible hasta junio de 2026.

Los pronósticos son estimaciones estadísticas y no garantizan valores futuros.

Algunos hallazgos comparativos proceden del informe del Laboratorio 1 y requieren considerar su metodología original.

El modelo SARIMA utilizado en el script funciona como referencia reproducible y no constituye por sí solo evidencia de superioridad frente a todos los modelos alternativos.

## Entregables del laboratorio

El proyecto contempla:

- Infografía digital en formato PNG.
- Infografía de una página en formato PDF.
- Documento PDF de explicación de las decisiones de diseño.
- Notebook y script Python reproducibles.
- Repositorio con historial de versiones.
- Enlaces a los documentos colaborativos utilizados por el equipo.

## Autores

**Osman de León**  
**Milton Polanco**

Universidad del Valle de Guatemala  
CC3084 – Data Science  
Semestre II – 2026

## Uso de los datos

La base migratoria fue proporcionada con fines estrictamente académicos.

No se autoriza su publicación o redistribución abierta sin la autorización correspondiente.

**Fuente:** Base de Migración 2009–junio 2026, material académico asociado a INGUAT/IGM.
