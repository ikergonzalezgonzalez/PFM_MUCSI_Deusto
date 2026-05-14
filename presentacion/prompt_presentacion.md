

Eres un experto en diseño de presentaciones académicas y comunicación científica visual.

Te adjunto un documento con todos los datos de mi Proyecto Fin de Máster sobre predicción de consumo eléctrico con Machine Learning. Necesito que crees una presentacion que resuma de forma concisa, visual e impactante lo que se ha hecho hasta ahora en el proyecto.

## Requisitos de la presentación

**Formato y extensión:**
- Número de diapositivas: entre 8 y 12 (ni más ni menos)
- Idioma: español
- Estilo: académico pero dinámico — claro, directo, visualmente rico

**Estilo visual:**
- Esquema de colores: azul oscuro (#1a2744) como fondo de portada, blanco para el cuerpo, con acento en naranja (#f07030) o azul claro (#4a9eda) para destacar datos clave
- Tipografía limpia, tamaño de fuente generoso (no saturar de texto)
- Máximo 5-6 líneas de texto por diapositiva — el resto debe ser visual
- Usa emojis estratégicos para hacer la lectura más ágil (⚡📊🔍🧹📈🤖)

**Diagramas obligatorios con Mermaid:**
Incluye al menos estos tres diagramas incrustados como bloques ```mermaid:

1. **Diagrama de flujo del pipeline de limpieza** (Notebook 03):
   Datos raw → Eliminar Issues=1 → Outliers > 15.000W → Remuestreo 1min → Imputar gaps ≤30min → Datos limpios
   Añade las cifras clave en cada flecha/nodo (ej: "−408.627 filas", "7,5× reducción", "12% NaN restante")

2. **Diagrama de los 5 grupos de features** (Notebook 04):
   Un diagrama tipo mindmap o flowchart con el nodo central "36 Features" y 5 ramas: Temporales (9), Cíclicas (8), Binarias (3), Lags (8), Ventana (8)
   En cada rama incluye 2-3 ejemplos representativos

3. **Roadmap de fases del proyecto**:
   Un diagrama de Gantt simplificado o timeline horizontal:
   Fase 1 EDA [✅ completada] → Fase 2 Modelado [🔜 siguiente] → Fase 3 Dashboard+Memoria [⬜ pendiente]
   Con los modelos planificados listados bajo Fase 2 (Baseline, ARIMA, XGBoost, LightGBM, LSTM)

**Estructura de diapositivas sugerida** (ajusta si ves mejoras):
1. **Portada** — Título del PFM, universidad, fecha
2. **El problema** — Por qué predecir el consumo eléctrico (1-2 frases de motivación + dato impactante)
3. **El dataset REFIT** — Tabla comparativa de los 3 hogares con los números clave
4. **Fase 1 completada: resumen visual** — Lista de los 4 notebooks con iconos + qué produjo cada uno
5. **Pipeline de limpieza** — Diagrama Mermaid del flujo completo con cifras clave
6. **Hallazgos del EDA** — Los 3-4 hallazgos más importantes (asimetría, ciclo diario, autocorrelación, House2)
7. **Feature Engineering** — Diagrama Mermaid de los 5 grupos de features
8. **Decisiones técnicas clave** — Tabla o lista de las decisiones con su justificación (máx. 5)
9. **Siguiente paso: Fase 2** — Roadmap de modelos a comparar con sus métricas
10. **Visión final del proyecto** — Diagrama de las 3 fases + qué quedará cuando todo esté listo

**Tono y énfasis:**
- Destaca los números grandes con formato bold o en una caja visual: **~2,7M filas**, **36 features**, **2 años de datos**
- Resalta las alertas importantes: House2 con 23,69% NaN, el outlier de 65.836 W
- El mensaje central de la presentación debe quedar claro: "Se ha construido una base de datos limpia, analizada en profundidad y con features de calidad — lista para el modelado"



