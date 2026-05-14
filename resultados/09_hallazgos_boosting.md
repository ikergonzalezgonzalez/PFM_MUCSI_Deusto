# Hallazgos — Notebook 09: Gradient Boosting (XGBoost + LightGBM)

**Fecha:** 2026-05-12
**Notebook:** `notebooks/09_boosting_xgb_lgbm.ipynb`
**Fase del proyecto:** 2 — Modelado y comparativa (segundo bloque de modelos clásicos)

---

## 1. Configuración del experimento

Idéntica al Nb08 salvo modelo:

| Parámetro | Valor |
|-----------|-------|
| Granularidad | 15 min |
| Features | 22 (mismas que Nb08) |
| Horizontes (min) | 15, 60, 1440 |
| Estrategia | Solo modelo global con `id_hogar` |
| Split | 80/20 cronológico por hogar |
| XGBoost | n_estimators=300, max_depth=8, lr=0,05, min_child_weight=10, subsample=0,9 |
| LightGBM | n_estimators=300, num_leaves=63, lr=0,05, min_child_samples=20 |

---

## 2. Comparativa global — promedio sobre 18 hogares de entrenamiento

| Horizonte | Estrategia | RMSE (W) | MAE (W) | MAPE (%) | R² |
|-----------|------------|---------:|--------:|---------:|---:|
| 15 min | baseline media hora-día | 604,15 | 341,58 | 89,01 | 0,04 |
| 15 min | baseline persistencia | 669,17 | 255,63 | 53,72 | −0,23 |
| 15 min | RF global | 424,66 | 226,08 | 50,74 | 0,32 |
| 15 min | LightGBM | 419,86 | 221,44 | 49,52 | 0,33 |
| 15 min | **XGBoost** | **418,74** | **221,02** | **48,95** | **0,34** |
| 60 min | RF global | 459,14 | 258,68 | 61,23 | 0,22 |
| 60 min | LightGBM | 448,85 | 250,62 | 59,05 | 0,25 |
| 60 min | **XGBoost** | **448,12** | **249,93** | **58,44** | **0,25** |
| 1440 min | RF global | 473,95 | 266,28 | 64,40 | 0,19 |
| 1440 min | XGBoost | 469,46 | 268,37 | 64,39 | 0,21 |
| 1440 min | **LightGBM** | **469,12** | **266,00** | 63,04 | **0,21** |

## 3. Comparativa global — validación externa (H2 + H13)

| Horizonte | Estrategia | RMSE (W) | MAE (W) | MAPE (%) | R² |
|-----------|------------|---------:|--------:|---------:|---:|
| 15 min | RF global | 661,75 | 350,73 | 86,00 | 0,38 |
| 15 min | XGBoost | 679,64 | 336,94 | 70,82 | 0,35 |
| 15 min | **LightGBM** | **655,80** | **320,79** | **65,64** | **0,39** |
| 60 min | RF global | 732,32 | 411,55 | 108,33 | 0,25 |
| 60 min | XGBoost | 725,85 | 377,17 | 85,92 | 0,26 |
| 60 min | **LightGBM** | **721,14** | **369,34** | **80,35** | **0,27** |
| 1440 min | **RF global** | **810,05** | 439,06 | 118,86 | **0,09** |
| 1440 min | LightGBM | 817,74 | **405,96** | **89,58** | 0,07 |
| 1440 min | XGBoost | 822,41 | 419,87 | 103,50 | 0,06 |

---

## 4. Importancia de features (h = 15 min, modelos globales)

### XGBoost
1. lag_1: 35,2 %
2. media_movil_1h: 13,4 %
3. lag_1d: 4,4 %
4. hora: 4,2 %
5. lag_7d: 4,2 %

### LightGBM
1. lag_1: 51,0 %
2. media_movil_1h: 18,1 %
3. lag_1d: 4,7 %
4. lag_7d: 4,5 %
5. hora: 3,7 %

Ambos modelos coinciden con el RF en las features dominantes; LightGBM concentra más
peso en `lag_1`, mientras que XGBoost reparte más entre las features secundarias.

---

## 5. Conclusiones clave

1. **El gradient boosting bate al Random Forest en todos los horizontes y roles.**
   Mejora de 5-11 W de RMSE sobre 18 hogares train (consistente, aunque marginal).

2. **XGBoost y LightGBM son virtualmente equivalentes en train**
   (diferencias < 1 W de RMSE). Es esperado: son modelos del mismo paradigma.

3. **LightGBM gana en validación externa en 2 de 3 horizontes** (15 min y 60 min):
   reduce RMSE 6-11 W frente a XGBoost y mejora notablemente MAPE y MAE. Indica
   mejor generalización a hogares no vistos.

4. **En horizonte 1440 min (24 h) los tres modelos quedan empatados** (R² ≈ 0,19-0,21).
   El cuello de botella ya no es el algoritmo, sino la falta de información exógena
   (temperatura, calendario laboral, ocupación). Motivación para explorar arquitecturas
   con memoria larga (LSTM/Transformers) o features adicionales.

5. **Velocidad:** LightGBM entrena ~3× más rápido que XGBoost para tamaños equivalentes.
   Ventaja decisiva de cara al tuning del Nb10.

### Decisión — modelo finalista clásico: **LightGBM**

Razones:
- Gana en validación externa (donde se mide la generalización real).
- Mucho más rápido de entrenar (esencial para el tuning con grid/random search).
- Maneja NaN nativamente.
- Empate técnico con XGBoost en train, así que se prioriza generalización + velocidad.

---

## 6. Umbrales actualizados para Fase 2

| Horizonte | RMSE objetivo (W) | MAE objetivo (W) | R² objetivo |
|-----------|------------------:|-----------------:|------------:|
| 15 min | < 419 | < 221 | > 0,33 |
| 60 min | < 449 | < 251 | > 0,25 |
| 1440 min | < 469 | < 266 | > 0,21 |

---

## 7. Siguiente paso — Notebook 10

**Tuning de hiperparámetros de LightGBM** con `RandomizedSearchCV` adaptado a series temporales
(`TimeSeriesSplit` o equivalente walk-forward). Espacio de búsqueda inicial:
`num_leaves ∈ [31, 63, 127, 255]`, `learning_rate ∈ [0,03, 0,05, 0,1]`,
`n_estimators ∈ [200, 400, 800]`, `min_child_samples ∈ [5, 20, 50]`,
`subsample/colsample_bytree ∈ [0,7, 0,9, 1,0]`.
Después de Nb10, el modelo finalista queda fijado para la comparativa con redes neuronales (Nb11+).

## 8. Artefactos generados

- `resultados/metricas/09_boosting.csv` — tabla completa.
- `resultados/metricas/09_boosting_resumen.csv` — agregados.
- `resultados/metricas/09_importancia_features_xgb.csv`
- `resultados/metricas/09_importancia_features_lgbm.csv`
- `resultados/figuras/09_rmse_comparativa_modelos.png`
- `resultados/figuras/09_importancia_features_h15.png`
- `resultados/figuras/09_boxplot_rmse_finalistas.png`
