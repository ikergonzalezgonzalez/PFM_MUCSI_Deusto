# Hallazgos — Notebook 03: Limpieza de Datos

**Proyecto Fin de Máster — MUCSI, Universidad de Deusto**  
**Notebook de referencia:** `notebooks/03_limpieza_datos.ipynb`  
**Datos de entrada:** `datos/raw/CLEAN_House{1,2,3}.csv`  
**Datos de salida:** `datos/processed/house{1,2,3}_1min_limpio.csv`  
**Fecha de ejecución:** 2026-04-17

---

## Objetivo

Aplicar un pipeline sistemático de limpieza sobre los tres hogares de trabajo,
pasando de los CSVs originales a 7 s de granularidad a datasets limpios a 1 minuto
listos para el análisis estadístico y el modelado.

El pipeline sigue cuatro pasos ordenados:

1. Eliminación de registros con `Issues=1`
2. Detección y tratamiento de outliers en `Aggregate`
3. Remuestreo a 1 minuto (de los ~7 s originales)
4. Imputación de huecos cortos (gaps ≤ 30 min)

---

## Paso 1 — Eliminación de registros con Issues=1

### Justificación

El flag `Issues=1` indica que el sensor tuvo un problema en esa medición:
pérdida de comunicación, lectura inconsistente o valores faltantes en los
electrodomésticos individuales. Estos registros no son recuperables y deben eliminarse.

### Análisis previo de distribución temporal (House3)

Antes de decidir la estrategia para House3 (5,84% de Issues=1), se analizó si
los problemas estaban concentrados en períodos concretos o distribuidos uniformemente.

**Resultado:** los Issues=1 de House3 están distribuidos de forma relativamente uniforme
a lo largo de los 614 días del dataset. Ningún mes supera el ~10% de Issues=1.
Esto permite aplicar eliminación fila a fila en lugar de descartar períodos completos.

### Resultados

| Hogar | Registros originales | Eliminados (Issues=1) | % eliminado | Registros resultantes |
|---|---|---|---|---|
| House1 | 6.960.008 | 58.183 | 0,84% | 6.901.825 |
| House2 | 5.733.526 | 28.444 | 0,50% | 5.705.082 |
| House3 | 6.994.594 | **408.627** | **5,84%** | 6.585.967 |

### Figura generada

- `03_issues_temporales_house3.png` — Distribución mensual de Issues=1 en House3
  (cantidad y porcentaje). Confirma que no hay concentración anómala en ningún período.

---

## Paso 2 — Detección y tratamiento de outliers en Aggregate

### Justificación del umbral de 15.000 W

Se aplica un **umbral físico** basado en los límites reales del suministro eléctrico:

- Límite teórico máximo del suministro doméstico UK: 100A × 230V = **23.000 W**
- En la práctica, un hogar doméstico raramente supera 10.000–12.000 W de forma simultánea
- Un umbral de **15.000 W** es conservador: cubre todos los electrodomésticos de alto consumo
  (horno ~3 kW, caldera eléctrica ~6 kW, lavadora ~2 kW, lavavajillas ~2 kW, etc.)
- El máximo de House3 (65.836 W) equivale a casi **3× el límite teórico** del suministro
  doméstico — es físicamente imposible y constituye un artefacto de medición

Los valores superiores al umbral se convierten a **NaN** (no se eliminan las filas),
para ser gestionados junto con los huecos del remuestreo en el paso siguiente.

Solo se aplica el umbral a la columna `Aggregate`. Los electrodomésticos individuales
(Appliance1–Appliance9) tienen rangos propios mucho menores (máx. ~4.000 W) y sus
outliers, si los hubiere, se tratarán en el modelado.

### Resultados

| Hogar | Outliers detectados | % outliers | Máx. original | Máx. tras umbral |
|---|---|---|---|---|
| House1 | 0 | 0,0000% | 29.159 W | — (sin cambio) |
| House2 | 17 | 0,0003% | 24.595 W | < 15.000 W |
| House3 | 3.206 | **0,0487%** | **65.836 W** | < 15.000 W |

House1 no tiene outliers por encima del umbral de 15.000 W. House3 acumula el 99,8%
de todos los outliers detectados en el conjunto, coherente con el valor máximo
de 65.836 W identificado en la inspección inicial.

### Figura generada

- `03_outliers_histograma.png` — Histograma del consumo agregado (rango 0–20.000 W) con
  línea vertical en 15.000 W. Muestra la cantidad y porcentaje de outliers por hogar.

---

## Paso 3 — Remuestreo a 1 minuto

### Justificación

El dataset original tiene una granularidad nominal de 8 segundos (real: ~7 segundos).
El remuestreo a **1 minuto por media aritmética** ofrece:

- Eliminación automática de la irregularidad del intervalo (~7 s vs. 8 s)
- Reducción del volumen de datos ~7×: de ~7M filas a ~630K–920K por hogar
- Suavizado del ruido de alta frecuencia (que no aporta información predictiva)
- Granularidad de referencia en la literatura de NILM/predicción de carga eléctrica

Los minutos donde no existe ningún registro original quedan como `NaN` y son gestionados
en el Paso 4. El resampleo se aplica exclusivamente a las columnas de consumo
(`Aggregate` + `Appliance1`–`Appliance9`), descartando `Unix`, `Issues` y la columna
de identificador del hogar.

### Resultados

| Hogar | Filas (~7 s) | Filas (1 min) | Factor reducción | NaN en Aggregate | % NaN |
|---|---|---|---|---|---|
| House1 | 6.901.825 | 920.091 | 7,5× | 119.993 | 13,04% |
| House2 | 5.705.082 | 889.078 | 6,4× | 219.633 | 24,70% |
| House3 | 6.585.967 | 885.095 | 7,4× | 136.345 | 15,40% |

**Nota sobre House2:** el factor de reducción es 6,4× (inferior a los ~7,5× de los otros
hogares) porque House2 tiene más huecos reales en los datos originales, lo que reduce el
número de registros de partida sin reducir el número de minutos del período cubierto.

---

## Paso 4 — Imputación de huecos cortos (gaps ≤ 30 min)

### Justificación del umbral de imputación

Los `NaN` post-remuestreo tienen dos orígenes:
1. **Huecos en los datos originales** (cortes del sensor donde no hubo ninguna medición)
2. **Outliers reemplazados** en el Paso 2

La estrategia adoptada:
- **Gaps ≤ 30 minutos:** interpolación lineal entre los dos extremos conocidos del hueco.
  Estos huecos cortos (< 30 min) son razonablemente recuperables: la serie de consumo
  varía gradualmente y la interpolación lineal introduce un error aceptable.
- **Gaps > 30 minutos:** se mantienen como `NaN`. Fabricar datos durante ausencias largas
  introduciría sesgo artificial y podría confundir al modelo sobre patrones reales.

El umbral de 30 minutos es un criterio estándar conservador en la literatura de series
temporales de consumo eléctrico (e.g., Kelly & Knottenbelt, 2015 — dataset REFIT).

### Análisis de distribución de gaps

Antes de imputar, se analizó la distribución de longitudes de gap en cada hogar.
El histograma mostró que la mayoría de los gaps son cortos (1–15 minutos), lo que
confirma que el umbral de 30 minutos es adecuado: cubre la mayoría de los huecos
sin extenderse a ausencias largas.

### Resultados

| Hogar | NaN antes imputación | NaN imputados | NaN restantes | % NaN final |
|---|---|---|---|---|
| House1 | 119.993 | 9.313 | 110.680 | **12,03%** |
| House2 | 219.633 | 8.989 | 210.644 | **23,69%** ⚠️ |
| House3 | 136.345 | 26.339 | 110.006 | **12,43%** |

House3 es el hogar con más NaN imputados (26.339) porque tenía más outliers severos
reemplazados por NaN en el Paso 2 (3.206 valores), los cuales forman huecos cortos
que la interpolación lineal puede recuperar.

### Figura generada

- `03_distribucion_gaps.png` — Histograma de longitudes de gap (hasta 120 min) con
  línea vertical en 30 min (umbral de imputación) para los 3 hogares.

---

## Resumen comparativo antes/después

| Indicador | House1 | House2 | House3 |
|---|---|---|---|
| Filas originales (raw) | 6.960.008 | 5.733.526 | 6.994.594 |
| Filas finales (1 min) | 920.091 | 889.078 | 885.095 |
| Media original (W) | 481,1 | 465,1 | 678,5 |
| Media final (W) | 482,1 | 461,4 | 686,6 |
| Máximo original (W) | 29.159 | 24.595 | **65.836** |
| Máximo final (W) | 13.763 | 14.294 | 12.628 |
| % NaN final en Aggregate | 12,03% | **23,69%** ⚠️ | 12,43% |

Las medias se mantienen estables antes y después de la limpieza (diferencia < 1,5%),
lo que confirma que el pipeline no introduce sesgo sistemático en el nivel de consumo.

### Figura generada

- `03_comparativa_antes_despues.png` — Serie temporal de House3 (primeros 14 días)
  antes y después de la limpieza. Muestra la eliminación de outliers y la estabilización
  del rango de valores.

---

## Datos procesados guardados

| Archivo | Filas | Media (W) | Máx. (W) | % NaN |
|---|---|---|---|---|
| `datos/processed/house1_1min_limpio.csv` | 920.091 | 482,1 | 13.763 | 12,03% |
| `datos/processed/house2_1min_limpio.csv` | 889.078 | 461,4 | 14.294 | 23,69% ⚠️ |
| `datos/processed/house3_1min_limpio.csv` | 885.095 | 686,6 | 12.628 | 12,43% |

## Métricas exportadas

| Archivo | Descripción |
|---|---|
| `resultados/metricas/03_resumen_limpieza.csv` | Tabla comparativa antes/después por hogar |

---

## Alertas y decisiones para fases posteriores

### Alerta principal: House2 con 23,69% de NaN

House2 presenta una tasa de NaN casi el doble que House1 y House3. El análisis
temporal (Notebook 04) confirmó que estos NaN están concentrados en ciertos meses
de 2014, lo que indica cortes prolongados del sensor.

**Decisión adoptada (Notebook 04):** House2 no se usará como hogar de entrenamiento
primario en los modelos. Se reserva para validación cruzada externa
(*out-of-distribution testing*) en la Fase 2.

### Consideración para el modelado: propagación de NaN en lags

Los NaN residuales (12–24%) se propagarán al construir features de lag (lag_1440,
lag_10080). La estrategia en el Notebook 05 será eliminar los primeros N registros
correspondientes al lag más largo (lag_10080 = 7 días) antes de entrenar los modelos.

---

## Parámetros del pipeline (reproducibilidad)

| Parámetro | Valor | Justificación |
|---|---|---|
| `UMBRAL_OUTLIER_W` | 15.000 W | Umbral físico conservador para suministro doméstico UK |
| `UMBRAL_GAP_MIN` | 30 minutos | Límite de imputación lineal sin fabricar datos artificiales |
| Método de remuestreo | media aritmética | Preserva el nivel energético medio por minuto |
| Método de imputación | interpolación lineal | Adecuado para series continuas y gaps cortos |
| `SEMILLA` | 42 | Reproducibilidad global del proyecto |

---

## Síntesis para la memoria del PFM

### Qué incluir en el Capítulo de Preprocesado (Cap. 3 de la memoria)

Este notebook aporta material directo para:

1. **Sección: Tratamiento de outliers** — Justificación del umbral de 15.000 W con
   referencia al límite físico del suministro doméstico UK (100A × 230V = 23.000 W).
   Tabla de outliers detectados y eliminados por hogar.

2. **Sección: Remuestreo temporal** — Descripción del paso de ~7 s a 1 min.
   Tabla de factores de reducción. Citar la granularidad como estándar en la
   literatura de predicción de carga (Kelly & Knottenbelt, 2015).

3. **Sección: Tratamiento de valores ausentes** — Pipeline de dos niveles:
   interpolación lineal (gaps ≤ 30 min) y preservación de NaN largos.
   Tabla de NaN antes/después de imputación.

4. **Sección: Análisis de calidad post-limpieza** — Figura `03_comparativa_antes_despues.png`
   para mostrar el efecto visual del pipeline. Tabla resumen con medias y máximos finales.

5. **Alerta House2** — Documentar el 23,69% de NaN y la decisión de no usarlo
   en entrenamiento primario, con justificación estadística.

### Referencias bibliográficas sugeridas

- Kelly, J., & Knottenbelt, W. (2015). The UK-DALE dataset, domestic appliance-level
  electricity demand and whole-house demand from five UK homes. *Scientific Data*, 2, 150007.
- Makonin, S., & Popowich, F. (2015). Nonintrusive load monitoring (NILM) performance
  evaluation. *Energy Efficiency*, 8(4), 809–814.
- Moritz, S., & Bartz-Beielstein, T. (2017). imputeTS: Time series missing value
  imputation in R. *The R Journal*, 9(1), 207–218.

---

*Documento generado durante la Fase 1 del PFM — Minería de datos y EDA.*  
*Fecha: 2026-04-26*
