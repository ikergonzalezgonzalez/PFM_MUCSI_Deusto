# Hallazgos — Notebook 07: Baselines y estrategia de validación temporal

**Fecha:** 2026-05-12
**Notebook:** `notebooks/07_baseline_split_temporal.ipynb`
**Fase del proyecto:** 2 — Modelado y comparativa (apertura)

---

## 1. Reglas del juego de la Fase 2

| Parámetro | Valor | Justificación |
|-----------|-------|---------------|
| Estrategia de validación | Split cronológico 80/20 por hogar | Prohibido el split aleatorio en series temporales (fuga de información). |
| Walk-forward | Reservado para la evaluación final de modelos seleccionados (Fase 2.3) | Coste computacional alto; no se necesita para la comparativa entre modelos. |
| Horizontes evaluados (min) | 1, 15, 60, 1440 | Corto, medio y largo plazo (24 h cubre el ciclo diario dominante). |
| Umbral MAPE | y_real > 50 W | Evita la divergencia del MAPE en consumos nocturnos cercanos a 0. |
| Métricas reportadas | RMSE, MAE, MAPE (filtrado), R² | RMSE y MAE en watts (interpretable); R² para comparar entre hogares. |
| Hogares evaluados | 18 train + 2 validación externa (H2, H13) | Definidos en `06_seleccion_hogares_final.csv`. |

---

## 2. Baselines implementados

### 2.1. Persistencia (última observación conocida)
- Definición: ŷ_{t+h} = y_t.
- Implementación: `pd.Series.shift(h)` sobre el test.
- Las primeras `h` filas del test quedan como NaN (no se evalúan).

### 2.2. Media histórica por (hora, día de la semana)
- Definición: ŷ_{t+h} = media(y | hora(t+h), día_semana(t+h)) calculada sobre train.
- Implementación: `groupby(['hora','dia_semana']).mean()` → lookup contra el test.
- Para combinaciones no vistas en train se usa la media global.
- **Nota:** la predicción no depende del horizonte → la métrica es prácticamente constante.

---

## 3. Resultados — promedios sobre los 18 hogares de entrenamiento

| Horizonte | Modelo | RMSE (W) | MAE (W) | MAPE (%) | R² |
|-----------|--------|---------:|--------:|---------:|---:|
| 1 min | **Persistencia** | **297,24** | **72,77** | 10,98 | **0,74** |
| 1 min | Media hora-día | 604,13 | 341,58 | 89,01 | 0,04 |
| 15 min | Persistencia | 669,17 | 255,63 | 53,72 | −0,23 |
| 15 min | **Media hora-día** | **604,15** | **341,58** | 89,01 | 0,04 |
| 60 min | Persistencia | 763,00 | 322,62 | 72,94 | −0,57 |
| 60 min | **Media hora-día** | **604,17** | **341,60** | 89,02 | 0,04 |
| 1440 min | Persistencia | 772,01 | 335,97 | 79,76 | −0,62 |
| 1440 min | **Media hora-día** | **604,43** | **341,78** | 89,25 | 0,04 |

## 4. Resultados — validación externa (H2 + H13)

| Horizonte | Modelo | RMSE (W) | MAE (W) | MAPE (%) | R² |
|-----------|--------|---------:|--------:|---------:|---:|
| 1 min | **Persistencia** | **416,61** | **91,76** | 11,34 | **0,81** |
| 1 min | Media hora-día | 945,76 | 446,08 | 99,10 | 0,06 |
| 1440 min | Persistencia | 1185,78 | 506,88 | 122,20 | −0,45 |
| 1440 min | **Media hora-día** | **944,14** | **443,82** | 98,03 | 0,06 |

---

## 5. Conclusiones y umbrales para Fase 2

1. **Horizonte corto (1 min):** la persistencia es un rival muy fuerte (RMSE=297 W, R²=0,74). Coherente con el EDA del Notebook 04, que mostró lag_1 con r > 0,95 contra Aggregate. Cualquier modelo que no la supere en este horizonte no aporta valor.

2. **Horizonte medio-largo (≥15 min):** la persistencia colapsa a R² negativo (es peor que predecir la media global). A partir de aquí, los modelos deben capturar el patrón circadiano y la dinámica intradiaria.

3. **La media hora-día es plana en RMSE (~604 W) para todos los horizontes:** establece el suelo absoluto que cualquier modelo debe batir en todos los plazos.

4. **R² más alto en validación externa que en train a horizonte 1 min** (0,81 vs 0,74): H2 y H13 son hogares con consumo menos volátil, por lo que la persistencia los predice relativamente mejor. No es síntoma de fuga de información — el modelo no se entrena en train, solo se calculan métricas.

### Umbrales que cualquier modelo de Fase 2 debe batir

| Horizonte | RMSE máximo aceptable (W) | MAE máximo aceptable (W) | R² mínimo esperable |
|-----------|---------------------------:|--------------------------:|---------------------:|
| 1 min | < 297 | < 73 | > 0,74 |
| 15 min | < 604 | < 342 | > 0,04 |
| 60 min | < 604 | < 342 | > 0,04 |
| 1440 min | < 604 | < 342 | > 0,04 |

---

## 6. Siguiente paso — Notebook 08

Entrenar el primer modelo clásico — **Random Forest con el catálogo de 36 features (Nb04 y Nb06)** — manteniendo el mismo split cronológico 80/20 y comparando con `07_baseline.csv` en los cuatro horizontes.

## 7. Artefactos generados

- `resultados/metricas/07_baseline.csv` — 160 filas (20 hogares × 4 horizontes × 2 modelos).
- `resultados/metricas/07_baseline_resumen.csv` — agregados por rol/horizonte/modelo.
- `resultados/figuras/07_rmse_baselines_por_horizonte.png`
- `resultados/figuras/07_mae_persistencia_heatmap.png`
- `resultados/figuras/07_ejemplo_prediccion_house1.png`
