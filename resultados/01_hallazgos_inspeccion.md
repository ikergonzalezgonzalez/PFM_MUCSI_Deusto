# Hallazgos — Notebook 01: Inspección Inicial

**Proyecto Fin de Máster — MUCSI, Universidad de Deusto**  
**Notebook de referencia:** `notebooks/01_inspeccion_inicial.ipynb`  
**Datos de entrada:** `datos/raw/CLEAN_House{1,2,3}.csv`  
**Fecha de ejecución:** 2026-04-11

---

## Objetivo

Primer contacto con el dataset REFIT. Sin modificar ningún dato — solo lectura y análisis.  
Verificar estructura, integridad básica, rangos temporales y detectar problemas que requerirán
tratamiento en el Notebook 03.

---

## Estructura del dataset

Los tres CSVs tienen la misma estructura de columnas:

| Columna | Tipo | Descripción |
|---|---|---|
| `Time` | datetime | Timestamp de la medición (índice temporal) |
| `Unix` | int64 | Timestamp en formato Unix (no se usa en modelado) |
| `Aggregate` | float64 | Consumo total del hogar (W) — **variable objetivo** |
| `Appliance1`–`Appliance9` | float64 | Consumo de electrodomésticos individuales (W) |
| `Issues` | int64 | Flag de calidad: 0 = correcto, 1 = medición problemática |

---

## Estadísticas de los tres hogares

| Hogar | Inicio | Fin | Días | Registros | Intervalo med. | Consumo medio | Consumo máx |
|---|---|---|---|---|---|---|---|
| House1 | 2013-10-09 | 2015-07-10 | 638 | 6.960.008 | 7 s | 481,1 W | 29.159 W |
| House2 | 2013-09-17 | 2015-05-28 | 617 | 5.733.526 | 7 s | 465,1 W | 24.595 W |
| House3 | 2013-09-25 | 2015-06-02 | 614 | 6.994.594 | 7 s | 678,5 W | **65.836 W ⚠️** |

---

## Verificación de integridad

| Check | House1 | House2 | House3 |
|---|---|---|---|
| Valores nulos (NaN nativos) | 0 | 0 | 0 |
| Timestamps duplicados | 0 | 0 | 0 |
| Valores negativos en Aggregate | 0 | 0 | 0 |
| Registros con `Issues=1` | 58.183 (0,84%) | 28.444 (0,50%) | **408.627 (5,84%) ⚠️** |

El dataset REFIT no tiene NaN nativos ni duplicados — la calidad de la recolección es alta.  
Los problemas están encapsulados en la columna `Issues`.

---

## Hallazgos clave

### 1. Intervalo real de muestreo: 7 segundos (no 8 s)

La documentación oficial de REFIT declara una granularidad de 8 segundos. El análisis del
intervalo mediano real entre timestamps da **7 segundos** en los tres hogares. Este dato afecta
al factor de reducción esperado al remuestrear a 1 minuto (≈ 8,6× si fuera 7 s, ≈ 7,5× si fuera 8 s).

**Impacto:** el remuestreo a 1 minuto resuelve este problema automáticamente — la irregularidad
del intervalo desaparece al agregar por ventanas de 60 segundos.

---

### 2. House3: 5,84% de registros con Issues=1 ⚠️

House3 tiene una tasa de Issues=1 más de 7 veces superior a House1 y House2.  
Antes de decidir la estrategia de tratamiento, se analizó la distribución temporal
de estos issues para comprobar si están concentrados en períodos concretos.

**Resultado del análisis (Notebook 03):** los Issues=1 están distribuidos de forma
relativamente uniforme a lo largo de los ~614 días. No hay ningún mes donde superen
el 10% del total. Esto permitió aplicar la misma estrategia que para House1 y House2
(eliminación de filas individuales) en lugar de descartar períodos completos.

**Estrategia adoptada:** eliminación de filas con `Issues=1` en los tres hogares.  
Ver [cleaning.md](../cleaning.md) para justificación detallada.

---

### 3. House3: máximo de 65.836 W — outlier físicamente imposible ⚠️

El consumo máximo registrado en House3 es de 65.836 W, lo que equivale a casi
**tres veces el límite teórico máximo del suministro doméstico del Reino Unido**
(100A × 230V = 23.000 W). Este valor es claramente un artefacto de medición.

Para contexto, los máximos de House1 y House2 también superan el umbral físico razonable
para un hogar (29.159 W y 24.595 W respectivamente), aunque en menor medida.

**Estrategia adoptada:** umbral físico de 15.000 W para la columna `Aggregate`.  
Ver [cleaning.md](../cleaning.md) para justificación detallada.

---

### 4. House3: consumo medio más alto (678,5 W vs ~473 W de media en House1/House2)

House3 tiene un consumo medio significativamente más alto. Esto puede deberse a:
- Mayor superficie del hogar
- Más ocupantes
- Presencia de electrodomésticos de alto consumo (calefacción eléctrica, vehículo eléctrico, etc.)

**Implicación para el modelado:** los modelos entrenados en House3 no serán directamente
comparables en escala absoluta con los de House1 y House2. Las métricas deben interpretarse
en términos relativos (MAPE, R²) además de absolutos (RMSE, MAE).

---

## Decisiones derivadas de este análisis

| Decisión | Detalle | Estado |
|---|---|---|
| Tratamiento de Issues=1 | Eliminación de filas | Implementado en Notebook 03 |
| Tratamiento de outliers en Aggregate | Umbral físico 15.000 W → NaN | Implementado en Notebook 03 |
| Granularidad de trabajo | Remuestreo a 1 minuto por media | Implementado en Notebook 03 |
| Relleno de huecos cortos | Interpolación lineal, gaps ≤ 30 min | Implementado en Notebook 03 |

---

## Figuras generadas

| Figura | Descripción |
|---|---|
| `01_serie_aggregate_house1.png` | Serie temporal completa de Aggregate — House1 |
| `01_serie_aggregate_house2.png` | Serie temporal completa de Aggregate — House2 |
| `01_serie_aggregate_house3.png` | Serie temporal completa de Aggregate — House3 (outlier visible) |
| `01_distribucion_aggregate.png` | Distribución del consumo agregado (histograma + boxplot) |
| `01_issues_temporales.png` | Evolución temporal de Issues=1 en los tres hogares |
| `01_heatmap_nulos.png` | Mapa de presencia/ausencia de datos por electrodoméstico |
| `01_intervalo_muestreo.png` | Distribución del intervalo entre timestamps (~7 s) |
| `01_comparativa_hogares.png` | Comparativa de consumo medio entre los tres hogares |

## Métricas exportadas

| Archivo | Descripción |
|---|---|
| `metricas/01_resumen_inspeccion.csv` | Tabla resumen con estadísticas básicas de los tres hogares |

---

*Documento generado durante la Fase 1 del PFM — Minería de datos y EDA.*  
*Fecha: 2026-04-11*
