# PFM MUCSI Deusto — Predicción de Consumo Eléctrico en Hogares Inteligentes

**Máster Universitario en Computación y Sistemas Inteligentes (MUCSI)**  
**Universidad de Deusto, Facultad de Ingeniería — Bilbao**  
**Curso académico 2024-2025**

---

## Descripción

Desarrollo de un modelo de aprendizaje automático para la **predicción y 
optimización del consumo eléctrico en entornos domésticos inteligentes**.

El proyecto abarca el ciclo completo de un proyecto de ciencia de datos:
desde la exploración y limpieza del dataset hasta el despliegue de un 
dashboard interactivo, pasando por la comparativa rigurosa de múltiples 
modelos de ML y series temporales.

---

## Dataset

**REFIT Electrical Load Measurements** (versión limpia)  
- Fuente: [Zenodo doi:10.5281/zenodo.5063428](https://doi.org/10.5281/zenodo.5063428)
- 20 hogares del Reino Unido, granularidad de 8 segundos, periodo 2013-2015
- Variables: consumo agregado del hogar + hasta 9 electrodomésticos individuales
- Ficheros de trabajo: `CLEAN_House1.csv`, `CLEAN_House2.csv`, `CLEAN_House3.csv`

---

## Estructura del Proyecto

```
PFM_MUCSI_Deusto/
├── datos/
│   ├── raw/            # CSVs originales sin modificar (no versionar si >100MB)
│   └── processed/      # Datos limpios y features engineered
├── notebooks/          # Jupyter Notebooks numerados por fase
│   ├── 01_inspeccion_inicial.ipynb
│   ├── 02_limpieza_datos.ipynb
│   ├── 03_eda_exploratorio.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_modelos_baseline.ipynb
│   ├── 06_modelos_clasicos.ipynb
│   └── 07_redes_neuronales.ipynb
├── src/
│   └── utils/          # Funciones auxiliares reutilizables
├── modelos/            # Modelos entrenados (.pkl, .h5)
├── resultados/
│   ├── figuras/        # Gráficos exportados (.png, .pdf)
│   └── metricas/       # Resultados de evaluación (.csv)
├── memoria_latex/      # Memoria académica en LaTeX
├── dashboard/          # Aplicación Streamlit
├── CLAUDE.md           # Contexto del proyecto para el asistente IA
├── requirements.txt    # Dependencias Python
└── .gitignore
```

---

## Fases del Proyecto

| Fase | Descripción                          | Estado     |
|------|--------------------------------------|------------|
| 1    | Minería de datos y EDA               | En curso   |
| 2    | Modelado y comparativa de modelos    | Pendiente  |
| 3    | Dashboard + Memoria académica        | Pendiente  |

---

## Instalación y Ejecución

### 1. Requisitos previos

- Python 3.10 o superior (probado con 3.14.0)
- Git

### 2. Clonar el repositorio

```bash
git clone <url-repositorio>
cd PFM_MUCSI_Deusto
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Lanzar Jupyter

```bash
jupyter lab
```

Abre los notebooks en orden numérico desde la carpeta `notebooks/`.

### 5. Dashboard (Fase 3)

```bash
cd dashboard
streamlit run app.py
```

---

## Convenciones del Proyecto

- **Reproducibilidad:** semilla fija `SEMILLA = 42` en todos los experimentos
- **Idioma del código:** comentarios y nombres de variables en español
- **Notebooks:** autocontenidos, ejecutables de arriba a abajo sin errores
- **Validación:** estrictamente temporal (walk-forward), nunca aleatoria

---

## Librerías Principales

Ver `requirements.txt` para versiones exactas.

| Librería     | Uso                                      |
|--------------|------------------------------------------|
| pandas       | Manipulación de datos y series temporales|
| numpy        | Operaciones numéricas                    |
| matplotlib   | Visualizaciones base                     |
| seaborn      | Visualizaciones estadísticas             |
| scikit-learn | Modelos clásicos de ML                   |
| statsmodels  | ARIMA/SARIMA y tests estadísticos        |
| xgboost      | Gradient boosting (XGBoost)              |
| lightgbm     | Gradient boosting (LightGBM)             |
| tensorflow   | Redes neuronales (LSTM)                  |
| streamlit    | Dashboard interactivo                    |
| jupyter      | Entorno de notebooks                     |

---

## Licencia

Proyecto académico — Universidad de Deusto, 2025.  
Dataset REFIT bajo licencia Creative Commons Attribution 4.0 International.
