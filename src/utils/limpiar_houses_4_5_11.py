"""
Pipeline de limpieza para Houses 4, 5 y 11 (formato Zenodo CLEAN).
Mismo proceso que el Notebook 03 aplicado a los hogares adicionales.

Uso: python src/utils/limpiar_houses_4_5_11.py
Genera: datos/processed/house{4,5,11}_1min_limpio.csv
        resultados/metricas/03b_resumen_limpieza_houses4511.csv
"""

import os
import sys
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
np.random.seed(42)

# Rutas
BASE = os.path.join(os.path.dirname(__file__), '..', '..')
RUTA_RAW       = os.path.join(BASE, 'datos', 'raw')
RUTA_PROCESSED = os.path.join(BASE, 'datos', 'processed')
RUTA_MET       = os.path.join(BASE, 'resultados', 'metricas')
os.makedirs(RUTA_PROCESSED, exist_ok=True)
os.makedirs(RUTA_MET, exist_ok=True)

# Parámetros (idénticos al Notebook 03)
HOGARES          = ['House4', 'House5', 'House11']
COLS_CONSUMO     = ['Aggregate'] + [f'Appliance{i}' for i in range(1, 10)]
UMBRAL_OUTLIER_W = 15_000
UMBRAL_GAP_MIN   = 30

print(f'pandas  : {pd.__version__}')
print(f'numpy   : {np.__version__}')
print(f'Hogares : {HOGARES}')
print()


def cargar_hogar(nombre):
    ruta = os.path.join(RUTA_RAW, f'CLEAN_{nombre}.csv')
    df = pd.read_csv(ruta, parse_dates=['Time'], infer_datetime_format=True)
    df = df.set_index('Time')
    df.index.name = 'timestamp'
    return df


def imputar_gaps_cortos(serie, umbral_min):
    return serie.interpolate(method='linear', limit=umbral_min, limit_area='inside')


resumen = []

for hogar in HOGARES:
    print(f'=== {hogar} ===')

    # 1. Cargar
    print(f'  Cargando CLEAN_{hogar}.csv...', end=' ')
    df = cargar_hogar(hogar)
    print(f'{len(df):,} filas')

    # 2. Issues = 1 → eliminar
    n_issues = (df['Issues'] == 1).sum()
    df = df[df['Issues'] == 0].copy()
    print(f'  Issues=1 eliminados: {n_issues:,} ({100*n_issues/len(df):.2f}%)')

    # 3. Outliers Aggregate → NaN
    n_out = (df['Aggregate'] > UMBRAL_OUTLIER_W).sum()
    df.loc[df['Aggregate'] > UMBRAL_OUTLIER_W, 'Aggregate'] = np.nan
    print(f'  Outliers >15kW:      {n_out:,}')

    # 4. Resampleo 1 minuto
    df_1min = df[COLS_CONSUMO].resample('1min').mean()
    nan_antes = df_1min['Aggregate'].isna().sum()
    print(f'  Tras resampleo:      {len(df_1min):,} filas | NaN={nan_antes:,} ({100*nan_antes/len(df_1min):.2f}%)')

    # 5. Interpolación gaps ≤ 30 min
    for col in COLS_CONSUMO:
        df_1min[col] = imputar_gaps_cortos(df_1min[col], UMBRAL_GAP_MIN)

    nan_final = df_1min['Aggregate'].isna().sum()
    pct_nan   = 100 * nan_final / len(df_1min)
    media_w   = df_1min['Aggregate'].mean()
    max_w     = df_1min['Aggregate'].max()
    print(f'  NaN final:           {nan_final:,} ({pct_nan:.2f}%) | media={media_w:.1f}W | max={max_w:.1f}W')

    # 6. Guardar
    nombre_csv = f'{hogar.lower()}_1min_limpio.csv'
    ruta_out   = os.path.join(RUTA_PROCESSED, nombre_csv)
    df_1min.to_csv(ruta_out)
    tam_mb = os.path.getsize(ruta_out) / 1024**2
    print(f'  Guardado: {nombre_csv} ({tam_mb:.1f} MB)')
    print()

    resumen.append({
        'house'           : hogar,
        'filas_raw'       : len(df),
        'issues_eliminados': n_issues,
        'outliers_eliminados': n_out,
        'filas_1min'      : len(df_1min),
        'nan_antes_interp': nan_antes,
        'pct_nan_antes'   : round(100 * nan_antes / len(df_1min), 2),
        'nan_final'       : nan_final,
        'pct_nan_final'   : round(pct_nan, 2),
        'media_limpio_w'  : round(media_w, 1),
        'max_limpio_w'    : round(max_w, 1),
        'apto_training'   : pct_nan <= 20.0,
    })

# Guardar CSV de resumen
df_res = pd.DataFrame(resumen).set_index('house')
ruta_csv = os.path.join(RUTA_MET, '03b_resumen_limpieza_houses4511.csv')
df_res.to_csv(ruta_csv)
print(f'Resumen guardado en: {ruta_csv}')
print()
print('=== RESUMEN FINAL ===')
print(df_res[['pct_nan_final', 'media_limpio_w', 'max_limpio_w', 'apto_training']].to_string())
