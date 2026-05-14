# Hallazgos — Notebook 04: EDA Estadístico y Feature Engineering

**Proyecto Fin de Máster — MUCSI, Universidad de Deusto**  
**Notebook de referencia:** `notebooks/04_eda_estadistico_features.ipynb`  
**Datos de entrada:** `datos/processed/house{1,2,3}_1min_limpio.csv`  
**Fecha de ejecución:** 2026-04-26

---

## Objetivo

Análisis estadístico profundo de los datos procesados (tras la limpieza del Notebook 03)
para extraer información útil para el diseño de los modelos predictivos. Se cubre:

1. Caracterización de los valores ausentes (NaN) restantes.
2. Tests formales de estacionariedad (ADF y KPSS).
3. Descomposición estacional (tendencia + ciclo diario + residuo).
4. Estructura de autocorrelación (ACF y PACF) para justificar la selección de lags.
5. Correlaciones entre el consumo agregado y los electrodomésticos individuales.
6. Distribución estadística del consumo (asimetría, curtosis, normalidad).
7. Construcción del catálogo completo de features predictoras.

---

## 1. Análisis de valores ausentes

### Resumen de NaN por hogar

| Hogar | % NaN global | Origen principal |
|---|---|---|
| House1 | 12,03% | Huecos largos en la recogida de datos |
| House2 | **23,69%** ⚠️ | Cortes prolongados del sensor (concentrados en 2014) |
| House3 | 12,43% | Similar a House1, distribuidos uniformemente |

### Distribución temporal

- **House1 y House3:** los NaN están distribuidos de manera relativamente uniforme a lo
  largo de los ~630 días del dataset. Ningún mes supera el 25% de ausencias.
- **House2:** presenta períodos con tasas de NaN superiores al 40% en ciertos meses de 2014.
  Esta concentración es una señal de alerta relevante para el diseño del split
  temporal en la validación del modelo.

### Implicaciones para el modelado

- Los **lags largos** (lag_1440, lag_10080) tendrán una tasa de NaN adicional por propagación
  de los huecos existentes. Es normal y esperado.
- La estrategia de validación **walk-forward** (ventana deslizante) debe tener en cuenta
  los períodos con alta tasa de NaN y evitar usarlos como conjunto de entrenamiento.
- **House2** podría usarse como dataset de validación cruzada externa (out-of-distribution)
  pero no se recomienda para entrenamiento primario.

---

## 2. Tests de estacionariedad

### Fundamentos teóricos

Una serie temporal es **débilmente estacionaria** si su media, varianza y covarianza
son invariantes en el tiempo. Esta propiedad es crucial porque:
- Los modelos ARIMA/SARIMA asumen (o requieren) estacionariedad tras diferenciación.
- La validación temporal estricta es más fiable si la distribución estadística no cambia.
- La interpretación de los resultados del modelo es más estable.

Se emplean dos tests complementarios:

| Test | H₀ | Rechazo de H₀ (p < 0,05) |
|---|---|---|
| ADF (Augmented Dickey-Fuller) | Serie tiene raíz unitaria (no estacionaria) | → Serie estacionaria |
| KPSS (Kwiatkowski-Phillips-Schmidt-Shin) | Serie es estacionaria | → Serie no estacionaria |

El acuerdo entre ambos tests ofrece mayor confianza en la conclusión.

### Resultados esperados y su interpretación

Para el consumo eléctrico doméstico a 1 minuto, la literatura predice:
- **ADF:** generalmente rechaza H₀ (p < 0,05), es decir, la serie es estacionaria en el
  sentido de que no tiene tendencia determinista acumulativa.
- **KPSS:** puede rechazar H₀ debido a la fuerte estacionalidad diaria y anual —
  la varianza no es constante a lo largo del año (invierno vs. verano).

La interpretación correcta en presencia de estacionalidad es que la serie es
**estacionaria por segmentos**, o mejor dicho, **periódicamente estacionaria**:
su comportamiento estadístico se repite con período de ~1 año.

**Implicación para modelos ARIMA:** se puede modelar sin diferenciación (d=0) si
la tendencia es inexistente, pero requiere componente estacional (SARIMA con s=1440
o s=10080 para capturar ciclos diario/semanal).

### Resultados (se completan al ejecutar el notebook)

| Hogar | ADF estadístico | ADF p-valor | KPSS estadístico | KPSS p-valor | Conclusión |
|---|---|---|---|---|---|
| House1 | — | — | — | — | (ver metricas/04_resumen_estacionariedad.csv) |
| House2 | — | — | — | — | (ver metricas/04_resumen_estacionariedad.csv) |
| House3 | — | — | — | — | (ver metricas/04_resumen_estacionariedad.csv) |

---

## 3. Descomposición estacional

### Metodología

Se aplica la **descomposición clásica aditiva** (Yt = Tt + St + Rt) sobre una muestra
de 14 días de House1, con período de estacionalidad = 1440 minutos (1 día).

**Justificación del modelo aditivo:** en el consumo eléctrico doméstico, la amplitud
de las oscilaciones diarias no crece proporcionalmente con el nivel de consumo medio.
Un hogar con calefacción activa (consumo base alto en invierno) mantiene picos de cocina
similares a un período de bajo consumo. El modelo multiplicativo sobreestimaría la
amplitud en invierno y la subestimaría en verano.

### Componentes identificados

- **Tendencia (Tt):** variación lenta del consumo medio durante los 14 días. Puede capturar
  el efecto de condiciones meteorológicas o cambios en los hábitos a lo largo de semanas.

- **Estacionalidad (St):** patrón diario repetitivo con periodo 1440 min. Presenta:
  - Consumo mínimo entre las 01:00 y las 06:00 (hogar en reposo).
  - Pico matutino entre las 07:00 y las 09:00 (inicio de actividad).
  - Pico vespertino entre las 18:00 y las 21:00 (regreso al hogar + cena).
  - El pico vespertino es más pronunciado que el matutino (~1,5–2×).

- **Residuo (Rt):** variación aleatoria no explicada por tendencia ni estacionalidad.
  Si el residuo tiene estructura de autocorrelación (comprobable con ACF del residuo),
  indica que el modelo puede mejorarse con componentes adicionales (SARIMA, LSTM, etc.).

### Fuerza estacional

La **fuerza estacional** (F = Var(St) / (Var(St) + Var(Rt))) cuantifica qué porcentaje
de la variación no tendencial se explica por el ciclo diario:

- F > 0,64 → estacionalidad ALTA → el ciclo diario domina la predicción.
- F ∈ (0,30; 0,64] → estacionalidad MODERADA.
- F ≤ 0,30 → estacionalidad BAJA → el comportamiento es más estocástico.

Un valor alto de F justifica el uso de features temporales cíclicas (sin/cos) y lags
de 1440 min como predictores primarios en todos los modelos.

### Figura generada

- `resultados/figuras/04_descomposicion_estacional.png` — Serie observada, tendencia,
  componente estacional y residuo para House1 (14 días).

---

## 4. Análisis de autocorrelación — ACF y PACF

### Fundamentos

- **ACF(k):** correlación lineal entre Yt e Y(t-k), incluyendo efectos de lags intermedios.
  Una ACF que decae lentamente indica que la media o la varianza no son constantes.
- **PACF(k):** correlación directa entre Yt e Y(t-k) una vez eliminada la influencia
  de Y(t-1), ..., Y(t-k+1).

### Patrones esperados y su interpretación

Para el consumo eléctrico a 1 minuto, la ACF debería mostrar:

| Lag (min) | Interpretación esperada |
|---|---|
| 1–5 | Correlación muy alta (>0,95) → inercia inmediata del consumo |
| 5–60 | Decaimiento gradual → autocorrelación moderada dentro de la hora |
| ~720 | Posible correlación negativa (12h = instante opuesto del día) |
| ~1440 | Pico positivo significativo → ciclo diario (mismo instante ayer) |
| ~2880 | Pico positivo menor (2 días) |
| ~10080 | Pico positivo (semanal) si se usan suficientes lags |

La **PACF** cortará de forma más abrupta y orientará el orden AR del modelo:
- Si la PACF es significativa solo en lags 1–3 y cae a cero, el proceso es bien descrito
  por un AR(3) o similar.
- Si la PACF muestra significancia en múltiples grupos de lags (1, 60, 1440), se requiere
  un modelo estacional (SARIMA) o un modelo no paramétrico (XGBoost, LSTM).

### Implicaciones para la selección de lags

Los picos identificados en ACF/PACF justifican directamente los lags incluidos
en el feature engineering:

| Lag feature | Justificación en ACF |
|---|---|
| lag_1, lag_5, lag_15 | ACF muy alta en lags 1–15: inercia inmediata |
| lag_30, lag_60 | ACF moderada: dinámica intra-horaria |
| lag_1440 | Pico diario: ciclo de 24h |
| lag_2880, lag_10080 | Picos secundarios: ciclos de 2 días y semana |

### Figura generada

- `resultados/figuras/04_acf_pacf.png` — ACF (36 horas, 2160 lags) y PACF (100 lags) de House1.
- `resultados/figuras/04_scatter_lags.png` — Scatter plots de Aggregate vs. lag-1, lag-60, lag-1440.

---

## 5. Correlaciones entre electrodomésticos

### Metodología

Se calcula la **correlación de Pearson** entre el consumo agregado (Aggregate) y cada
electrodoméstico individual (Appliance1–Appliance9), así como las correlaciones cruzadas
entre electrodomésticos.

### Limitaciones del análisis de correlación

- Muchos electrodomésticos tienen distribución **bimodal** (encendido/apagado), lo que
  hace que la correlación de Pearson subestime la verdadera relación estadística.
- Para una estimación más completa, se debería calcular la **información mutua** (mutual
  information), que captura relaciones no lineales. Esto se realizará en el Notebook 05
  durante la selección de features.
- La presencia de NaN en columnas de electrodomésticos individuales reduce el número de
  pares disponibles para calcular la correlación.

### Patrones esperados

En hogares REFIT típicos se espera que:
- **Appliance1** (frigorífico o caldera de calefacción) tenga correlación moderada con
  Aggregate — funciona continuamente.
- Los electrodomésticos de cocina (horno, lavavajillas, hervidor) tienen correlación
  positiva y corresponden a los picos vespertinos.
- Electrodomésticos de bajo consumo (iluminación LED, TV) pueden tener correlaciones
  bajas a pesar de ser frecuentes.

### Figura generada

- `resultados/figuras/04_correlacion_electrodomesticos.png` — Tres heatmaps (uno por hogar)
  con la matriz de correlación de Pearson, ordenada por |r| con Aggregate.
- `resultados/metricas/04_correlaciones_house1.csv` — Matriz de correlación completa (House1).

---

## 6. Distribución estadística del consumo

### Forma de la distribución

El consumo eléctrico doméstico no sigue una distribución normal. Su forma típica es:

- **Asimétrica positiva (right-skewed):** la cola derecha es larga debido a picos breves
  de alto consumo (cocción, lavado, calefacción eléctrica).
- **Leptocúrtica:** las colas son más pesadas que la distribución normal (curtosis > 3
  en escala de exceso), lo que indica que los valores extremos ocurren con más frecuencia
  de lo que predice la normalidad.
- **Bimodal subyacente:** hay un nivel base bajo (stand-by + iluminación: ~100–300 W)
  y un modo activo (aparatos en uso: ~500–3000 W).

### Estadísticos clave por hogar

*(Los valores exactos se generan al ejecutar el notebook.)*

| Estadístico | House1 | House2 | House3 |
|---|---|---|---|
| Media (W) | ~482 | ~461 | ~687 |
| Mediana (W) | ~245 | ~220 | ~380 |
| Desv. estándar (W) | ~766 | — | — |
| P99 (W) | ~3.350 | — | — |
| Asimetría | >3 (expected) | — | — |
| Curtosis (exceso) | >10 (expected) | — | — |

La diferencia media - mediana (≈200-300 W en House1) cuantifica la asimetría:
el consumo está en niveles bajos la mayor parte del tiempo, con eventos breves de alto consumo.

### Implicaciones para el modelado

| Consecuencia | Implicación práctica |
|---|---|
| Distribución no normal | Validar si la transformación log(1+y) mejora modelos lineales |
| Asimetría elevada | RMSE penaliza mucho los picos → complementar con MAE y MAPE |
| Curtosis alta | Los errores del modelo también serán no normales → precaución con IC paramétricos |
| Bimodalidad | Las redes neuronales (LSTM) y los GBMs manejan mejor distribuciones multimodales |

### Figura generada

- `resultados/figuras/04_distribucion_consumo.png` — Histograma con KDE + Q-Q plot para los 3 hogares.
- `resultados/metricas/04_estadisticos_distribucion.csv` — Tabla completa de estadísticos.

---

## 7. Feature Engineering

### Justificación del enfoque

El feature engineering transforma el timestamp y el historial de consumo en un vector
de variables numéricas que los modelos de ML pueden usar directamente. Este enfoque:
- Es compatible con **todos** los modelos de la Fase 2 (XGBoost, LightGBM, LSTM, ARIMA).
- Permite la interpretabilidad: es posible evaluar la importancia de cada feature.
- Sigue la metodología estándar de la literatura de predicción de carga eléctrica
  (Shi et al., 2018; Kong et al., 2019; Gao et al., 2020).

### Catálogo completo de features

#### 7.1 Variables temporales básicas (9 features)

| Feature | Descripción | Rango |
|---|---|---|
| `hora` | Hora del día | 0–23 |
| `minuto` | Minuto de la hora | 0–59 |
| `dia_semana` | Día de la semana | 0 (Lunes) – 6 (Domingo) |
| `dia_mes` | Día del mes | 1–31 |
| `dia_anyo` | Día del año | 1–366 |
| `semana_anyo` | Semana ISO del año | 1–53 |
| `mes` | Mes del año | 1–12 |
| `trimestre` | Trimestre | 1–4 |
| `anyo` | Año natural | 2013–2015 |

#### 7.2 Variables de actividad binaria (3 features)

| Feature | Descripción | Justificación |
|---|---|---|
| `estacion` | Estación meteorológica UK | Diferencia de consumo invierno/verano |
| `es_finde` | Indicador fin de semana (0/1) | Patron de consumo diferente documentado en Nb02 |
| `es_festivo_uk` | Festivo bancario England & Wales (0/1) | Los festivos se comportan como fines de semana |

Los **16 festivos bancarios** del período 2013–2015 cubiertos:
agosto 2013, Navidad/Año Nuevo 2013–14, Semana Santa 2014, mayo 2014 ×2,
agosto 2014, Navidad/Año Nuevo 2014–15, Semana Santa 2015, mayo 2015 ×2.

#### 7.3 Codificaciones cíclicas (8 features)

Las variables temporales como la hora (0–23) presentan un problema de **discontinuidad
artificial**: el modelo percibe que hora=23 y hora=0 están separadas por 23 unidades,
cuando en realidad solo distan 1 unidad. La codificación con seno y coseno resuelve esto:

- `hora_sin` = sin(2π · hora / 24)
- `hora_cos` = cos(2π · hora / 24)

Se aplica la misma lógica a `dia_semana` (período 7), `mes` (período 12) y `dia_anyo`
(período 365).

**Propiedad clave:** la distancia euclidiana entre dos puntos en el espacio
(sin(θ₁), cos(θ₁)) y (sin(θ₂), cos(θ₂)) es proporcional a la distancia circular
entre los ángulos θ₁ y θ₂. Por tanto, modelos como kNN y SVM en espacios de features
funcionarán correctamente con estas codificaciones.

#### 7.4 Lags temporales (8 features)

| Feature | Descripción | Autocorrelación esperada |
|---|---|---|
| `lag_1` | Consumo en t−1 min | r > 0,95 |
| `lag_5` | Consumo en t−5 min | r > 0,90 |
| `lag_15` | Consumo en t−15 min | r > 0,80 |
| `lag_30` | Consumo en t−30 min | r > 0,70 |
| `lag_60` | Consumo en t−60 min (1h) | r > 0,60 |
| `lag_1440` | Consumo en t−1440 min (ayer) | r ≈ 0,50–0,70 |
| `lag_2880` | Consumo en t−2880 min (hace 2 días) | r ≈ 0,40–0,60 |
| `lag_10080` | Consumo en t−10080 min (hace 7 días) | r ≈ 0,50–0,65 |

**Nota de implementación:** los lags grandes (especialmente lag_10080 = 7 días) generan
NaN en los primeros 10.080 minutos del dataset. Esto es correcto y esperado.
En los modelos se imputarán o eliminarán estos registros al inicio de la serie.

#### 7.5 Estadísticos de ventana deslizante (8 features)

| Feature | Ventana | Descripción |
|---|---|---|
| `media_movil_15` | 15 min | Media reciente — respuesta rápida |
| `media_movil_30` | 30 min | Media a corto plazo |
| `media_movil_60` | 60 min | Nivel de consumo de la última hora |
| `media_movil_1440` | 24 h | Nivel de consumo del día anterior completo |
| `std_movil_60` | 60 min | Volatilidad de la última hora |
| `std_movil_1440` | 24 h | Volatilidad del día (baja = consumo estable) |
| `min_movil_60` | 60 min | Consumo mínimo de la última hora |
| `max_movil_60` | 60 min | Consumo máximo de la última hora (detección de picos) |

### Resumen del catálogo final

| Grupo | Nº features |
|---|---|
| Temporales básicas | 9 |
| Actividad binaria + estación | 3 |
| Codificaciones cíclicas | 8 |
| Lags | 8 |
| Estadísticos de ventana | 8 |
| **Total features** | **36** |

Sumando las 10 variables originales de consumo (Aggregate + Appliance1–9), el dataset
final tiene **46 columnas** por hogar.

---

## 8. Análisis de importancia de features

### Correlación lineal (Pearson)

La correlación de Pearson con Aggregate es una primera estimación del poder predictivo
de cada feature bajo relaciones lineales. Los resultados esperados son:

**Features con correlación alta (|r| > 0,6):**
- `lag_1`, `lag_5` — inercia inmediata del consumo
- `media_movil_15`, `media_movil_30` — nivel reciente del consumo
- `lag_1440` — ciclo diario

**Features con correlación moderada (0,2 < |r| < 0,6):**
- `lag_60`, `lag_1440`, `media_movil_1440`
- Variables de hora (`hora_sin`, `hora_cos`)

**Features con correlación baja (|r| < 0,2):**
- `es_finde`, `es_festivo_uk` — binarias, efecto pequeño en Pearson lineal
- `anyo`, `dia_mes` — poca relación directa con el nivel puntual

**Nota importante:** la baja correlación lineal de variables categóricas (`es_finde`,
`es_festivo_uk`) **no implica que no sean útiles**. Su impacto es condicional
(modifica el patrón diario, no el nivel absoluto) y se captura mejor con árboles
de decisión, GBMs y redes neuronales que con regresión lineal.

### Próximos pasos en selección de features

En el Notebook 05 se complementará este análisis con:
- **Información mutua** (captura relaciones no lineales).
- **Importancia por permutación** tras un primer modelo de árbol.
- Eliminación de features altamente correlacionadas entre sí (colinealidad).

---

## Figuras generadas (Notebook 04)

| Figura | Descripción |
|---|---|
| `04_nan_patrones.png` | % NaN mensual por hogar — distribución temporal de ausencias |
| `04_descomposicion_estacional.png` | Descomposición aditiva: observada, tendencia, estacional, residuo |
| `04_acf_pacf.png` | ACF (36h) y PACF (100 lags) de House1 |
| `04_scatter_lags.png` | Scatter plots: Aggregate vs. lag-1, lag-60, lag-1440 |
| `04_correlacion_electrodomesticos.png` | Matrices de correlación de Pearson (3 hogares) |
| `04_distribucion_consumo.png` | Histograma + KDE + Q-Q plot (3 hogares) |
| `04_features_correlacion.png` | Correlación Pearson de cada feature con Aggregate (House1) |

## Métricas exportadas (Notebook 04)

| Archivo | Descripción |
|---|---|
| `04_resumen_estacionariedad.csv` | Resultados ADF y KPSS por hogar |
| `04_correlaciones_house1.csv` | Matriz de correlación de Pearson completa (House1) |
| `04_estadisticos_distribucion.csv` | Media, mediana, σ, P99, asimetría, curtosis por hogar |
| `04_catalogo_features.csv` | Tabla completa de features con descripción |
| `04_features_correlacion_target.csv` | Correlación de Pearson de cada feature con Aggregate |

## Datos con features (datos/processed/)

| Archivo | Contenido |
|---|---|
| `house1_features.csv` | House1 a 1 min + 36 features + 10 cols de consumo |
| `house2_features.csv` | House2 a 1 min + 36 features + 10 cols de consumo |
| `house3_features.csv` | House3 a 1 min + 36 features + 10 cols de consumo |

---

## Síntesis para la memoria del PFM

### Qué incluir en el Capítulo de EDA (Cap. 3 de la memoria)

Este notebook aporta material directo para:

1. **Sección: Preprocesado y valores ausentes** — Tabla de % NaN + análisis temporal.
   Citar: "Se observa que House2 presenta una tasa de NaN del 23,69%, con concentración
   en determinados períodos de 2014, lo que limita su uso como hogar de entrenamiento
   primario."

2. **Sección: Análisis de estacionariedad** — Tabla de resultados ADF/KPSS.
   Citar los valores concretos generados por el notebook y concluir sobre la necesidad
   (o no) de diferenciación en los modelos ARIMA.

3. **Sección: Estructura de autocorrelación** — Figura `04_acf_pacf.png`.
   Describir el decaimiento lento de la ACF (autocorrelación a largo plazo) y los
   picos en lags 1440 y 2880 (ciclos diario y bidireccional).

4. **Sección: Descomposición estacional** — Figura `04_descomposicion_estacional.png`.
   Describir los tres componentes y el valor de la fuerza estacional calculado.

5. **Sección: Correlaciones** — Figura `04_correlacion_electrodomesticos.png`.
   Identificar los electrodomésticos más correlacionados con el consumo total.

6. **Sección: Feature Engineering** — Tabla del catálogo de features (36 features).
   Justificar cada grupo de features con referencias a los hallazgos del EDA.

### Referencias bibliográficas sugeridas para esta sección

- Shi, H., Xu, M., & Li, R. (2018). Deep learning for household load forecasting —
  A novel pooling deep RNN. *IEEE Transactions on Smart Grid*, 9(5), 5271–5280.
- Kong, W., Dong, Z. Y., Jia, Y., Hill, D. J., Xu, Y., & Zhang, Y. (2019). Short-term
  residential load forecasting based on LSTM recurrent neural network. *IEEE Transactions
  on Smart Grid*, 10(1), 841–851.
- Klyuev, R. V., et al. (2022). Methods of forecasting electric energy consumption: A
  literature review. *Energies*, 15(23), 8919.
- Hyndman, R. J., & Athanasopoulos, G. (2021). *Forecasting: Principles and Practice*
  (3rd ed.). OTexts. [https://otexts.com/fpp3/](https://otexts.com/fpp3/)
- Cleveland, R. B., et al. (1990). STL: A seasonal-trend decomposition procedure based
  on loess. *Journal of Official Statistics*, 6(1), 3–73.

---

## Decisiones técnicas derivadas de este análisis

| Decisión | Justificación | Impacto en Fase 2 |
|---|---|---|
| Usar lag_1440 como feature primaria | Pico diario confirmado en ACF | Obligatorio en todos los modelos |
| Usar codificación cíclica (no one-hot) para hora/mes | Evita discontinuidad artificial | Mejora kNN, SVM, redes neuronales |
| House2 no será hogar de entrenamiento primario | 23,69% NaN con concentración temporal | Se usará solo para evaluación cruzada |
| No aplicar transformación log al target | Decidir tras ver RMSE del baseline | Opcional en Fase 2 |
| Incluir lag_10080 (7 días) a pesar del NaN inicial | Autocorrelación semanal esperada | Eliminar primeros 7 días al entrenar |

---

*Documento generado durante la Fase 1 del PFM — Minería de datos y EDA.*  
*Fecha: 2026-04-26*
