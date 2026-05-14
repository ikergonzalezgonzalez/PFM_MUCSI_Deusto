# Hallazgos — Notebook 02: EDA Visual (Presentación a la Tutora)

**Proyecto Fin de Máster — MUCSI, Universidad de Deusto**  
**Notebook de referencia:** `notebooks/02_presentacion_tutora.ipynb`  
**Datos de entrada:** `datos/raw/CLEAN_House1.csv` (remuestreado a 1 minuto en memoria, sin limpiar)  
**Fecha de ejecución:** 2026-04-11

---

## Objetivo

Análisis exploratorio visual de House1 para preparar la presentación a la tutora.  
**No se aplica ninguna limpieza** — el objetivo es visualizar los patrones del consumo real
antes de cualquier procesamiento, para tomar decisiones informadas sobre el pipeline de limpieza.

> Solo se usa House1 en este notebook porque es el hogar con menor tasa de Issues=1 (0,84%)
> y por tanto el más representativo del comportamiento real sin artefactos.

---

## Estadísticas descriptivas — House1 a 1 minuto (sin limpiar)

| Estadístico | Consumo agregado (W) |
|---|---|
| Media | 477,8 W |
| Desviación estándar | 765,7 W |
| Mínimo | 87,3 W |
| Percentil 25 | 186,2 W |
| **Mediana (p50)** | **245,5 W** |
| Percentil 75 | 447,9 W |
| Percentil 99 | 3.351,2 W |
| Máximo | 23.969,6 W |

### Interpretación de la distribución

La diferencia entre la media (477,8 W) y la mediana (245,5 W) indica una **distribución
fuertemente asimétrica hacia la derecha**: la mayor parte del tiempo el hogar consume
alrededor de 245 W, pero hay episodios de alto consumo (cocina, calentador de agua, lavadora)
que elevan la media considerablemente.

La desviación estándar (765,7 W) es mayor que la media, lo que confirma la alta variabilidad.
El P99 de 3.351 W indica que solo en el 1% del tiempo el consumo supera los ~3,4 kW, aunque el
máximo absoluto llega a casi 24 kW (outlier que se eliminará en la limpieza).

**Implicación para el modelado:** dado que el consumo no sigue una distribución normal,
los modelos de ML que asumen normalidad (e.g., regresión lineal simple) deberán usarse
con cautela. XGBoost, LightGBM y LSTM son más adecuados para distribuciones asimétricas.

---

## Patrones temporales identificados

### Perfil diario (laborable vs. fin de semana)

Se observan dos picos de consumo en los días laborables:
- **Pico matutino:** en torno a las 07:00–08:00 h (inicio de actividad del hogar)
- **Pico vespertino:** en torno a las 18:00–21:00 h (regreso al hogar + preparación de cena)

Los fines de semana presentan:
- Pico matutino desplazado una hora más tarde (~09:00 h)
- Mayor consumo sostenido a lo largo del día (más horas de ocupación)
- Diferencia estadísticamente significativa respecto a los días laborables

**Implicación:** la variable `es_finde` (indicador de fin de semana) será una feature predictora
relevante en todos los modelos basados en features de ingeniería.

---

### Patrón semanal

El consumo medio varía a lo largo de la semana:
- Los días de lunes a viernes presentan una media similar entre sí
- El sábado y el domingo tienen medias superiores a los días laborables
- Los intervalos de confianza al 95% entre días laborables se solapan
  (no hay diferencias significativas entre un lunes y un viernes)

**Implicación:** el día de la semana como variable numérica (0–6) o como one-hot encoding
aportará información al modelo, especialmente para distinguir fin de semana de días laborables.

---

### Estacionalidad mensual

Se observa una clara variación estacional:
- **Invierno (dic–feb):** consumo más alto — calefacción y más horas de oscuridad
- **Verano (jun–ago):** consumo más bajo — sin calefacción
- El patrón es coherente con el clima del Reino Unido (latitud ~53°N)

Con ~2 años de datos, hay dos ciclos completos invierno–verano disponibles, lo que es
suficiente para que los modelos capturen la estacionalidad anual.

**Implicación:** la variable `mes` o mejor aún una codificación cíclica (`sin(2π·mes/12)`,
`cos(2π·mes/12)`) será importante en el feature engineering.

---

### Heatmap hora × día de la semana (semana típica)

El heatmap de consumo medio por hora y día de la semana muestra:
- Las horas 00:00–06:00 tienen consumo mínimo (hogar en reposo) todos los días
- Los picos vespertinos de lunes a viernes son más pronunciados que los de fin de semana
- El sábado por la mañana (09:00–12:00) destaca como período de alto consumo relativo

Este patrón bidimensional justifica el uso de **features de interacción** entre hora y día
de la semana en lugar de tratarlos como variables independientes.

---

## Implicaciones para el Notebook 04 (Feature Engineering)

| Feature | Tipo | Justificación |
|---|---|---|
| `hora` | Numérica / cíclica sin/cos | Captura el ciclo diario |
| `dia_semana` | Categórica (0–6) | Distingue laborables de fin de semana |
| `es_finde` | Binaria | Diferencia de patrón laborable/fin de semana |
| `mes` | Numérica / cíclica sin/cos | Captura estacionalidad anual |
| `estacion` | Categórica (4 valores) | Proxy de estacionalidad con menos cardinalidad |
| `es_festivo_UK` | Binaria | Los festivos se comportan como fines de semana |
| Lags (t-1, t-5, t-30, t-60) | Numérica | El consumo tiene autocorrelación fuerte a corto plazo |
| Media móvil (15, 30, 60 min) | Numérica | Captura tendencia local / inertia del consumo |

---

## Limitaciones de este análisis

1. **Solo House1:** los patrones observados pueden no generalizarse directamente a House2 y House3,
   que tienen diferentes perfiles de consumo y calidad de datos.

2. **Sin limpieza aplicada:** los outliers (máx. 23.969 W) distorsionan ligeramente las estadísticas.
   Las medias reales tras la limpieza serán marginalmente diferentes (ver Notebook 03).

3. **Datos sin remuestrear definitivo:** el remuestreo a 1 minuto aquí es provisional (en memoria),
   no el dataset limpio definitivo de `datos/processed/`.

---

## Figuras generadas

| Figura | Descripción |
|---|---|
| `02_serie_temporal_completa.png` | Serie temporal House1 (2 años) con media móvil de 30 días |
| `02_patron_diario_horas.png` | Perfil horario (laborable vs. fin de semana) con banda ±1σ |
| `02_patron_semanal.png` | Consumo medio por día de la semana con IC al 95% |
| `02_estacionalidad_mensual.png` | Consumo medio mensual con paleta estacional invierno–verano |
| `02_heatmap_semana_tipica.png` | Heatmap de consumo medio por hora × día de la semana |

## Métricas exportadas

| Archivo | Descripción |
|---|---|
| `metricas/02_estadisticas_house1_1min.csv` | Estadísticas descriptivas de House1 a 1 minuto |

---

*Documento generado durante la Fase 1 del PFM — Minería de datos y EDA.*  
*Fecha: 2026-04-11*
