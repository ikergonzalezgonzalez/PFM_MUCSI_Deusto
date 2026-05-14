# PFM MUCSI Deusto — Datos del Proyecto (Resumen para presentación)

## Título
"Desarrollo de un modelo de aprendizaje automático para la predicción y optimización del consumo eléctrico en entornos domésticos inteligentes"

**Universidad:** Universidad de Deusto, Facultad de Ingeniería, Bilbao  
**Máster:** MUCSI — Computación y Sistemas Inteligentes  
**Tecnología:** Python 3.14 · pandas · numpy · scikit-learn · statsmodels · XGBoost · LightGBM · (LSTM en Fase 2)

---

## Dataset: REFIT Electrical Load Measurements
- **Fuente:** Zenodo doi:10.5281/zenodo.5063428 — datos reales de hogares del Reino Unido
- **Granularidad original:** ~7 segundos por lectura
- **Período:** ~2 años (oct 2013 – jul 2015)
- **Hogares usados:** House1, House2, House3 (trabajo principal) + 3 adicionales
- **Variables:** consumo total del hogar (Aggregate) + 9 electrodomésticos individuales

| Hogar | Registros raw | Período | Consumo medio | Max. detectado |
|---|---|---|---|---|
| House1 | 6.960.008 | Oct 2013 – Jul 2015 | 481 W | 29.159 W |
| House2 | 5.733.526 | Sep 2013 – May 2015 | 465 W | 24.595 W |
| House3 | 6.994.594 | Sep 2013 – Jun 2015 | 679 W | **65.836 W ⚠️** |

---

## Fases del proyecto

### FASE 1 — Minería de datos y EDA ✅ COMPLETADA
### FASE 2 — Modelado y comparativa 🔜 SIGUIENTE
### FASE 3 — Dashboard + Memoria LaTeX 🔜 PENDIENTE

---

## Lo que se ha hecho — Paso a paso

### Notebook 01 · Inspección inicial (11 abr 2026)
- Carga y exploración de los 3 hogares (sin modificar ningún dato)
- Descubrimientos clave:
  - Intervalo real: 7 s (no 8 s como indica la documentación)
  - Sin NaN nativos, sin duplicados — calidad de recolección alta
  - Issues=1: House1 0,84% · House2 0,50% · House3 **5,84% ⚠️**
  - Outlier severo en House3: 65.836 W (imposible físicamente — suministro máximo UK = 23.000 W)
- Salidas: 8 figuras + CSV de estadísticas

### Notebook 02 · EDA visual para tutora (11 abr 2026)
- Patrones temporales identificados en House1:
  - Pico matutino (07:00–09:00) + pico vespertino (18:00–21:00) todos los días
  - Fines de semana: pico desplazado +1h, más consumo sostenido durante el día
  - Estacionalidad anual clara: invierno +30% vs verano
- Salidas: 5 figuras de patrones + documento resumen para la tutora

### Notebook 03 · Limpieza de datos (17 abr 2026)
Pipeline en 4 pasos:

**Paso 1 — Eliminar Issues=1**
| Hogar | Eliminados | % |
|---|---|---|
| House1 | 58.183 | 0,84% |
| House2 | 28.444 | 0,50% |
| House3 | 408.627 | 5,84% |

**Paso 2 — Outliers Aggregate > 15.000 W → NaN**
- Umbral físico: suministro doméstico UK (100A × 230V = 23.000 W) → conservador en 15.000 W
- House3: 3.206 outliers eliminados (65.836 W → máx. 12.628 W)

**Paso 3 — Remuestreo: 7 s → 1 minuto (media)**
| Hogar | Filas raw | Filas 1 min | Reducción |
|---|---|---|---|
| House1 | 6.901.825 | 920.091 | 7,5× |
| House2 | 5.705.082 | 889.078 | 6,4× |
| House3 | 6.585.967 | 885.095 | 7,4× |

**Paso 4 — Imputación: gaps ≤ 30 min → interpolación lineal**
| Hogar | NaN antes | Imputados | % NaN final |
|---|---|---|---|
| House1 | 119.993 | 9.313 | **12,03%** |
| House2 | 219.633 | 8.989 | **23,69% ⚠️** |
| House3 | 136.345 | 26.339 | **12,43%** |

**Decisión:** House2 con 23,69% NaN → solo se usará para validación cruzada, NO para entrenamiento.

### Notebook 04 · EDA estadístico + Feature Engineering (26 abr 2026)

**Análisis estadísticos realizados:**
- Tests ADF y KPSS (estacionariedad) → pendiente ejecutar, resultados en CSV
- Descomposición estacional aditiva (período = 1440 min = 1 día)
  - Fuerza estacional F → calculada al ejecutar
  - Componente estacional diario claramente identificable
- ACF/PACF (36 horas, 2160 lags) → picos en lag 60 (1h), lag 1440 (1 día)
- Distribución: asimetría > 3, leptocúrtica — NO sigue distribución normal
- Correlaciones Pearson entre electrodomésticos y Aggregate

**Feature Engineering — 36 features en 5 grupos:**

| Grupo | Nº | Ejemplos |
|---|---|---|
| Temporales básicas | 9 | hora, dia_semana, mes, trimestre, estacion |
| Actividad binaria | 3 | es_finde, es_festivo_uk, estacion |
| Codificaciones cíclicas | 8 | hora_sin/cos, mes_sin/cos, dia_semana_sin/cos |
| Lags temporales | 8 | lag_1, lag_60, lag_1440, lag_10080 |
| Ventana deslizante | 8 | media_movil_60, std_movil_60, max_movil_60 |

---

## Decisiones técnicas clave

| Decisión | Por qué |
|---|---|
| Umbral outlier 15.000 W | Límite físico conservador del suministro doméstico UK |
| Remuestreo a 1 minuto | Estándar en literatura NILM; elimina irregularidad del intervalo |
| Imputar solo gaps ≤ 30 min | No fabricar datos en ausencias largas |
| House2 solo para validación | 23,69% NaN con concentración temporal |
| Codificación cíclica sin/cos | Evita discontinuidad en variables periódicas (hora 23 → hora 0) |
| lag_1440 como feature primaria | Confirmado pico diario en ACF |
| Semilla fija = 42 | Reproducibilidad total del proyecto |

---

## Siguiente paso: Fase 2 — Modelado

**Modelos planificados (en orden de complejidad):**
1. Baseline: media histórica + última observación conocida
2. ARIMA/SARIMA — modelo estadístico clásico de series temporales
3. XGBoost / LightGBM — Gradient Boosting con las 36 features
4. Random Forest
5. LSTM — red neuronal recurrente para secuencias temporales
6. (Opcional) Transformer

**Métricas de evaluación:** RMSE · MAE · MAPE · R²  
**Validación:** walk-forward temporal estricta (nunca aleatoria)

---

## Números clave del proyecto hasta ahora

- **~2,7M filas** de datos limpios a 1 minuto (3 hogares combinados)
- **~2 años** de mediciones por hogar
- **4 notebooks** completados
- **36 features** de ingeniería construidas
- **7 figuras** + **5 CSVs** de métricas en Notebook 04
- **4 documentos .md** de hallazgos para la memoria
