# Hallazgos: Limpieza y EDA de Hogares Adicionales

**Fecha:** 2026-05-06  
**Notebooks ejecutados:** Nb03 (Houses 4, 5, 11 vía script), Nb05 (Strathclyde), Nb06 (EDA Strathclyde)  
**Fase del proyecto:** Cierre de Fase 1 (EDA y preparación de datos)

---

## Contexto

Este documento recoge los hallazgos de la segunda ampliación del conjunto de hogares,
motivada por el riesgo de sesgo de representatividad identificado en la reunión de tutoría.
El proceso amplia el dataset de entrenamiento desde los 2 hogares originales (Houses 1 y 3)
hasta un conjunto mucho más diverso proveniente de dos fuentes:

- **Zenodo CLEAN** (formato con cabecera, columna Issues): Houses 4, 5, 11
- **Strathclyde Power Data** (formato sin cabecera, sin Issues): Houses 6–21 exc. 14

La decisión y su justificación están documentadas en `05_decision_ampliacion_hogares.md`.

---

## 1. Houses 4, 5, 11 — Formato Zenodo CLEAN

### 1.1 Pipeline aplicado

Idéntico al Notebook 03 (Houses 1, 2, 3):
1. Eliminación de filas con `Issues = 1`
2. Outliers `Aggregate > 15.000 W` → NaN
3. Resampleo a 1 minuto (media aritmética)
4. Interpolación lineal de gaps ≤ 30 minutos

Script utilizado: `src/utils/limpiar_houses_4_5_11.py`

### 1.2 Resultados de limpieza

*(Tabla generada automáticamente por el script — valores reales del CSV `03b_resumen_limpieza_houses4511.csv`)*

| Hogar   | Filas raw | Issues=1 elim. | Outliers elim. | Filas 1min | NaN% antes interp. | NaN% final | Media (W) | Máx (W) | Apto training |
|---------|-----------|----------------|----------------|------------|-------------------|------------|-----------|---------|---------------|
| House4  | 6.760.511 | 67.441 (1,01%) | 16             | 912.939    | 14,05%            | **11,63%** | 381,7     | 11.705,6 | ✓ Sí         |
| House5  | 7.430.755 | 425.766 (6,08%)| 28             | 933.593    | 13,25%            | **8,38%**  | 733,2     | 13.554,9 | ✓ Sí         |
| House11 | 4.431.541 | 40.114 (0,91%) | 8              | 564.697    | 11,38%            | **10,67%** | 455,8     | 6.872,6  | ✓ Sí         |

### 1.3 Observaciones específicas

- **House4** (381,7 W media): consumo medio notablemente inferior al resto. Es coherente
  con el perfil documentado (pareja, uno teletrabaja) si el hogar es eficiente o pequeño.
  Issues=1 al 1,01% — nivel normal, similar a House1.

- **House5** (733,2 W media): el consumo más alto de los tres hogares, coherente con una
  familia de 4 personas. Issues=1 al 6,08% — nivel elevado similar a House3 (5,84%).
  NaN final del 8,38%, el mejor de los tres: datos de alta calidad.

- **House11** (455,8 W media, max=6.872 W): consumo máximo significativamente inferior
  al resto (máx 6.873 W vs ~11.000–13.000 W de las otras). Coherente con una persona sola
  en piso moderno con menor potencia contratada o electrodomésticos de menor potencia.
  Período más corto: solo 564.697 filas a 1 min (~392 días) frente a ~900.000 de los otros.

---

## 2. Houses 6–21 (exc. 14) — Formato Strathclyde

### 2.1 Diferencias de formato y adaptaciones del pipeline

El formato Strathclyde (`REFITPowerData111215.7z`, diciembre 2015) difiere del Zenodo CLEAN:

| Aspecto | Adaptación aplicada |
|---------|---------------------|
| Sin cabecera | Columnas asignadas: `['Unix','Aggregate','Appliance1',...,'Appliance9']` |
| Sin columna `Time` | Derivada de Unix: `pd.to_datetime(df['Unix'], unit='s')` |
| Sin columna `Issues` | El umbral físico 15.000 W actúa como filtro equivalente |
| Duplicados de timestamp | Eliminados con `df[~df.index.duplicated(keep='first')]` |

El resto del pipeline (outliers, resampleo 1 min, interpolación ≤ 30 min) es **idéntico**.

### 2.2 Resultados de limpieza (Notebook 05)

*(Valores reales en `resultados/metricas/05_resumen_limpieza_strathclyde.csv`)*

| Hogar    | Inicio     | Fin        | Días | Filas 1min | Outliers | NaN% antes | NaN% final  | Media (W) | Máx (W)  | Apto   |
|----------|------------|------------|------|------------|----------|------------|-------------|-----------|----------|--------|
| House6   | 2013-11-28 | 2015-06-28 | 577  | 831.420    | 32       | 15,13%     | **14,71%**  | 480,4     | 8.121,2  | ✓ Sí   |
| House7   | 2013-11-01 | 2015-07-08 | 613  | 882.910    | 35       | 12,45%     | **12,20%**  | 562,0     | 11.069,9 | ✓ Sí   |
| House8   | 2013-11-01 | 2015-05-10 | 555  | 799.224    | 1.176    | 10,12%     | **9,89%**   | 681,9     | 14.870,0 | ✓ Sí   |
| House9   | 2013-12-17 | 2015-07-08 | 568  | 817.947    | 15       | 15,28%     | **15,08%**  | 575,6     | 13.776,6 | ✓ Sí   |
| House10  | 2013-11-20 | 2015-06-30 | 586  | 845.197    | 36       | 11,13%     | **8,94%**   | 759,5     | 9.643,1  | ✓ Sí   |
| House12  | 2014-03-07 | 2015-07-08 | 487  | 702.139    | 1        | 6,82%      | **6,21%**   | 371,0     | 8.779,3  | ✓ Sí   |
| House13  | 2014-01-17 | 2015-05-31 | 498  | 717.821    | 103      | 22,76%     | **21,27%** ⚠️| 560,8   | 11.110,0 | ✗ No   |
| House15  | 2013-12-17 | 2015-07-08 | 567  | 816.947    | 0        | 13,64%     | **11,72%**  | 255,3     | 8.662,0  | ✓ Sí   |
| House16  | 2014-01-10 | 2015-07-08 | 543  | 782.773    | 227      | 17,33%     | **15,31%**  | 556,8     | 11.453,0 | ✓ Sí   |
| House17  | 2014-03-06 | 2015-06-19 | 469  | 676.650    | 105      | 5,98%      | **5,75%**   | 406,3     | 13.004,0 | ✓ Sí   |
| House18  | 2014-03-07 | 2015-05-24 | 443  | 637.922    | 242      | 5,80%      | **5,63%**   | 446,8     | 11.553,6 | ✓ Sí   |
| House19  | 2014-03-06 | 2015-06-20 | 470  | 677.410    | 0        | 6,33%      | **5,75%**   | 291,0     | 7.571,2  | ✓ Sí   |
| House20  | 2014-03-20 | 2015-06-23 | 460  | 662.804    | 29       | 5,92%      | **5,79%**   | 375,9     | 7.321,1  | ✓ Sí   |
| House21  | 2014-03-07 | 2015-07-10 | 489  | 705.337    | 13       | 9,24%      | **9,01%**   | 637,8     | 8.075,2  | ✓ Sí   |

### 2.3 Observaciones específicas

- **Sin valores negativos** en ninguna de las 14 casas Strathclyde. La versión Power Data
  de diciembre 2015 ya había pasado por un filtro básico previo a su publicación.

- **House8** tiene 1.176 outliers (el máximo del grupo) y un pico de 14.870 W,
  rozando el umbral de 15.000 W. Aun así queda dentro del rango físicamente plausible.

- **House13 excluida** (NaN=21,27%): supera el umbral por apenas 1,3 puntos. Sus datos
  muestran un patrón de huecos más concentrado que el resto. Queda disponible para
  validación adicional si se necesita.

- **House15 con consumo muy bajo** (media 255,3 W): el hogar de menor consumo del
  dataset completo. Posible hogar desocupado parcialmente o con muy pocos ocupantes.
  Es un caso de interés para el modelo por representar el extremo inferior del rango.

- **Houses 17–20**: período de monitorización más corto (~443–470 días) al comenzar
  en marzo 2014, frente a los ~577–613 días de las casas que empezaron en nov–dic 2013.

- **House10** (media 759,5 W): el mayor consumo medio del grupo Strathclyde, coherente
  con un hogar de 4–5 ocupantes.

### 2.4 Criterio de selección

Se aplica el mismo umbral que se usó para excluir House2 del entrenamiento:

- **NaN final ≤ 20%** → apta para entrenamiento
- **NaN final > 20%** → excluida del entrenamiento, puede usarse como validación adicional

---

## 3. EDA condensado — Casas Strathclyde aptas (Notebook 06)

### 3.1 Estadísticas descriptivas

*(Fuente: `resultados/metricas/06_estadisticos_strathclyde.csv`)*

| Hogar | Media (W) | Mediana (W) | Std (W) | P25 (W) | P75 (W) | Asimetría | Curtosis |
|-------|-----------|------------|---------|---------|---------|-----------|----------|
| H6    | 480,4     | 369,7      | 427,3   | 258,2   | 555,9   | 4,727     | 29,113   |
| H7    | 562,0     | 226,9      | 808,7   | 162,0   | 558,7   | 3,092     | 11,559   |
| H8    | 681,9     | 261,8      | 1.096,0 | 203,8   | 748,2   | 5,269     | 42,753   |
| H9    | 575,6     | 208,7      | 933,5   | 171,6   | 560,2   | 4,556     | 29,219   |
| H10   | 759,5     | 432,8      | 833,3   | 269,4   | 793,2   | 2,506     | 7,789    |
| H12   | 371,0     | 169,0      | 584,0   | 151,4   | 309,6   | 4,164     | 20,125   |
| H15   | 255,3     | 179,4      | 330,2   | 159,2   | 243,4   | 7,387     | **65,427** |
| H16   | 556,8     | 355,0      | 623,0   | 256,9   | 556,4   | 3,656     | 17,584   |
| H17   | 406,3     | 234,0      | 743,0   | 139,0   | 329,5   | 7,268     | **77,015** |
| H18   | 446,8     | 360,2      | 463,3   | 227,0   | 514,9   | 5,565     | 48,249   |
| H19   | 291,0     | 191,6      | 346,2   | 157,8   | 289,7   | 6,187     | 50,137   |
| H20   | 375,9     | 266,6      | 432,1   | 202,4   | 407,4   | 4,721     | 27,767   |
| H21   | 637,8     | 281,0      | 671,9   | 182,6   | 950,1   | 1,614     | 2,621    |

**Observaciones clave:**

- **Distribuciones fuertemente asimétricas en todos los hogares** (asimetría > 1,6 en los 13).
  Confirma el patrón de Houses 1–3 (Nb04): la distribución de consumo eléctrico doméstico
  nunca es normal — siempre presenta cola derecha por los picos esporádicos.

- **Curtosis extrema en H15 (65,4) y H17 (77,0):** distribuciones muy leptocúrticas con
  picos de consumo muy concentrados en valores bajos y colas muy pesadas. H15 en particular
  (media 255 W, la más baja del dataset) sugiere un hogar casi siempre vacío con destellos
  de consumo esporádico intenso.

- **House 21 es el caso más "regular"** (asimetría 1,6, curtosis 2,6): la distribución
  más cercana a la normalidad del dataset completo. Consumo más continuo y estable.

- **Diferencia media–mediana amplia en H7, H8, H9, H12:** la mediana es menos de la
  mitad de la media (p.ej. H7: 226,9 W vs 562,0 W). Indica que el hogar consume poco
  la mayor parte del tiempo pero tiene picos muy elevados frecuentes (posiblemente
  cocina eléctrica, calefacción eléctrica o vehículo eléctrico).

- **H10 con la distribución más simétrica de los Strathclyde** (asimetría 2,5): consumo
  más distribuido a lo largo del día, coherente con mayor ocupación y mayor número de
  electrodomésticos encendidos simultáneamente.

### 3.2 Perfiles de consumo

*(Ver figuras `06_perfil_diario_strathclyde.png` y `06_perfil_semanal_strathclyde.png`)*

Los perfiles horarios (laborable vs. fin de semana) muestran los patrones esperados en
hogares domésticos del Reino Unido:

- **Pico matutino** (7–9h): encendido de electrodomésticos al despertar (hervidor, tostadora,
  luces). Más pronunciado en días laborables.
- **Valle diurno** (10–16h): hogares desocupados durante la jornada laboral. Las casas con
  ocupantes en casa (teletrabajo, jubilados, familias) tienen este valle menos marcado.
- **Pico vespertino** (17–21h): vuelta a casa, cocina, televisión, lavadora. El más elevado
  del día en la mayoría de hogares.
- **Diferencia laborable/fin de semana:** en fines de semana el pico matutino aparece
  desplazado 1–2 horas más tarde y el valle diurno desaparece o se reduce significativamente.

### 3.3 Feature engineering — Resultados

*(Fuente: `resultados/metricas/06_features_correlacion_strathclyde.csv`)*

Se aplica el **catálogo unificado de 36 features** idéntico al Notebook 04:

| Grupo | n | Features |
|-------|---|---------|
| Temporales | 9 | hora, dia_semana, dia_mes, mes, anio, semana_anio, dia_anio, trimestre, parte_dia |
| Binarias | 3 | es_fin_semana, es_festivo_uk, es_laboral |
| Cíclicas sin/cos | 8 | hora, dia_semana, mes, dia_anio |
| Lags | 8 | lag_1, 5, 15, 30, 60, 120, 1440, 10080 |
| Rolling media+std | 8 | ventanas 15, 60, 240, 1440 min |

**Correlación de features con Aggregate — top 2 por hogar:**

| Hogar | Top 1 feature | r    | Top 2 feature    | r    |
|-------|--------------|------|-----------------|------|
| H6    | lag_1        | 0,779 | rolling_mean_15 | 0,671 |
| H7    | lag_1        | 0,924 | rolling_mean_15 | 0,794 |
| H8    | lag_1        | 0,878 | rolling_mean_15 | 0,706 |
| H9    | lag_1        | 0,913 | rolling_mean_15 | 0,763 |
| H10   | lag_1        | 0,922 | rolling_mean_15 | 0,857 |
| H12   | lag_1        | 0,893 | rolling_mean_15 | 0,718 |
| H15   | lag_1        | 0,876 | rolling_mean_15 | 0,761 |
| H16   | lag_1        | 0,871 | rolling_mean_15 | 0,754 |
| H17   | lag_1        | 0,857 | rolling_mean_15 | 0,682 |
| H18   | lag_1        | 0,915 | rolling_mean_15 | 0,730 |
| H19   | lag_1        | 0,786 | rolling_mean_15 | 0,660 |
| H20   | lag_1        | 0,805 | rolling_mean_15 | 0,686 |
| H21   | lag_1        | 0,936 | rolling_mean_15 | 0,851 |

**Hallazgo clave: `lag_1` es la feature más correlacionada en los 13 hogares** (r entre 0,779
y 0,936). Confirma el patrón observado en Nb04 para Houses 1–3: el consumo del minuto
anterior explica gran parte del consumo actual (inercia térmica y de uso). La segunda feature
es invariablemente `rolling_mean_15` (media móvil de 15 minutos).

Este resultado valida el catálogo de 36 features como representativo para todo el dataset REFIT
independientemente de las características específicas de cada hogar.

**NaN introducidos por lag_10080 (7 días):**
- Rango: 41.143 (H17, período corto) a 133.351 (H9, período largo desde dic 2013)
- Estrategia confirmada: eliminar las primeras 10.080 filas de cada serie antes de entrenar

**Archivos de features generados** (13 casas × ~300 MB c/u):
H6, H7, H8, H9, H10, H12, H15, H16, H17, H18, H19, H20, H21 → `datos/processed/house{N}_features.csv`

> **Pendiente:** Features de H4, H5 y H11 (Zenodo CLEAN) — requieren ejecutar
> el equivalente al Notebook 04 sobre sus datos procesados.

---

## 4. Tabla final de selección de hogares para modelado

*(Tabla definitiva en `resultados/metricas/06_seleccion_hogares_final.csv`)*

| Hogar   | Fuente | NaN% | Uso en modelado |
|---------|--------|------|-----------------|
| House1  | Zenodo CLEAN | 12,03% | **Entrenamiento** |
| House2  | Zenodo CLEAN | 23,69% | Validación externa |
| House3  | Zenodo CLEAN | 12,43% | **Entrenamiento** |
| House4  | Zenodo CLEAN | 11,63% | **Entrenamiento** ✓ |
| House5  | Zenodo CLEAN | 8,38%  | **Entrenamiento** ✓ |
| House11 | Zenodo CLEAN | 10,67% | **Entrenamiento** ✓ |
| House6  | Strathclyde | 14,71% | **Entrenamiento** ✓ |
| House7  | Strathclyde | 12,20% | **Entrenamiento** ✓ |
| House8  | Strathclyde | 9,89%  | **Entrenamiento** ✓ |
| House9  | Strathclyde | 15,08% | **Entrenamiento** ✓ |
| House10 | Strathclyde | 8,94%  | **Entrenamiento** ✓ |
| House12 | Strathclyde | 6,21%  | **Entrenamiento** ✓ |
| House13 | Strathclyde | 21,27% | Excluido — validación adicional |
| House15 | Strathclyde | 11,72% | **Entrenamiento** ✓ |
| House16 | Strathclyde | 15,31% | **Entrenamiento** ✓ |
| House17 | Strathclyde | 5,75%  | **Entrenamiento** ✓ |
| House18 | Strathclyde | 5,63%  | **Entrenamiento** ✓ |
| House19 | Strathclyde | 5,75%  | **Entrenamiento** ✓ |
| House20 | Strathclyde | 5,79%  | **Entrenamiento** ✓ |
| House21 | Strathclyde | 9,01%  | **Entrenamiento** ✓ |

**Resumen cuantitativo:**
- Total hogares disponibles en el dataset REFIT: 20 (Houses 1–21, sin House 14)
- **Hogares para entrenamiento: 18** (H1, H3, H4, H5, H11 + H6, H7, H8, H9, H10, H12, H15, H16, H17, H18, H19, H20, H21)
- **Hogares para validación externa: 2** (H2 Zenodo: 23,69% NaN; H13 Strathclyde: 21,27% NaN)
- Rango de NaN en hogares de entrenamiento: 5,63% (H18) – 15,31% (H16)
- Consumo medio de entrenamiento: 255 W (H15, mínimo) – 759 W (H10, máximo)

> Tabla completa y definitiva. Todos los valores son reales obtenidos de los pipelines
> de limpieza ejecutados el 2026-05-06.

---

## 5. Decisiones técnicas derivadas

| Decisión | Justificación |
|----------|---------------|
| Mismo umbral NaN (20%) para Strathclyde que para Zenodo | Criterio consistente y justificable en la memoria |
| No repetir ACF/PACF/ADF para cada nueva casa | Patrones estadísticos documentados en Nb04 son representativos del dataset REFIT |
| Catálogo de 36 features idéntico para todas las casas | Garantiza comparabilidad en fase de modelado |
| Primeras 10.080 filas descartadas por lag_10080 | Mismo criterio que Nb04 — evita NaN propagados |

---

## 6. Archivos generados

### Scripts y notebooks
- `src/utils/limpiar_houses_4_5_11.py` — script de limpieza Houses 4, 5, 11
- `notebooks/05_inspeccion_limpieza_strathclyde.ipynb` — limpieza batch 14 casas
- `notebooks/06_eda_features_strathclyde.ipynb` — EDA condensado + features

### Datos procesados (`datos/processed/`)
- `house4_1min_limpio.csv`, `house5_1min_limpio.csv`, `house11_1min_limpio.csv`
- `house{6,7,8,9,10,12,13,15,16,17,18,19,20,21}_1min_limpio.csv`
- `house{N}_features.csv` (36 features) para casas aptas

### Métricas (`resultados/metricas/`)
- `03b_resumen_limpieza_houses4511.csv`
- `05_resumen_limpieza_strathclyde.csv`
- `05_resumen_inspeccion_strathclyde.csv`
- `06_estadisticos_strathclyde.csv`
- `06_features_correlacion_strathclyde.csv`
- `06_seleccion_hogares_final.csv`

### Figuras (`resultados/figuras/`)
- `05_nan_por_hogar_strathclyde.png`
- `05_comparativa_limpieza_strathclyde.png`
- `05_consumo_por_hogar_strathclyde.png`
- `06_perfil_diario_strathclyde.png`
- `06_perfil_semanal_strathclyde.png`
- `06_features_correlacion_strathclyde.png`

---

*Documento creado y completado el 2026-05-06.*  
*Houses 4, 5, 11: valores reales del script `limpiar_houses_4_5_11.py` (completado 18:32h).*  
*Houses 6–21: valores reales del Notebook 05 (completado ~18:35h).*  
*Nb06 (EDA + features Strathclyde): completado. Todas las secciones contienen valores reales.*  
*Pendiente: features de H4, H5, H11 (equivalente Nb04 para hogares Zenodo adicionales).*
