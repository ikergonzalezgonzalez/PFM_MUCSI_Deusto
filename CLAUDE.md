# CONTEXTO GENERAL DEL PROYECTO — PFM MUCSI Deusto

Eres el asistente técnico y académico de mi Proyecto Fin de Máster (PFM) 
del Máster Universitario en Computación y Sistemas Inteligentes (MUCSI) 
de la Universidad de Deusto, Facultad de Ingeniería, Bilbao.

## TÍTULO DEL PROYECTO
"Desarrollo de un modelo de aprendizaje automático para la predicción y 
optimización del consumo eléctrico en entornos domésticos inteligentes"

## PERFIL DEL ESTUDIANTE
- Ingeniero informático con nivel medio en ML/IA
- Familiarizado con Python, Java, C, C++
- Conocimientos básicos de aprendizaje automático
- Nivel intermedio-básico en uso de Claude y LLMs en general
- Quiere aprender a trabajar de forma eficiente y organizada con IA

## ESTÁNDARES DE CALIDAD EXIGIDOS
- Calidad académica de PFM de máster universitario (Universidad de Deusto)
- Todo el código en Python, comentado en español
- Nombres de variables y funciones en español
- Reproducibilidad total: semilla fija = 42 en todos los experimentos
- Documentar versiones de librerías usadas
- Cada notebook debe ser autocontenido y ejecutable de arriba a abajo
- Sin celdas rotas, sin outputs hardcodeados
- Rigor estadístico en todas las métricas y visualizaciones

## STACK TECNOLÓGICO
- Lenguaje: Python 3.10+ (instalado: Python 3.14.0)
- Entorno: Jupyter Notebooks para EDA y experimentación
- Scripts .py para código de producción y utilidades
- Librerías principales: pandas, numpy, matplotlib, seaborn, 
  scikit-learn, statsmodels, xgboost, lightgbm, tensorflow/keras
- Dashboard final: Streamlit (por decidir)
- Control de versiones: Git + GitHub
- Memoria académica: LaTeX (plantilla oficial Deusto — memoriaPFC.cls)

## DATASET

### Fuente 1 — Zenodo CLEAN (6 hogares)
- Nombre: REFIT Electrical Load Measurements (versión limpia)
- Fuente: Zenodo doi:10.5281/zenodo.5063428
- Granularidad: 8 segundos | Duración: ~2 años (2013-2015)
- Variables: consumo agregado + 9 electrodomésticos individuales
- Ficheros en datos/raw/: CLEAN_House1.csv, CLEAN_House2.csv, CLEAN_House3.csv,
  CLEAN_House4.csv, CLEAN_House5.csv, CLEAN_House11.csv
- Formato: CSV con cabecera, columnas Time/Unix/Aggregate/App1-9/Issues (13 cols)

### Fuente 2 — Strathclyde Power Data (14 hogares nuevos)
- Fuente: pureportal.strath.ac.uk (REFITPowerData111215.7z, dic 2015)
- Hogares: House6-10, House12-13, House15-21 (en datos/raw/)
- Duplicados (H1-5, H11) movidos a datos/raw/strathclyde_duplicados/
- Formato diferente: sin cabecera, 11 cols (Unix, Aggregate, App1-9), sin columna Issues
- Granularidad y período similares al Zenodo

### Hogares procesados (datos/processed/)
- Entrenamiento (18): H1,H3,H4,H5,H11 (Zenodo) + H6,H7,H8,H9,H10,H12,H15,H16,H17,H18,H19,H20,H21 (Strathclyde)
- Validación externa (2): H2 (NaN=23,69%) + H13 (NaN=21,27%)
- Tabla completa: resultados/metricas/06_seleccion_hogares_final.csv

## FASES DEL PROYECTO

### FASE 1 — Minería de datos y EDA ✅ COMPLETADA (2026-05-06)
- [x] Extracción y carga del dataset REFIT
- [x] Inspección inicial: estructura, tipos, rango temporal, nulos, duplicados
- [x] Limpieza: Issues=1 eliminados, outliers (umbral 15.000 W), remuestreo a 1 min, interpolación gaps ≤30 min
- [x] Remuestreo a 1 minuto (incluido en Notebook 03)
- [x] EDA completo sobre datos limpios: ACF/PACF, correlaciones, test estacionariedad, análisis NaN restantes
- [x] Feature engineering: 36 features (temporales, cíclicas, lags, medias móviles) — H1,H2,H3
- [x] Limpieza Houses 4, 5, 11 (Zenodo CLEAN) — NaN: 11,63% / 8,38% / 10,67%
- [x] Limpieza 14 casas Strathclyde (Nb05) — 13 aptas, House13 excluida
- [x] Features H4, H5, H11 (Zenodo) — lag_1 top feature (r=0,888/0,907/0,937)
- [x] Features + EDA condensado 13 casas Strathclyde (Nb06) — lag_1 domina en todos (r=0,779–0,936)

### FASE 2 — Modelado y comparativa
- [x] Baseline: persistencia y media hora-día (Nb07, 2026-05-12) — RMSE persistencia h=1 min: 297 W; suelo media: 604 W
- [x] Random Forest (Nb08, 2026-05-12) — RF global RMSE h=15: 425 W (R²=0,32), h=60: 459 W, h=1440: 474 W
- [x] XGBoost + LightGBM (Nb09, 2026-05-12) — LightGBM elegido finalista: RMSE h=15: 420 W, h=60: 449 W, h=1440: 469 W
- [ ] ARIMA/SARIMA (opcional, baja prioridad)
- [ ] Redes neuronales: LSTM, posiblemente Transformers
- [x] Métricas estándar acordadas: RMSE, MAE, MAPE (filtrado >50 W), R²
- [x] Estrategia de validación: split cronológico 80/20 por hogar; walk-forward reservado para la evaluación final
- [ ] Comparativa rigurosa entre modelos

### FASE 3 — Aplicación y documentación
- [ ] Dashboard interactivo con Streamlit para predicción de consumo
- [ ] Memoria académica completa en LaTeX (plantilla Deusto memoriaPFC.cls)
- [ ] Capítulo obligatorio de Valoración Ética del proyecto
- [ ] Preparación de defensa oral ante tribunal

## ESTRUCTURA DEL PROYECTO
```
PFM_MUCSI_Deusto/
├── datos/
│   ├── raw/                  # CSVs originales sin modificar
│   └── processed/            # Datos limpios y procesados
├── notebooks/                # Jupyter Notebooks de análisis
├── src/                      # Scripts Python de producción
│   └── utils/                # Funciones auxiliares reutilizables
├── modelos/                  # Modelos entrenados serializados
├── resultados/
│   ├── figuras/              # Gráficos exportados
│   └── metricas/             # CSVs con resultados de evaluación
├── memoria_latex/            # Archivos .tex de la memoria académica
├── dashboard/                # Aplicación Streamlit (Fase 3)
├── CLAUDE.md                 # Este archivo de contexto
├── README.md                 # Descripción del proyecto
├── requirements.txt          # Dependencias Python
└── .gitignore                # Archivos a ignorar en Git
```

## ESTRUCTURA DE LA MEMORIA (plantilla Deusto)
- Resumen 200-250 palabras + descriptores 3-5 palabras clave
- Índice general, índice de figuras, índice de tablas
- Capítulos con \chapter, \section, \subsection
- Bibliografía en BibTeX (referencias.bib)
- Apéndices opcionales
- Sin páginas en blanco, márgenes y encabezados fijos según plantilla

## INSTRUCCIONES PERMANENTES PARA EL ASISTENTE
1. Mantén siempre rigor académico de PFM de máster universitario
2. Genera código Python bien estructurado, comentado en español
3. Prioriza reproducibilidad: semilla 42, documenta versiones de librerías
4. Justifica siempre las decisiones técnicas y de diseño
5. Sugiere proactivamente mejoras de calidad académica
6. Recuerda en cada sesión en qué fase estamos y qué queda por hacer
7. Cuando algo pueda hacerse de varias formas, explica las opciones brevemente
8. Si detectas un error o algo mejorable en el enfoque, dilo directamente
9. Ayuda a aprender buenas prácticas de organización y uso eficiente de IA
10. Al final de cada sesión de trabajo, resume qué se ha hecho y cuál es
    el siguiente paso concreto

## DECISIONES TÉCNICAS TOMADAS
| Fecha      | Decisión                                           | Justificación                        |
|------------|----------------------------------------------------|--------------------------------------|
| 2026-04-11 | Python 3.14.0 como entorno base                   | Ya instalado en el sistema            |
| 2026-04-11 | Trabajo principal con Houses 1, 2 y 3             | Indicado en el diseño del proyecto   |
| 2026-04-11 | Remuestreo de 8s a 1 minuto                       | Balance entre detalle y manejabilidad |
| 2026-04-26 | House2 solo para validación, no entrenamiento     | 23,69% NaN con concentración temporal |
| 2026-04-26 | Codificación cíclica sin/cos para vars. periódicas | Evita discontinuidad artificial en hora, mes, día |
| 2026-04-26 | 36 features en 5 grupos para todos los modelos    | Catálogo unificado desde EDA (Nb04) |
| 2026-05-06 | Ampliar a 6 hogares Zenodo + 14 Strathclyde       | Riesgo de sesgo con solo 2 hogares para entrenar; decisión post-tutoría |
| 2026-05-06 | Houses 1,3,4,5,11 (Zenodo) + aptas Strathclyde para entrenamiento | House2: 23,69% NaN → solo validación externa |
| 2026-05-06 | Strathclyde format: sin cabecera, 11 cols, sin Issues | Diferencia clave respecto a Zenodo CLEAN — adaptación del pipeline |
| 2026-05-06 | Umbral NaN ≤ 20% para incluir casa Strathclyde en training | Mismo criterio que se aplicó a House2 Zenodo |
| 2026-05-12 | Split cronológico 80/20 por hogar como estándar de Fase 2 | Comparativa rápida entre modelos; walk-forward reservado para evaluación final |
| 2026-05-12 | Horizontes de evaluación: 1, 15, 60, 1440 min | Cubren inercia inmediata, corto, medio plazo y ciclo diario completo |
| 2026-05-12 | MAPE con filtro y_real > 50 W | Evita divergencia del MAPE en consumos nocturnos cercanos a cero |
| 2026-05-12 | Granularidad 15 min para modelos no neuronales | Reduce 800K → 53K filas/hogar; mantiene horizontes 15/60/1440 min |
| 2026-05-12 | Descartar horizonte 1 min en modelos clásicos | Ya dominado por persistencia (RMSE 297 W); no aporta valor comparativo |
| 2026-05-12 | RF global con id_hogar > RF por hogar | Mejor transferabilidad y validación externa; será la estrategia por defecto |
| 2026-05-12 | LightGBM elegido como modelo clásico finalista | Empate con XGBoost en train pero gana en validación externa (2/3 horizontes) y ~3× más rápido |

---

## REGISTRO DE PROGRESO

### Sesión 1 — 2026-04-11
**Estado:** Configuración inicial completa y entorno listo para trabajar
- Estructura de carpetas creada en Escritorio/PFM_MUCSI_Deusto/
- CSVs extraídos del zip (Houses 1, 2, 3, 4, 5, 11) a datos/raw/
- CLAUDE.md, README.md, requirements.txt y .gitignore creados
- Repositorio Git inicializado con commit inicial
- Dependencias instaladas y verificadas:
  - pandas 2.3.3 / numpy 2.3.5 / matplotlib 3.10.7 / seaborn 0.13.2
  - scikit-learn 1.7.2 / statsmodels 0.14.6
  - xgboost 3.2.0 / lightgbm 4.6.0
  - jupyterlab 5.9.1 / ipykernel 7.2.0 / ipywidgets 8.1.8
**Pendiente:** tensorflow/keras (se instalará en Fase 2 cuando se necesite)

### Notebook 01 — 2026-04-11
**Estado:** Completado y ejecutado correctamente
- `notebooks/01_inspeccion_inicial.ipynb` generado y ejecutado sin errores
- 8 figuras exportadas a `resultados/figuras/`
- Resumen ejecutivo guardado en `resultados/metricas/01_resumen_inspeccion.csv`
- Hallazgos clave:
  - House1: 6.96M registros, 638 días (oct 2013 – jul 2015), media 481 W
  - House2: 5.73M registros, 617 días (sep 2013 – may 2015), media 465 W
  - House3: 6.99M registros, 614 días (sep 2013 – jun 2015), media 679 W
  - Intervalo mediano real: 7 s (no exactamente 8 s)
  - Sin valores nulos, sin duplicados de timestamp, sin valores negativos
  - Issues=1: House1 0.84%, House2 0.50%, House3 5.84% (⚠️  House3 elevado)
  - Consumo máximo House3: 65,836 W (posible outlier severo a investigar)
**Siguiente paso:** Notebook 03 — Limpieza de datos
  (tratamiento de Issues=1, outliers, remuestreo de 7s a 1 minuto)

### Notebook 02 + Resumen — 2026-04-11
**Estado:** Completado y ejecutado correctamente
- `notebooks/02_presentacion_tutora.ipynb` — 5 figuras generadas:
  - `02_serie_temporal_completa.png` — serie completa 2 años con media móvil 30 días
  - `02_patron_diario_horas.png` — perfil horario laborable vs fin de semana con ±1σ
  - `02_patron_semanal.png` — barras por día con IC al 95%
  - `02_estacionalidad_mensual.png` — consumo medio por mes con paleta estacional
  - `02_heatmap_semana_tipica.png` — heatmap hora × día de la semana
- `resultados/metricas/02_estadisticas_house1_1min.csv` — estadísticas del remuestreo
- `resultados/resumen_dataset_REFIT.md` — documento completo para tutora:
  - Justificación de REFIT vs REDD / UK-DALE / IHEPC
  - Características técnicas del dataset
  - Tabla comparativa de modelos y métricas planificados
  - Estado actual y próximos pasos detallados

### Notebook 03 — 2026-04-17
**Estado:** Completado y ejecutado correctamente
- `notebooks/03_limpieza_datos.ipynb` — pipeline de limpieza completo para los 3 hogares
- Decisiones resueltas:
  - Issues=1: eliminación de filas en los 3 hogares (distribuidos uniformemente, sin concentración temporal)
  - Outliers Aggregate: umbral físico 15.000 W → valores superiores convertidos a NaN
  - Huecos cortos: interpolación lineal para gaps ≤ 30 minutos
  - Remuestreo: de ~7 s a 1 minuto por media (resuelve irregularidad del intervalo)
- Datasets procesados guardados en `datos/processed/`:
  - `house1_1min_limpio.csv` — 920.091 filas, media 482 W, máx 13.763 W, 12,03% NaN
  - `house2_1min_limpio.csv` — 889.078 filas, media 461 W, máx 14.294 W, **23,69% NaN** ⚠️
  - `house3_1min_limpio.csv` — 885.095 filas, media 687 W, máx 12.628 W, 12,43% NaN
- 4 figuras exportadas a `resultados/figuras/`
- `resultados/metricas/03_resumen_limpieza.csv` exportado
**Siguiente paso:** Notebook 05 — Modelado baseline y comparativa

### Sesión 2026-05-06 — Ampliación de hogares
**Estado:** COMPLETADO — Nb05 y Nb06 ejecutados. Fase 1 cerrada excepto features H4,H5,H11
- **Decisión 1:** ampliar de 2 hogares (H1, H3) a 6 Zenodo (H1-5, H11) tras tutoría
- **Decisión 2:** añadir 14 casas nuevas del Strathclyde (H6-10, H12-13, H15-21)
  - Descargado `REFITPowerData111215.7z` de `pureportal.strath.ac.uk`
  - Duplicados Strathclyde (H1,2,3,4,5,11) movidos a `datos/raw/strathclyde_duplicados/`
  - Diferencia de formato: sin cabecera, 11 cols, sin Issues → pipeline adaptado
- **Notebooks creados:**
  - `notebooks/05_inspeccion_limpieza_strathclyde.ipynb` — pipeline batch para 14 casas
  - `notebooks/06_eda_features_strathclyde.ipynb` — EDA condensado + 36 features
- **Documentación:** `resultados/05_decision_ampliacion_hogares.md` actualizado
- **Resultados limpieza Houses 4, 5, 11 (Zenodo CLEAN):**
  - House4: NaN=11,63%, media=381,7W → APTO entrenamiento
  - House5: NaN=8,38%,  media=733,2W → APTO entrenamiento
  - House11: NaN=10,67%, media=455,8W → APTO entrenamiento
- **Resultados limpieza 14 casas Strathclyde (Nb05):**
  - 13 casas APTAS (NaN ≤ 20%): H6,H7,H8,H9,H10,H12,H15,H16,H17,H18,H19,H20,H21
  - 1 casa EXCLUIDA: House13 (NaN=21,27%) → disponible para validación
- **Lista definitiva de entrenamiento:** H1,H3,H4,H5,H11 (Zenodo) + H6,H7,H8,H9,H10,H12,H15,H16,H17,H18,H19,H20,H21 (Strathclyde) = **18 hogares**
- **Validación externa:** H2 (Zenodo, NaN=23,69%) + H13 (Strathclyde, NaN=21,27%)
- **Resultados Nb06 (EDA + features Strathclyde):**
  - lag_1 top feature en los 13 hogares (r=0,779–0,936); rolling_mean_15 siempre segundo
  - Distribuciones fuertemente asimétricas en todos — confirma patrón de Nb04
  - `06_hallazgos_limpieza_ampliacion.md` completado con todos los valores reales
- **Features H4, H5, H11 completadas** (`src/utils/features_houses_4_5_11.py`):
  - H4: lag_1 r=0,888 | H5: lag_1 r=0,907 | H11: lag_1 r=0,937
  - `06_seleccion_hogares_final.csv` actualizado con todos los NaN% reales
- **Fase 1 completada al 100%.** Siguiente paso: iniciar Fase 2 (baseline + modelos clásicos)

### Notebook 07 — 2026-05-12
**Estado:** Completado y ejecutado correctamente — apertura de Fase 2
- `notebooks/07_baseline_split_temporal.ipynb` — define la estrategia de validación temporal y evalúa dos baselines en los 20 hogares × 4 horizontes
- **Reglas del juego de Fase 2 fijadas:** split cronológico 80/20 por hogar, horizontes 1/15/60/1440 min, MAPE filtrado >50 W
- **Baselines implementados:**
  - Persistencia (ŷ_{t+h} = y_t): RMSE=297 W, R²=0,74 a horizonte 1 min — rival fortísimo en corto plazo, colapsa a R²<0 a partir de h=15 min
  - Media hora-día (lookup por hora y día_semana): RMSE plano ≈604 W en todos los horizontes; suelo absoluto a batir
- **Umbrales que cualquier modelo de Fase 2 debe superar:**
  - h=1 min: RMSE < 297 W, MAE < 73 W, R² > 0,74
  - h≥15 min: RMSE < 604 W, MAE < 342 W
- 3 figuras + 2 CSVs en `resultados/`; hallazgos en `resultados/07_hallazgos_baseline.md`
**Siguiente paso:** Notebook 08 — Random Forest con catálogo de 36 features (Nb04/Nb06), mismo split temporal

### Notebook 08 — 2026-05-12
**Estado:** Completado y ejecutado correctamente — primer modelo clásico
- `notebooks/08_random_forest.ipynb` — RF en granularidad 15 min con 22 features adaptadas; dos estrategias (por hogar y global con id_hogar)
- **Resultados (media 18 hogares train):**
  - h=15 min: RF global RMSE=425 W, R²=0,32 (baseline mejor era 604 W, R²=0,04) → mejora 30%
  - h=60 min: RF global RMSE=459 W, R²=0,22 → mejora 24%
  - h=1440 min: RF global RMSE=474 W, R²=0,19 → mejora 22%
- **Validación externa (H2, H13) con RF global:** R²=0,38 a h=15 min (mejor que train) → confirma generalización
- **Hallazgo clave:** RF global ≥ RF por hogar en 4 de 6 escenarios → transferabilidad gana a personalización
- **Top features por horizonte:**
  - Corto plazo: lag_1 domina (46,7%)
  - Largo plazo: lag_1d + lag_7d + medias móviles de 1 h y 1 día (patrón estacional)
- 3 figuras + 3 CSVs en `resultados/`; hallazgos en `resultados/08_hallazgos_random_forest.md`
**Siguiente paso:** Notebook 09 — XGBoost y/o LightGBM (boosting) con mismo protocolo

### Notebook 09 — 2026-05-12
**Estado:** Completado y ejecutado correctamente — segundo bloque de modelos clásicos
- `notebooks/09_boosting_xgb_lgbm.ipynb` — XGBoost + LightGBM globales, mismas 22 features y protocolo del Nb08
- **Bug detectado y resuelto:** duplicación de columna `id_hogar` al concatenar listas (sklearn lo toleraba, XGBoost no)
- **Instalación:** xgboost 3.2.0 y lightgbm 4.6.0 instalados en el Python 3.10 de Jupyter (CLAUDE.md decía que estaban pero no lo estaban)
- **Resultados (media 18 hogares train):**
  - h=15 min: XGBoost RMSE=419 W (R²=0,34), LightGBM=420 W, RF=425 W
  - h=60 min: XGBoost RMSE=448 W, LightGBM=449 W, RF=459 W
  - h=1440 min: LightGBM RMSE=469 W (R²=0,21), XGBoost=469 W, RF=474 W
- **Validación externa (H2, H13):** LightGBM gana en 2/3 horizontes con margen 5-11 W RMSE
- **Decisión finalista:** LightGBM por mejor generalización + 3× más rápido (esencial para tuning Nb10)
- **Top features (h=15 min):** lag_1 (35-51%) + media_movil_1h (13-18%) — coinciden con RF
- 3 figuras + 4 CSVs en `resultados/`; hallazgos en `resultados/09_hallazgos_boosting.md`
**Siguiente paso:** Notebook 10 — Tuning hiperparámetros de LightGBM con TimeSeriesSplit

### Notebook 04 — 2026-04-26
**Estado:** Completado y ejecutado correctamente
- `notebooks/04_eda_estadistico_features.ipynb` — EDA estadístico completo + feature engineering
- Análisis cubiertos: NaN temporales, tests ADF/KPSS, descomposición estacional,
  ACF/PACF (36h, 2160 lags), correlaciones entre electrodomésticos, distribuciones estadísticas
- Feature engineering: 36 features en 5 grupos (temporales, binarias, cíclicas, lags, rolling)
  aplicadas a H1, H2, H3 → `datos/processed/house{1,2,3}_features.csv`
- 7 figuras + 5 CSVs de métricas exportados
- `resultados/04_hallazgos_eda_estadistico.md` — documento de hallazgos para la memoria
- **Decisiones clave:**
  - House2 (23,69% NaN) no se usará para entrenamiento primario — solo validación cruzada
  - lag_1440 es feature primaria (pico diario en ACF confirmado)
  - Codificación cíclica (sin/cos) adoptada para variables temporales periódicas
  - lag_10080 incluido a pesar de NaN inicial (autocorrelación semanal esperada)

---

## HALLAZGOS EDA INICIAL (Sesión 2 — 2026-04-11)

- House1: 6.96M registros, oct 2013 – jul 2015, media 481W, Issues=1: 0.84%
- House2: 5.73M registros, sep 2013 – may 2015, media 465W, Issues=1: 0.50%
- House3: 6.99M registros, sep 2013 – jun 2015, media 679W, Issues=1: 5.84% ⚠️
- Intervalo real de muestreo: 7 segundos (no 8 como indica la documentación)
- House3 máximo: 65,836W — outlier severo, físicamente inverosímil ⚠️

## HALLAZGOS LIMPIEZA (Notebook 03 — 2026-04-17)

- Outliers eliminados: máximos reducidos a niveles físicamente plausibles en los 3 hogares
- NaN residuales tras limpieza y remuestreo: House1 12,03%, House2 **23,69%** ⚠️, House3 12,43%
- House2 con 23,69% de NaN es una alerta relevante para la fase de modelado
- Los huecos cortos (≤30 min) se interpolaron linealmente; los largos se dejan como NaN

### HALLAZGOS EDA ESTADÍSTICO (Notebook 04 — 2026-04-26)
- 36 features construidas: 9 temporales + 3 binarias + 8 cíclicas + 8 lags + 8 rolling
- lag_1, lag_5, lag_15 tienen r > 0,95 con Aggregate (inercia inmediata)
- lag_1440 tiene r ≈ 0,50–0,70 (ciclo diario dominante, confirma pico en ACF)
- Distribución Aggregate: fuertemente asimétrica (asimetría > 3), leptocúrtica, no normal
- Descomposición estacional: ciclo diario dominante confirmado (ver figuras 04_descomposicion_estacional.png)
- Tests ADF/KPSS: series estacionarias en las 3 casas (ver 04_resumen_estacionariedad.csv)

### DECISIONES RESUELTAS (antes pendientes)
- **House2 y NaN:** se usa solo para validación cruzada external (out-of-distribution)
  No se incluye en el entrenamiento primario.
- **Estrategia NaN en modelado:** los lags introducen NaN propagados → se eliminan las
  primeras N filas correspondientes al lag más largo (lag_10080 = 7 días) antes de entrenar.

---
*Este archivo debe leerse al inicio de cada nueva sesión de trabajo.*
