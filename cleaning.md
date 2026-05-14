# Limpieza de Datos — Dataset REFIT

**Proyecto Fin de Máster — MUCSI, Universidad de Deusto**  
**Notebook de referencia:** `notebooks/03_limpieza_datos.ipynb`  
**Datos de entrada:** `datos/raw/CLEAN_House{1,2,3}.csv`  
**Datos de salida:** `datos/processed/house{1,2,3}_1min_limpio.csv`

---

## Errores identificados

El análisis exploratorio inicial (Notebook 01) detectó cuatro tipos de problemas en el dataset REFIT:

| Problema | House1 | House2 | House3 | Severidad |
|---|---|---|---|---|
| Registros con `Issues=1` | 0.84% | 0.50% | 5.84% | ⚠️ Alta en House3 |
| Outliers en `Aggregate` | max 29,159 W | max 24,595 W | max 65,836 W | ⚠️ Crítico en House3 |
| Intervalo de muestreo irregular | ~7 s (doc. dice 8 s) | ~7 s | ~7 s | Baja |
| NaN post-remuestreo | — | — | — | Dependiente de los anteriores |

---

## Decisiones de diseño

### ¿Por qué eliminar Issues=1 en lugar de imputar?

El flag `Issues=1` en el dataset REFIT indica que el sensor tuvo un problema de medición real:
pérdida de comunicación, lectura inconsistente o ausencia de datos en algún electrodoméstico.
La causa no es un artefacto estadístico sino un fallo de hardware, por lo que imputar esos
valores introduciría datos fabricados sin base real. Eliminar las filas afectadas es más honesto
académicamente y el impacto es mínimo en House1 (0.84%) y House2 (0.50%).

Para **House3 (5.84%)** se analizó previamente la distribución temporal de los Issues=1 para
verificar que no están concentrados en un período concreto (lo que obligaría a descartar ese
período completo). Al estar distribuidos uniformemente a lo largo de los dos años, se aplica
la misma estrategia de eliminación individual de filas.

### ¿Por qué un umbral de 15.000 W para outliers?

El suministro doméstico estándar en el Reino Unido es de 100A × 230V = **23.000 W** como
máximo teórico absoluto. En la práctica, un hogar doméstico típico no supera 10.000–12.000 W
de consumo simultáneo (cocina eléctrica ~7 kW + caldera ~6 kW + resto de electrodomésticos).

Se eligió **15.000 W** como umbral conservador que:
- Está por debajo del límite físico real de la instalación
- Cubre cualquier pico legítimo de consumo doméstico
- Excluye claramente lecturas imposibles como el máximo de House3 (65.836 W)

Los valores que superan el umbral se reemplazan por `NaN` — no se eliminan las filas —
para ser tratados en la etapa de imputación.

### ¿Por qué el umbral de 30 minutos para imputación?

La interpolación lineal es válida para rellenar huecos cortos en series de consumo eléctrico
siempre que el comportamiento durante el hueco sea razonablemente predecible por los valores
adyacentes. Un gap de 30 minutos es coherente con un reinicio del sensor o una interrupción
breve de comunicación. Por encima de 30 minutos, los patrones de comportamiento del hogar
pueden haber cambiado (encendido o apagado de electrodomésticos) y la interpolación lineal
ya no es una aproximación razonable.

Este umbral de 30 minutos es el criterio de referencia en la literatura de NILM/NALM
(Kelly & Knottenbelt, 2015; Batra et al., 2014).

---

## Pasos del proceso de limpieza

### Paso 1 — Eliminación de registros Issues=1

**Qué se hizo:** Se eliminaron todas las filas donde la columna `Issues` tiene valor 1.

**Código clave:**
```python
df_limpio = df[df['Issues'] == 0].copy()
```

**Resultado:**

| Hogar | Eliminados | % eliminado |
|---|---|---|
| House1 | 58.183 filas | 0.84% |
| House2 | 28.444 filas | 0.50% |
| House3 | 408.627 filas | 5.84% |

---

### Paso 2 — Tratamiento de outliers en Aggregate

**Qué se hizo:** Los valores de `Aggregate` superiores a 15.000 W se reemplazaron por `NaN`.
Solo se aplicó a la columna `Aggregate` (objetivo del modelo). Los electrodomésticos
individuales tienen rangos máximos de ~4.000 W y no requieren este umbral.

**Código clave:**
```python
UMBRAL_OUTLIER_W = 15_000
df.loc[df['Aggregate'] > UMBRAL_OUTLIER_W, 'Aggregate'] = np.nan
```

**Resultado:**

| Hogar | Outliers detectados | % sobre total |
|---|---|---|
| House1 | Muy pocos (< 0.001%) | Residual |
| House2 | Muy pocos (< 0.001%) | Residual |
| House3 | Varios (65.836 W era el máximo) | < 0.01% |

---

### Paso 3 — Remuestreo a 1 minuto

**Qué se hizo:** Se agregaron los registros de ~7 segundos a ventanas de 1 minuto
usando la **media aritmética**. Solo se conservaron las columnas de consumo
(`Aggregate` + `Appliance1`–`Appliance9`). Las columnas `Unix`, `Issues` y `hogar`
se descartaron, ya que no son necesarias para el modelado.

**Código clave:**
```python
df_1min = df[COLS_CONSUMO].resample('1min').mean()
```

**Resultado:**

| Hogar | Filas originales | Filas tras resample | Factor de reducción |
|---|---|---|---|
| House1 | ~6.9M | ~920K | ~7.6× |
| House2 | ~5.7M | ~760K | ~7.5× |
| House3 | ~6.6M | ~890K | ~7.4× |

Los minutos donde no hay ningún registro en los datos originales quedan como `NaN`
(gaps heredados de los datos raw, más los outliers reemplazados en el paso 2).

---

### Paso 4 — Imputación de NaN post-remuestreo

**Qué se hizo:** Se aplicó **interpolación lineal** a los bloques de `NaN` consecutivos
con longitud ≤ 30 minutos. Los gaps más largos se mantuvieron como `NaN`.
La imputación se aplicó a todas las columnas de consumo simultáneamente.

**Código clave:**
```python
UMBRAL_GAP_MIN = 30  # minutos
serie_final = serie.interpolate(
    method='linear',
    limit=UMBRAL_GAP_MIN,
    limit_area='inside'
)
```

El parámetro `limit_area='inside'` previene que se extrapolen valores más allá
del inicio o el final de la serie (solo se rellenan NaN entre dos valores conocidos).

**Resultado:**

| Hogar | NaN antes imput. | NaN imputados | NaN restantes | % NaN final |
|---|---|---|---|---|
| House1 | 119.993 | 9.313 | 110.680 | 12,03% |
| House2 | 219.633 | 8.989 | 210.644 | **23,69% ⚠️** |
| House3 | 136.345 | 26.339 | 110.006 | 12,43% |

> **Nota sobre House2:** el 23,69% de NaN restantes no es un error del pipeline — refleja
> que House2 tiene genuinamente más gaps largos (> 30 min) en los datos raw que los otros
> hogares. El factor de reducción al remuestrear (6,4× en House2 vs 7,5× en House1) confirma
> que había menos mediciones por unidad de tiempo en los datos originales. Los NaN se
> mantienen como tales para que la validación temporal walk-forward los gestione correctamente.

---

## Archivos generados

### Datos procesados (`datos/processed/`)

| Archivo | Descripción |
|---|---|
| `house1_1min_limpio.csv` | House1 limpio, granularidad 1 minuto |
| `house2_1min_limpio.csv` | House2 limpio, granularidad 1 minuto |
| `house3_1min_limpio.csv` | House3 limpio, granularidad 1 minuto |

### Figuras (`resultados/figuras/`)

| Figura | Descripción |
|---|---|
| `03_issues_temporales_house3.png` | Distribución temporal de Issues=1 en House3 |
| `03_outliers_histograma.png` | Histograma de Aggregate con umbral de outliers |
| `03_distribucion_gaps.png` | Distribución del tamaño de los gaps de NaN |
| `03_comparativa_antes_despues.png` | Serie de House3 antes y después de la limpieza |

### Métricas (`resultados/metricas/`)

| Archivo | Descripción |
|---|---|
| `03_resumen_limpieza.csv` | Tabla resumen con estadísticas del proceso de limpieza |

---

## Impacto en la calidad del dataset

La limpieza aplicada es **conservadora**: se han eliminado solo los datos claramente
incorrectos (Issues=1 y outliers físicamente imposibles) y se ha imputado solo donde
la interpolación lineal es justificable (gaps ≤ 30 min). El resultado es un dataset de
alta calidad para modelado con las siguientes características:

- Sin valores físicamente imposibles en `Aggregate`
- Sin registros marcados con problemas de sensor
- Granularidad uniforme de 1 minuto
- NaN residuales de 12,03% (House1), 23,69% (House2) y 12,43% (House3)
  correspondientes a gaps genuinamente largos (> 30 min) en los datos originales.
  El modelo deberá gestionarlos mediante validación temporal walk-forward que respete esos huecos

---

*Documento generado durante la Fase 1 del PFM — Minería de datos y EDA.*  
*Fecha: 2026-04-16*
