# Dashboard Power BI – Exportaciones de minerales de oro (partida 2616901000)

Datos: 363 filas / 360 declaraciones, régimen 40 (exportación definitiva), 02-ene-2025 a 12-oct-2026.

## 1. Carga (5 minutos)
1. Power BI Desktop → Obtener datos → Excel → `Datos_Exportaciones_PowerBI.xlsx` → marcar las 3 hojas → Cargar.
2. Vista Modelo, crear relaciones (varios a uno, filtro único):
   - `Fact_Exportaciones[Cod_Aduana]` → `Dim_Aduana[Cod_Aduana]`
   - `Fact_Exportaciones[Cod_Departamento]` → `Dim_Departamento[Cod_Departamento]`
   - `Fact_Exportaciones[Fecha]` → `Calendario[Fecha]`
3. En Power Query confirma tipos: `Fecha` = Fecha, `Cod_Aduana`, `Cod_Departamento`, `Cod_Ubigeo`, `RUC_Usuario` = Texto.

## 2. Tabla Calendario (Modelado → Nueva tabla)
```dax
Calendario =
ADDCOLUMNS(
    CALENDAR(DATE(2025,1,1), DATE(2026,12,31)),
    "Año", YEAR([Date]),
    "Mes N", MONTH([Date]),
    "Mes", FORMAT([Date], "mmm"),
    "Año-Mes", FORMAT([Date], "yyyy-mm"),
    "Trimestre", "T" & QUARTER([Date])
)
```
Renombra la columna `Date` a `Fecha`, ordena `Mes` por `Mes N` y márcala como tabla de fechas.

## 3. Medidas DAX
```dax
FOB USD = SUM(Fact_Exportaciones[FOB_USD])
FOB MM USD = DIVIDE([FOB USD], 1000000)
Peso Neto TM = SUM(Fact_Exportaciones[Peso_Neto_TM])
Declaraciones = DISTINCTCOUNT(Fact_Exportaciones[ID_Declaracion])
Precio USD por TM = DIVIDE([FOB USD], [Peso Neto TM])
FOB Promedio por Declaración = DIVIDE([FOB USD], [Declaraciones])
TM Promedio por Declaración = DIVIDE([Peso Neto TM], [Declaraciones])

% FOB del Total =
DIVIDE([FOB USD], CALCULATE([FOB USD], ALLSELECTED()))

FOB Mes Anterior =
CALCULATE([FOB USD], DATEADD(Calendario[Fecha], -1, MONTH))

Var % FOB vs Mes Anterior =
DIVIDE([FOB USD] - [FOB Mes Anterior], [FOB Mes Anterior])

FOB Acumulado Año =
TOTALYTD([FOB USD], Calendario[Fecha])

FOB Mismo Período Año Anterior =
CALCULATE([FOB USD], SAMEPERIODLASTYEAR(Calendario[Fecha]))

Var % FOB vs Año Anterior =
DIVIDE([FOB USD] - [FOB Mismo Período Año Anterior], [FOB Mismo Período Año Anterior])

Declaraciones con FOB Atípico =
CALCULATE([Declaraciones], Fact_Exportaciones[FOB_Atipico] = "Sí")
```
Nota: las comparaciones contra el año anterior de 2026 deben leerse con cuidado, porque 2026 llega solo hasta el 12-oct.

## 4. Diseño de páginas (de lo más relevante a lo más detallado)

### Página 1 – Resumen ejecutivo
- **Tarjetas (fila superior):** FOB MM USD · Peso Neto TM · Declaraciones · Precio USD por TM · Var % vs Año Anterior
- **Columnas + línea:** Eje `Calendario[Año-Mes]`; columnas = FOB MM USD, línea = Peso Neto TM (eje secundario)
- **Barras horizontales:** `Dim_Departamento[Departamento]` × FOB MM USD (Top 10)
- **Anillo:** `Tipo_Producto` × FOB USD
- **Segmentadores:** Año, Departamento, Aduana, Tipo_Producto

### Página 2 – Precio y volumen
- **Línea:** Precio USD por TM por `Año-Mes`
- **Dispersión:** X = Peso Neto TM, Y = FOB USD, detalle = `ID_Declaracion`, leyenda = `Tipo_Producto` (detecta envíos atípicos)
- **Matriz:** `Tipo_Producto` × `Año` con FOB, TM y Precio USD por TM
- **Histograma (columnas agrupadas):** declaraciones por rango de tamaño (crear grupo sobre `Peso_Neto_TM`)

### Página 3 – Origen geográfico
- **Mapa de burbujas / mapa coroplético:** `Departamento` × FOB USD
- **Treemap:** Departamento → `Cod_Ubigeo` × FOB USD
- **Tabla:** Top 15 ubigeos con declaraciones, TM, FOB

### Página 4 – Operadores y aduanas
- **Barras:** `RUC_Usuario` × FOB USD (Top 10) con `% FOB del Total`
- **Barras apiladas:** `RUC_Usuario` por `Año`
- **Columnas:** `Dim_Aduana[Aduana]` × Declaraciones
- **Matriz:** RUC_Usuario × Departamento (mapa de calor con formato condicional)

### Página 5 – Detalle y calidad de datos
- **Tabla:** Fecha, ID_Declaracion, Num_Declaracion, Descripcion, Departamento, Peso_Neto_TM, FOB_USD, Precio USD por TM
- **Tarjetas:** Declaraciones con FOB Atípico · Declaraciones anuladas

## 5. Notas de calidad de datos
- `RUC_Usuario` es el usuario que registró la declaración (normalmente el agente de aduana o el exportador); no es necesariamente el exportador.
- 3 declaraciones tienen 2 series (ítems); por eso hay 363 filas y 360 declaraciones. Usa siempre `Declaraciones` (DISTINCTCOUNT).
- `Bultos` se dejó vacío cuando el dato original venía con valores en kg (granel); no lo uses como KPI.
- 1 fila marcada `Anulada = Sí` y con FOB < 100 USD: filtra `FOB_Atipico = "No"` si quieres precios limpios.
- Las aduanas 235 y 370 no se pudieron nombrar con certeza; completa `Dim_Aduana` si tienes la tabla oficial de SUNAT.
- El nombre de distrito no está en el archivo; si lo necesitas, une `Cod_Ubigeo` con la tabla de ubigeos del INEI.
