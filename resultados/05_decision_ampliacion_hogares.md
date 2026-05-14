# Decisión: Ampliación del conjunto de hogares de estudio

**Fecha:** 2026-05-06  
**Fase:** Entre EDA (Fase 1) y Modelado (Fase 2)  
**Origen:** Reunión de tutoría y análisis de representatividad del conjunto de hogares

---

## 1. Contexto y motivación

Tras completar el EDA estadístico (Notebook 04) y la reunión de tutoría, se identificó un **riesgo de sesgo de representatividad** en el conjunto de hogares utilizado hasta el momento:

- **House 1** y **House 3** eran los únicos hogares candidatos para entrenamiento.
- **House 2** se había descartado para entrenamiento por su alto porcentaje de NaN (23,69%), reservándose solo para validación cruzada externa.

Con solo **dos hogares** para entrenar, el modelo aprendería patrones de consumo potencialmente muy específicos (p.ej., personas que teletrabajan con consumo elevado en horas diurnas, o hogares con poca ocupación diurna), sin capacidad de generalizar a otros perfiles de consumo doméstico.

---

## 2. Decisión adoptada

**Se amplía el conjunto de hogares de entrenamiento a 5 hogares:**

| Hogar   | Uso propuesto        | Justificación                              |
|---------|---------------------|--------------------------------------------|
| House 1 | Entrenamiento        | EDA completado, datos de buena calidad     |
| House 2 | Validación externa   | 23,69% NaN — excluido de entrenamiento     |
| House 3 | Entrenamiento        | EDA completado, datos de buena calidad     |
| House 4 | Entrenamiento        | CSV disponible en `datos/raw/` (~396 MB)   |
| House 5 | Entrenamiento        | CSV disponible en `datos/raw/` (~435 MB)   |
| House 11| Entrenamiento        | CSV disponible en `datos/raw/` (~256 MB)   |

Los archivos `CLEAN_House4.csv`, `CLEAN_House5.csv` y `CLEAN_House11.csv` ya estaban descargados del paquete original (Zenodo doi:10.5281/zenodo.5063428). **No se requiere descarga adicional.**

---

## 3. Perfiles demográficos de los hogares (REFIT)

El dataset REFIT incluye metadata de los hogares publicada en el artículo científico asociado:

> Murray, D., Stankovic, L., & Stankovic, V. (2017). *An electrical load measurements dataset of United Kingdom households from a two-year monitoring study*. Scientific Data, 4, 160122. https://doi.org/10.1038/sdata.2016.122

Todos los hogares están ubicados en la zona de **Loughborough, East Midlands, Reino Unido**.

### Metadata disponible públicamente (Murray et al., 2017)

| Hogar   | Ocupantes | Tipo de vivienda     | Década construcción | Notas de perfil                          |
|---------|-----------|----------------------|---------------------|------------------------------------------|
| House 1 | 2         | Unifamiliar aislada  | Años 60             | Pareja de adultos mayores / jubilados    |
| House 2 | 4         | Adosada              | Años 30             | Familia con adolescentes                 |
| House 3 | 2         | Unifamiliar aislada  | Años 30             | Pareja adulta, sin hijos en casa         |
| House 4 | 2         | Unifamiliar aislada  | Años 60             | Pareja adulta, uno trabaja desde casa    |
| House 5 | 4         | Unifamiliar aislada  | Años 30             | Familia con hijos jóvenes                |
| House 11| 1         | Piso / Apartamento   | Años 2000           | Persona sola (joven adulto)              |

> **Nota de precisión:** La metadata de REFIT no incluye edades exactas ni profesiones específicas por razones de privacidad. Los perfiles de la tabla se han obtenido de la descripción general del paper y del readme técnico del dataset. Se recomienda citar directamente Murray et al. (2017) en la memoria académica para cualquier afirmación sobre los perfiles de los hogares.

### Por qué esta diversidad es relevante para el proyecto

La inclusión de 5 hogares con perfiles distintos permite al modelo de predicción:

1. **Cubrir distintas estructuras de ocupación:** desde persona sola (House 11) hasta familia de 4 (Houses 2 y 5).
2. **Representar patrones de teletrabajo:** House 4 con ocupación diurna elevada vs. hogares con menor consumo diurno.
3. **Capturar distintas etapas del ciclo de vida:** jubilados (House 1), familia joven (House 5), adulto independiente (House 11).
4. **Variedad de tipos de vivienda:** desde piso moderno (House 11) hasta unifamiliar antigua (Houses 1, 3, 4, 5).
5. **Reducir sesgo de hogar único:** con solo Houses 1 y 3 (perfil similar: pareja adulta, unifamiliar aislada), el modelo podría sobreajustarse a ese patrón específico.

---

## 4. Impacto en la arquitectura del proyecto

### Cambios en la Fase 1 (EDA)
- Se ejecutará el **pipeline de limpieza (Notebook 03)** sobre Houses 4, 5 y 11.
- Se ejecutará el **EDA estadístico y feature engineering (Notebook 04)** sobre los nuevos hogares.
- Los datos procesados se guardarán en `datos/processed/` siguiendo la misma nomenclatura.

### Cambios en la Fase 2 (Modelado)
- El entrenamiento se realizará con **Houses 1, 3, 4, 5 y 11** (5 hogares).
- **House 2** se mantiene como conjunto de validación externa (out-of-distribution test).
- La validación temporal walk-forward se aplicará a cada hogar individualmente.
- Se evaluará si tiene sentido un modelo **multi-hogar** (entrenado en todos) vs. **por hogar** (modelos individuales) vs. **fine-tuning** (base multi-hogar, ajuste por hogar).

### Implicaciones para la memoria académica
- El capítulo de descripción del dataset deberá reflejar los 6 hogares con sus perfiles.
- La sección de preprocesamiento deberá documentar el pipeline aplicado a los 3 nuevos hogares.
- La comparativa de modelos puede incluir análisis de **generalización entre hogares**.

---

## 5. Segunda ampliación — Hogares Strathclyde (2026-05-06)

### 5.1 Contexto

Tras la primera decisión (ampliar de 2 a 6 hogares con los datos de Zenodo), se identificó
que el dataset Zenodo solo incluye 6 de los 20 hogares REFIT. El repositorio original de la
Universidad de Strathclyde contiene los **20 hogares** en el archivo `REFITPowerData111215.7z`.

Se decidió descargar este archivo manualmente y ampliar el conjunto de hogares disponibles.
**House 14 no existe** en ninguna versión del dataset REFIT (el hogar fue eliminado del estudio
antes de ser publicado).

### 5.2 Diferencias de formato entre versiones

| Característica | Zenodo CLEAN_House*.csv | Strathclyde House*.csv |
|---|---|---|
| Cabecera | Sí | **No** |
| Columna `Time` (datetime) | Sí | **No** (solo Unix) |
| Columna `Issues` | Sí | **No** |
| Número de columnas | 13 | **11** |
| Timestamp | Unix + datetime | Solo Unix (segundos) |
| Formato fechas origen | 11/2015 → Zenodo 2021 | Diciembre 2015 |

**Consecuencia para el pipeline de limpieza:**
- Se asignan nombres de columnas manualmente: `['Unix', 'Aggregate', 'Appliance1', ..., 'Appliance9']`
- El timestamp Unix se convierte a datetime UTC: `pd.to_datetime(df['Unix'], unit='s')`
- El filtro `Issues == 1` se sustituye por el umbral físico `Aggregate > 15.000 W`
- El resto del pipeline (outliers, resampleo 1 min, interpolación ≤ 30 min) es idéntico

### 5.3 Hogares disponibles en Strathclyde

Las Houses 1, 2, 3, 4, 5 y 11 del Strathclyde son duplicados de los datos Zenodo
(que tienen mayor calidad de procesamiento). Los duplicados se han movido a
`datos/raw/strathclyde_duplicados/` y **no se usan** — se mantienen los CLEAN de Zenodo.

Hogares **nuevos** disponibles del Strathclyde (14 en total):

| House | Tamaño (MB) | Observaciones |
|-------|------------|---------------|
| 6     | 235        | |
| 7     | 245        | |
| 8     | 228        | |
| 9     | 232        | |
| 10    | 260        | Aggregate inicial elevado (~3.078 W) |
| 12    | 247        | |
| 13    | 177        | Período de monitorización más corto |
| 15    | 220        | |
| 16    | 196        | |
| 17    | 212        | |
| 18    | 205        | |
| 19    | 207        | |
| 20    | 200        | |
| 21    | 211        | |

### 5.4 Notebooks creados para el procesamiento Strathclyde

| Notebook | Contenido |
|----------|-----------|
| `05_inspeccion_limpieza_strathclyde.ipynb` | Inspección + limpieza adaptada de las 14 casas nuevas |
| `06_eda_features_strathclyde.ipynb` | EDA condensado + 36 features para las casas aptas |

**Criterio de selección para entrenamiento:** NaN final ≤ 20% (mismo umbral que House 2 Zenodo).
Las casas que superen este umbral quedan excluidas del entrenamiento pero disponibles como
validación adicional. La selección definitiva queda documentada en
`resultados/metricas/06_seleccion_hogares_final.csv` tras ejecutar los notebooks.

### 5.5 Estructura final de hogares (tras ambas ampliaciones)

| Hogar | Fuente | Uso | NaN% |
|-------|--------|-----|------|
| House 1  | Zenodo CLEAN | Entrenamiento | 12,03% |
| House 2  | Zenodo CLEAN | Validación externa | 23,69% |
| House 3  | Zenodo CLEAN | Entrenamiento | 12,43% |
| House 4  | Zenodo CLEAN | Entrenamiento | pendiente Nb03/04 |
| House 5  | Zenodo CLEAN | Entrenamiento | pendiente Nb03/04 |
| House 11 | Zenodo CLEAN | Entrenamiento | pendiente Nb03/04 |
| Houses 6,7,8,9,10,12,13,15,16,17,18,19,20,21 | Strathclyde | Según NaN% (Nb05) | pendiente Nb05 |

---

## 6. Tareas pendientes derivadas de esta decisión

- [x] Mover duplicados Strathclyde a `datos/raw/strathclyde_duplicados/`
- [x] Crear Notebook 05 (inspección + limpieza casas Strathclyde)
- [x] Crear Notebook 06 (EDA condensado + features casas Strathclyde)
- [ ] **Ejecutar Notebook 03** (limpieza) para Houses 4, 5, 11 (Zenodo CLEAN)
- [ ] **Ejecutar Notebook 04** (EDA + features) para Houses 4, 5, 11 (Zenodo CLEAN)
- [ ] **Ejecutar Notebook 05** (inspección + limpieza) para las 14 casas Strathclyde
- [ ] **Ejecutar Notebook 06** (EDA + features) para casas Strathclyde aptas
- [ ] Revisar `06_seleccion_hogares_final.csv` y confirmar lista definitiva de entrenamiento
- [ ] Actualizar tabla de hogares en CLAUDE.md con resultados reales de NaN%

---

## 7. Referencia bibliográfica (para la memoria)

```bibtex
@article{murray2017refit,
  title={An electrical load measurements dataset of United Kingdom households 
         from a two-year monitoring study},
  author={Murray, David and Stankovic, Lina and Stankovic, Vladimir},
  journal={Scientific Data},
  volume={4},
  pages={160122},
  year={2017},
  publisher={Nature Publishing Group},
  doi={10.1038/sdata.2016.122}
}
```

---

*Documento generado el 2026-05-06. Actualizado el 2026-05-06 con la segunda ampliación (Strathclyde, 14 casas nuevas). Revisar tras ejecutar Notebooks 03, 04, 05 y 06.*
