# Hallazgos — Notebook 08: Random Forest con catálogo de features

**Fecha:** 2026-05-12
**Notebook:** `notebooks/08_random_forest.ipynb`
**Fase del proyecto:** 2 — Modelado y comparativa (primer modelo clásico)

---

## 1. Configuración del experimento

| Parámetro | Valor |
|-----------|-------|
| Granularidad temporal | 15 min (resampling con media desde 1 min) |
| Horizontes evaluados (min) | 15, 60, 1440 (descartado el de 1 min: dominado por persistencia) |
| Features | 22 (5 temporales + 1 binaria + 8 cíclicas + 4 lags + 4 rolling) |
| Hiperparámetros | n_estimators=100, max_depth=15, min_samples_leaf=5, random_state=42 |
| Split | 80/20 cronológico por hogar (idéntico al Nb07) |
| Estrategias comparadas | RF por hogar (18 modelos × 3 horizontes) y RF global con `id_hogar` (3 modelos) |

---

## 2. Resultados — promedios sobre los 18 hogares de entrenamiento

| Horizonte | Estrategia | RMSE (W) | MAE (W) | MAPE (%) | R² |
|-----------|------------|---------:|--------:|---------:|---:|
| 15 min | baseline media hora-día | 604,15 | 341,58 | 89,01 | 0,04 |
| 15 min | baseline persistencia | 669,17 | 255,63 | 53,72 | −0,23 |
| 15 min | **RF global** | **424,66** | 226,08 | 50,74 | **0,32** |
| 15 min | RF por hogar | 422,41 | 232,61 | 53,95 | 0,31 |
| 60 min | baseline media hora-día | 604,17 | 341,60 | 89,02 | 0,04 |
| 60 min | **RF global** | **459,14** | 258,68 | 61,23 | **0,22** |
| 60 min | RF por hogar | 460,66 | 267,82 | 65,26 | 0,20 |
| 1440 min | baseline media hora-día | 604,43 | 341,78 | 89,25 | 0,04 |
| 1440 min | **RF global** | **473,95** | 266,28 | 64,40 | **0,19** |
| 1440 min | RF por hogar | 492,96 | 292,78 | 74,35 | 0,09 |

## 3. Resultados — validación externa (H2 + H13)

| Horizonte | Estrategia | RMSE (W) | MAE (W) | MAPE (%) | R² |
|-----------|------------|---------:|--------:|---------:|---:|
| 15 min | baseline media hora-día | 945,72 | 446,01 | 99,08 | 0,06 |
| 15 min | **RF global** | **661,75** | 350,73 | 86,00 | **0,38** |
| 15 min | RF por hogar | 682,42 | 351,28 | 73,69 | 0,35 |
| 60 min | **RF global** | **732,32** | 411,55 | 108,33 | **0,25** |
| 60 min | RF por hogar | 759,90 | 392,61 | 86,56 | 0,19 |
| 1440 min | RF global | 810,05 | 439,06 | 118,86 | 0,09 |
| 1440 min | RF por hogar | 804,54 | 439,43 | 113,28 | 0,10 |

---

## 4. Top features (importancia media del RF global)

### Horizonte 15 min
1. **lag_1** (15 min antes): 46,7 %
2. **media_movil_1h**: 16,6 %
3. lag_1d (24 h antes): 5,7 %
4. lag_7d (1 semana antes): 5,4 %
5. media_movil_1d: 3,9 %

### Horizonte 60 min
1. **lag_1**: 31,4 %
2. **media_movil_1h**: 14,0 %
3. media_movil_1d: 10,6 %
4. std_movil_1d: 4,5 %
5. hora_cos: 4,5 %

### Horizonte 1440 min
1. **media_movil_1h**: 28,6 %
2. **lag_1d**: 15,4 %
3. **lag_7d**: 10,7 %
4. std_movil_1d: 5,4 %
5. media_movil_1d: 5,4 %

A medida que crece el horizonte, los lags inmediatos pierden peso y emergen los lags
periódicos (1 día, 7 días) y las medias móviles diarias.

---

## 5. Conclusiones para la memoria

1. **El RF bate al mejor baseline en todos los horizontes y roles.** Reducciones de RMSE de
   −180 W (h=15), −145 W (h=60) y −130 W (h=1440) sobre los hogares de entrenamiento.

2. **RF global ≥ RF por hogar.** En 4 de 6 combinaciones (rol × horizonte) el modelo global
   supera al personalizado, especialmente en validación externa. La transferabilidad entre hogares
   compensa la pérdida de personalización con `n_estimators=100`. Es una conclusión robusta
   para la memoria: **un único modelo entrenado con muchos hogares generaliza mejor que
   muchos modelos pequeños**.

3. **La validación externa (H2, H13) supera el R² del train en h=15 min** (0,38 vs 0,32) cuando
   se usa el RF global. Indica que H2 y H13 son hogares más predecibles cuando el modelo
   tiene buena capacidad de generalización — descarta sobreajuste.

4. **Las features dominantes son interpretables y dependientes del horizonte:**
   - Corto plazo (15 min): predomina la inercia inmediata (lag_1).
   - Medio plazo (60 min): la media móvil de 1 h gana peso.
   - Largo plazo (24 h): los lags estacionales (1 día, 7 días) y las medias diarias dominan.

5. **R² limitado en horizonte 1440 min (0,19)** confirma la dificultad intrínseca de la
   predicción a 24 h vista con features puramente endógenos. Aporta motivación al uso futuro
   de redes neuronales con memoria larga (LSTM, Transformers).

### Umbrales actualizados que cualquier modelo posterior debe batir

| Horizonte | RMSE objetivo (W) | MAE objetivo (W) | R² objetivo |
|-----------|------------------:|-----------------:|------------:|
| 15 min | < 425 | < 226 | > 0,32 |
| 60 min | < 459 | < 259 | > 0,22 |
| 1440 min | < 474 | < 266 | > 0,19 |

---

## 6. Siguiente paso — Notebook 09

Modelos de boosting (**XGBoost** y/o **LightGBM**) con el mismo protocolo (split, horizontes,
features, métricas). El boosting suele superar al RF en datos tabulares: si bate el RF en
RMSE y velocidad, se convierte en el modelo de referencia para la comparativa final con
redes neuronales (Nb 10/11).

## 7. Artefactos generados

- `resultados/metricas/08_random_forest.csv` — 198 filas (todos los modelos × hogares × horizontes).
- `resultados/metricas/08_random_forest_resumen.csv` — agregados por rol/horizonte/estrategia.
- `resultados/metricas/08_importancia_features_global.csv` — importancia features del RF global.
- `resultados/figuras/08_rmse_estrategias_por_horizonte.png`
- `resultados/figuras/08_importancia_features_global_h15.png`
- `resultados/figuras/08_mejora_rf_vs_baseline.png`
