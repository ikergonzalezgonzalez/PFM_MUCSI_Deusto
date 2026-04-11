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
- Nombre: REFIT Electrical Load Measurements (versión limpia)
- Fuente: Zenodo doi:10.5281/zenodo.5063428
- Contenido: consumo eléctrico de 20 hogares del Reino Unido
- Granularidad: 8 segundos
- Duración: ~2 años (2013-2015)
- Variables: consumo agregado del hogar + 9 electrodomésticos individuales
- Ficheros disponibles en datos/raw/:
    CLEAN_House1.csv, CLEAN_House2.csv, CLEAN_House3.csv (trabajo principal)
    CLEAN_House4.csv, CLEAN_House5.csv, CLEAN_House11.csv (adicionales)
- Formato: CSV con separador coma, columna de timestamp

## FASES DEL PROYECTO

### FASE 1 — Minería de datos y EDA (EN CURSO)
- [x] Extracción y carga del dataset REFIT
- [x] Inspección inicial: estructura, tipos, rango temporal, nulos, duplicados
- [ ] Limpieza: valores nulos, duplicados, outliers
- [ ] Análisis exploratorio: patrones temporales, correlaciones, distribuciones
- [ ] Feature engineering: variables temporales, lags, medias móviles
- [ ] Remuestreo a 1 minuto (de los 8 segundos originales)

### FASE 2 — Modelado y comparativa
- [ ] Baseline: media histórica y última observación conocida
- [ ] Modelos clásicos: ARIMA/SARIMA, XGBoost, Random Forest, LightGBM
- [ ] Redes neuronales: LSTM, posiblemente Transformers
- [ ] Métricas: RMSE, MAE, MAPE, R²
- [ ] Validación temporal estricta (walk-forward, nunca aleatoria)
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

---

## HALLAZGOS EDA INICIAL (Sesión 2 — 2026-04-11)

- House1: 6.96M registros, oct 2013 – jul 2015, media 481W, Issues=1: 0.84%
- House2: 5.73M registros, sep 2013 – may 2015, media 465W, Issues=1: 0.50%
- House3: 6.99M registros, sep 2013 – jun 2015, media 679W, Issues=1: 5.84% ⚠️
- Intervalo real de muestreo: 7 segundos (no 8 como indica la documentación)
- House3 máximo: 65,836W — outlier severo, físicamente inverosímil ⚠️
- House3 Issues=1 elevado — pendiente decidir estrategia: descartar o imputar
- 8 figuras exportadas a resultados/figuras/
- CSV resumen exportado a resultados/metricas/

### DECISIONES PENDIENTES
- Estrategia de tratamiento de Issues=1 en House3
- Estrategia de tratamiento de outliers severos (especialmente House3)

---
*Este archivo debe leerse al inicio de cada nueva sesión de trabajo.*
