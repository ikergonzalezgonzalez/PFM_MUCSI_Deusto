"""
Feature engineering para Houses 4, 5 y 11 (formato Zenodo CLEAN procesado).
Mismo catálogo de 36 features que el Notebook 04 (H1,H2,H3) y el Notebook 06 (Strathclyde).

Uso: python src/utils/features_houses_4_5_11.py
Lee:  datos/processed/house{4,5,11}_1min_limpio.csv
Genera: datos/processed/house{4,5,11}_features.csv
        resultados/metricas/04b_resumen_features_houses4511.csv
"""

import os
import gc
import warnings
import numpy as np
import pandas as pd

warnings.filterwarnings('ignore')
np.random.seed(42)

# Rutas
BASE           = os.path.join(os.path.dirname(__file__), '..', '..')
RUTA_PROCESSED = os.path.join(BASE, 'datos', 'processed')
RUTA_MET       = os.path.join(BASE, 'resultados', 'metricas')
os.makedirs(RUTA_PROCESSED, exist_ok=True)
os.makedirs(RUTA_MET, exist_ok=True)

HOGARES = [4, 5, 11]

print(f'pandas  : {pd.__version__}')
print(f'numpy   : {np.__version__}')
print(f'Hogares : {HOGARES}')
print()

# Festivos UK 2013-2015 (lista manual — sin dependencia de librería externa)
FESTIVOS_UK = pd.to_datetime([
    '2013-12-25', '2013-12-26',
    '2014-01-01', '2014-04-18', '2014-04-21', '2014-05-05',
    '2014-05-26', '2014-08-25', '2014-12-25', '2014-12-26',
    '2015-01-01', '2015-04-03', '2015-04-06', '2015-05-04',
    '2015-05-25', '2015-08-31', '2015-12-25', '2015-12-28'
])


def crear_features(df, columna='Aggregate'):
    """
    Catálogo unificado de 36 features en 5 grupos:
    - 9 temporales: hora, dia_semana, dia_mes, mes, anio, semana_anio,
                    dia_anio, trimestre, parte_dia
    - 3 binarias:   es_fin_semana, es_festivo_uk, es_laboral
    - 8 cíclicas:   sin/cos de hora, dia_semana, mes, dia_anio
    - 8 lags:       lag_1, 5, 15, 30, 60, 120, 1440, 10080 (en minutos)
    - 8 rolling:    media y desv. estándar con ventanas 15, 60, 240, 1440 min
    Total: 36 features
    """
    df_feat = df[[columna]].copy()
    col = df_feat[columna]
    idx = df_feat.index

    # --- 9 Temporales ---
    df_feat['hora']        = idx.hour
    df_feat['dia_semana']  = idx.dayofweek
    df_feat['dia_mes']     = idx.day
    df_feat['mes']         = idx.month
    df_feat['anio']        = idx.year
    df_feat['semana_anio'] = idx.isocalendar().week.astype(int)
    df_feat['dia_anio']    = idx.dayofyear
    df_feat['trimestre']   = idx.quarter

    h = idx.hour
    parte = np.where(h < 6, 0, np.where(h < 12, 1, np.where(h < 18, 2, np.where(h < 21, 3, 4))))
    df_feat['parte_dia'] = parte

    # --- 3 Binarias ---
    df_feat['es_fin_semana'] = (idx.dayofweek >= 5).astype(int)
    df_feat['es_festivo_uk'] = idx.normalize().isin(FESTIVOS_UK).astype(int)
    df_feat['es_laboral']    = (
        (df_feat['es_fin_semana'] == 0) & (df_feat['es_festivo_uk'] == 0)
    ).astype(int)

    # --- 8 Cíclicas ---
    df_feat['hora_sin']       = np.sin(2 * np.pi * idx.hour / 24)
    df_feat['hora_cos']       = np.cos(2 * np.pi * idx.hour / 24)
    df_feat['dia_semana_sin'] = np.sin(2 * np.pi * idx.dayofweek / 7)
    df_feat['dia_semana_cos'] = np.cos(2 * np.pi * idx.dayofweek / 7)
    df_feat['mes_sin']        = np.sin(2 * np.pi * idx.month / 12)
    df_feat['mes_cos']        = np.cos(2 * np.pi * idx.month / 12)
    df_feat['dia_anio_sin']   = np.sin(2 * np.pi * idx.dayofyear / 365)
    df_feat['dia_anio_cos']   = np.cos(2 * np.pi * idx.dayofyear / 365)

    # --- 8 Lags (en minutos) ---
    for lag in [1, 5, 15, 30, 60, 120, 1440, 10080]:
        df_feat[f'lag_{lag}'] = col.shift(lag)

    # --- 8 Rolling (media y desv. estándar) ---
    for ventana in [15, 60, 240, 1440]:
        df_feat[f'rolling_mean_{ventana}'] = col.rolling(window=ventana, min_periods=1).mean()
        df_feat[f'rolling_std_{ventana}']  = col.rolling(window=ventana, min_periods=1).std()

    return df_feat


resumen = []

for numero in HOGARES:
    print(f'=== House {numero} ===')

    # 1. Cargar datos limpios
    ruta_in = os.path.join(RUTA_PROCESSED, f'house{numero}_1min_limpio.csv')
    print(f'  Cargando house{numero}_1min_limpio.csv...', end=' ')
    df = pd.read_csv(ruta_in, index_col='timestamp', parse_dates=True)
    print(f'{len(df):,} filas | NaN Aggregate={df["Aggregate"].isna().sum():,}')

    # 2. Feature engineering
    print(f'  Generando 36 features...', end=' ')
    df_feat = crear_features(df, columna='Aggregate')
    n_total    = len(df_feat)
    n_features = len(df_feat.columns) - 1  # sin Aggregate
    nan_lag    = int(df_feat['lag_10080'].isna().sum())
    print(f'{n_total:,} filas | {n_features} features | NaN lag_10080={nan_lag:,}')

    # 3. Correlación con Aggregate
    df_corr = df_feat.dropna(subset=['Aggregate'])
    corr = df_corr.corr()['Aggregate'].drop('Aggregate').abs().sort_values(ascending=False)
    top1_feat = corr.index[0]
    top1_r    = round(corr.iloc[0], 3)
    top2_feat = corr.index[1]
    top2_r    = round(corr.iloc[1], 3)
    print(f'  Top 1: {top1_feat} (r={top1_r}) | Top 2: {top2_feat} (r={top2_r})')

    # 4. Guardar features
    ruta_out = os.path.join(RUTA_PROCESSED, f'house{numero}_features.csv')
    df_feat.to_csv(ruta_out)
    tam_mb = os.path.getsize(ruta_out) / 1024**2
    print(f'  Guardado: house{numero}_features.csv ({tam_mb:.1f} MB)')
    print()

    resumen.append({
        'house'         : numero,
        'n_registros'   : n_total,
        'n_features'    : n_features,
        'nan_lag_10080' : nan_lag,
        'top1_feature'  : top1_feat,
        'top1_corr'     : top1_r,
        'top2_feature'  : top2_feat,
        'top2_corr'     : top2_r,
    })

    del df_feat, df_corr, corr
    gc.collect()

# Guardar CSV de resumen
df_res = pd.DataFrame(resumen).set_index('house')
ruta_csv = os.path.join(RUTA_MET, '04b_resumen_features_houses4511.csv')
df_res.to_csv(ruta_csv)
print(f'Resumen guardado en: {ruta_csv}')
print()
print('=== RESUMEN FINAL ===')
print(df_res.to_string())
print()
print('Nota: nan_lag_10080 = primeras 10.080 filas con NaN en lag semanal.')
print('      Estrategia: eliminar primeras 10.080 filas antes de entrenar (mismo criterio Nb04).')
