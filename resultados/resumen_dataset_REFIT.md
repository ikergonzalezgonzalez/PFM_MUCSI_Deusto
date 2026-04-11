# Resumen del Dataset y del Proyecto PFM
## Predicción de Consumo Eléctrico en Hogares Inteligentes

**Máster Universitario en Computación y Sistemas Inteligentes (MUCSI)**  
**Universidad de Deusto, Facultad de Ingeniería — Bilbao**  
**Fecha:** 2026-04-11

---

## 1. Por qué REFIT frente a otras alternativas

Para este proyecto se evaluaron los cuatro datasets de referencia en la literatura de predicción
de consumo eléctrico doméstico. La elección de REFIT se justifica en los siguientes criterios:

| Criterio | REFIT | REDD | UK-DALE | IHEPC |
|---|---|---|---|---|
| Nº de hogares | 20 | 6 | 5 | 1 |
| Duración | ~2 años | ~3 meses | ~4 años | ~4 años |
| Granularidad | 8 s | 3 s / 1 Hz | 6 s / 1 Hz | 1 min |
| Electrodomésticos | 9 por hogar | 3–24 por hogar | 5–26 por hogar | Agregado únicamente |
| País | Reino Unido | EE.UU. | Reino Unido | Francia |
| Acceso abierto | Sí (CC BY 4.0) | Sí | Sí | Sí |
| Versión limpia disponible | **Sí (CLEAN_)** | No oficial | No oficial | N/A |
| Diversidad de hogares | **Alta** | Baja | Baja | N/A |

**Razones concretas de la elección de REFIT:**

1. **Mayor diversidad de hogares (20 vs 5-6):** permite generalizaciones estadísticamente más
   robustas y reduces el sesgo por idiosincrasia de un único hogar.

2. **Versión limpia certificada:** el dataset incluye una versión preprocesada (`CLEAN_`) con
   una columna `Issues` que marca mediciones problemáticas, facilitando la limpieza reproducible.

3. **Duración suficiente para capturar estacionalidad anual completa:** con ~2 años de datos
   se dispone de dos ciclos invierno-verano, esencial para entrenar y validar modelos estacionales.

4. **Granularidad adecuada para predicción a corto plazo:** los ~8 s permiten remuestrear a
   cualquier resolución de interés (1 min, 15 min, 1 h) sin perder información.

5. **Contexto geográfico UK-DALE compatible:** ambos datasets son del Reino Unido, lo que facilita
   la comparación metodológica con trabajos previos que usan UK-DALE.

6. **REDD descartado** por ser exclusivamente norteamericano (60 Hz, diferente estándar de red)
   y por su cobertura temporal limitada (3 meses).

7. **IHEPC descartado** por no disponer de mediciones de electrodomésticos individuales,
   impidiendo análisis de desagregación de carga (NILM).

---

## 2. Características técnicas clave del dataset

| Característica | Detalle |
|---|---|
| Nombre completo | REFIT Electrical Load Measurements (Clean) |
| DOI | [10.5281/zenodo.5063428](https://doi.org/10.5281/zenodo.5063428) |
| Licencia | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| País | Reino Unido |
| Periodo de medición | 2013–2015 |
| Número de hogares total | 20 (Houses 1–21, sin House 14) |
| Hogares de trabajo en este PFM | House 1, House 2, House 3 |
| Granularidad original | ~7–8 segundos (declarada: 8 s) |
| Granularidad de trabajo | **1 minuto** (remuestreo por media) |
| Variables por hogar | Aggregate + Appliance1–Appliance9 + Issues |
| Unidad de medida | Vatios (W) instantáneos |
| Flag de calidad | Columna `Issues`: 0 = correcto, 1 = problemático |

### Características de los hogares de trabajo

| Hogar | Registros originales | Periodo | Consumo medio | Issues=1 |
|---|---|---|---|---|
| House 1 | 6.96 M | oct 2013 – jul 2015 | 481 W | 0.84% |
| House 2 | 5.73 M | sep 2013 – may 2015 | 465 W | 0.50% |
| House 3 | 6.99 M | sep 2013 – jun 2015 | 679 W | **5.84% ⚠️** |

> **Nota sobre House 3:** presenta un 5.84% de registros con `Issues=1` y un valor máximo de
> 65,836 W (físicamente inverosímil para un hogar doméstico). Se requiere análisis específico
> antes de usar este hogar en modelado.

---

## 3. Modelos a comparar y justificación académica

El proyecto adopta una estrategia de **comparativa progresiva de complejidad**, siguiendo la
metodología recomendada en la literatura de series temporales (Hyndman & Athanasopoulos, 2021):

### 3.1 Modelos baseline (referencia mínima)

| Modelo | Descripción | Justificación |
|---|---|---|
| Naïve (última observación) | Predice el último valor conocido | Cota inferior de error |
| Media histórica | Predice la media de la serie | Detector de si hay información explotable |
| Naïve estacional | Repite el mismo instante del día anterior | Baseline competitivo en series con ciclos |

> Los baselines son obligatorios en cualquier comparativa rigurosa: un modelo complejo que no
> supera el baseline no aporta valor real.

### 3.2 Modelos estadísticos clásicos

| Modelo | Librería | Justificación |
|---|---|---|
| SARIMA | `statsmodels` | Estándar de referencia en predicción de series temporales; interpretable |
| Prophet | `prophet` | Maneja automáticamente estacionalidad múltiple y días festivos |

### 3.3 Modelos de Machine Learning (con features de ingeniería)

| Modelo | Librería | Justificación |
|---|---|---|
| Random Forest | `scikit-learn` | Robusto, interpretable, buen rendimiento con features temporales |
| XGBoost | `xgboost` | Estado del arte en ML tabular; ampliamente usado en Kaggle y literatura |
| LightGBM | `lightgbm` | Más eficiente que XGBoost en datasets grandes; validado en benchmarks recientes |

### 3.4 Redes neuronales (deep learning)

| Modelo | Librería | Justificación |
|---|---|---|
| LSTM | `tensorflow/keras` | Arquitectura canónica para series temporales; aprende dependencias largas |
| (Opcional) Transformer | `tensorflow/keras` | Arquitectura moderna; alta capacidad pero requiere más datos y tuning |

### 3.5 Métricas de evaluación

| Métrica | Fórmula | Por qué se usa |
|---|---|---|
| **RMSE** | √(Σ(ŷ−y)²/n) | Penaliza errores grandes; mismas unidades que la variable (W) |
| **MAE** | Σ\|ŷ−y\|/n | Robusto a outliers; fácilmente interpretable |
| **MAPE** | Σ\|ŷ−y\|/y · 100 | Error porcentual; permite comparar entre hogares |
| **R²** | 1−SS_res/SS_tot | Proporción de varianza explicada; estándar académico |

> **Validación estrictamente temporal:** se usa walk-forward validation (nunca partición
> aleatoria) para respetar la causalidad de las series temporales. El conjunto de test
> comprende el último 20% temporal de cada hogar.

---

## 4. Estado actual del proyecto (a 2026-04-11)

### Completado ✅
- [x] Estructura de carpetas y repositorio Git inicializado
- [x] Dataset REFIT descargado y extraído en `datos/raw/`
- [x] Entorno Python configurado con todas las dependencias instaladas
- [x] **Notebook 01** — Inspección inicial ejecutado y verificado:
  - Estructura, tipos de datos, rango temporal
  - Análisis de valores nulos, duplicados y columna Issues
  - Estadísticas descriptivas y primeras visualizaciones
  - 8 figuras exportadas + CSV resumen generado
- [x] **Notebook 02** — Visualizaciones para presentación a tutora:
  - Serie temporal completa (2 años)
  - Perfil horario (laborables vs fin de semana)
  - Patrón semanal con IC al 95%
  - Estacionalidad mensual
  - Heatmap de semana típica

### En curso / Pendiente ⏳
- [ ] **Decisión:** estrategia de tratamiento de Issues=1 en House 3
- [ ] **Decisión:** umbral de recorte de outliers severos (House 3 máx: 65,836 W)
- [ ] **Notebook 03** — Limpieza de datos y guardado en `datos/processed/`
- [ ] **Notebook 04** — Feature engineering (lags, medias móviles, variables calendáricas)
- [ ] Fase 2: Modelado y comparativa
- [ ] Fase 3: Dashboard Streamlit + Memoria LaTeX

---

## 5. Próximos pasos concretos

### Fase 1 — Completar EDA y limpieza (inmediato)

1. **Decidir estrategia Issues=1** con la tutora:
   - Opción A: descartar registros (`Issues==1 → drop`) — sencillo, conservador
   - Opción B: imputar con interpolación lineal — preserva continuidad temporal
   - Recomendación provisional: **interpolación lineal para gaps < 5 min, descarte para gaps mayores**

2. **Decidir umbral de outliers:**
   - Opción A: recorte por percentil (p99.5 o p99.9 por hogar)
   - Opción B: umbral físico fijo (p.ej. 15,000 W = 15 kW para hogar doméstico)
   - Recomendación provisional: **umbral físico + winsorización al p99.5**

3. **Notebook 03 — Limpieza:** aplicar decisiones anteriores y guardar
   `datos/processed/house{n}_1min_clean.parquet` (formato Parquet, más eficiente que CSV)

4. **Notebook 04 — Feature engineering:**
   - Variables temporales: hora, día semana, mes, es_finde, es_festivo_UK
   - Lags: t-1, t-5, t-10, t-30, t-60 minutos
   - Medias móviles: ventanas de 15, 30, 60 minutos
   - Estadísticos por ventana: std, min, max de últimas N observaciones

### Fase 2 — Modelado (tras completar Fase 1)

5. **Notebook 05** — Baselines y SARIMA
6. **Notebook 06** — XGBoost, Random Forest, LightGBM
7. **Notebook 07** — LSTM

### Fase 3 — Entrega (tras completar Fase 2)

8. Dashboard Streamlit con predicción interactiva
9. Memoria académica en LaTeX (plantilla Deusto `memoriaPFC.cls`)
10. Defensa oral ante tribunal

---

*Documento generado automáticamente — actualizar tras cada sesión de trabajo.*
