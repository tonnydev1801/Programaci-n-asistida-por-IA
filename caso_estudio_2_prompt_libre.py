from pathlib import Path
import sys

import matplotlib.pyplot as plt
import pandas as pd


# Nombre del archivo CSV esperado en la raíz del proyecto
CSV_FILE = "desastres.csv"


def leer_csv(ruta_archivo: str) -> pd.DataFrame:
    """
    Lee el archivo CSV y devuelve un DataFrame.

    Valida:
    - Que el archivo exista
    - Que pueda leerse correctamente
    - Que contenga al menos un registro

    Args:
        ruta_archivo: Ruta del archivo CSV.

    Returns:
        DataFrame con la información leída.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        ValueError: Si el archivo está vacío o no contiene datos utilizables.
        RuntimeError: Si ocurre un error al leer el archivo.
    """
    ruta = Path(ruta_archivo)

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo '{ruta_archivo}' en la raíz del proyecto."
        )

    try:
        df = pd.read_csv(ruta)
    except pd.errors.EmptyDataError as exc:
        raise ValueError("El archivo CSV está vacío.") from exc
    except Exception as exc:
        raise RuntimeError(f"Error al leer el archivo CSV: {exc}") from exc

    if df.empty:
        raise ValueError("El archivo CSV no contiene registros para analizar.")

    return df


def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de columnas para facilitar su identificación.

    Convierte a minúsculas, elimina espacios al inicio/final y reemplaza
    espacios por guiones bajos.

    Args:
        df: DataFrame original.

    Returns:
        DataFrame con nombres de columnas normalizados.
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return df


def encontrar_columna(df: pd.DataFrame, candidatos: list[str]) -> str | None:
    """
    Busca la primera columna existente en el DataFrame dentro de una lista
    de nombres candidatos.

    Args:
        df: DataFrame a revisar.
        candidatos: Lista de posibles nombres de columna.

    Returns:
        El nombre de la columna encontrada o None si no existe.
    """
    for columna in candidatos:
        if columna in df.columns:
            return columna
    return None


def validar_columnas(df: pd.DataFrame) -> dict[str, str]:
    """
    Valida que existan las columnas necesarias para el análisis:
    - Entidad federativa
    - Municipios corroborados
    - Año o fecha del registro

    Debido a que los nombres pueden variar entre archivos, se prueban
    diferentes alternativas comunes.

    Args:
        df: DataFrame con columnas normalizadas.

    Returns:
        Diccionario con el mapeo de columnas encontradas.

    Raises:
        ValueError: Si falta alguna columna obligatoria.
    """
    candidatos_entidad = [
        "entidad_federativa",
        "entidad",
        "estado",
        "nombre_entidad",
        "nombre_estado",
    ]

    candidatos_municipios = [
        "municipios_corroborados",
        "municipio_corroborado",
        "municipios",
        "municipio",
        "num_municipios_corroborados",
        "cantidad_municipios_corroborados",
    ]

    candidatos_anio = [
        "anio",
        "año",
        "year",
        "fecha",
        "fecha_registro",
        "fecha_del_registro",
        "fecha_evento",
    ]

    columna_entidad = encontrar_columna(df, candidatos_entidad)
    columna_municipios = encontrar_columna(df, candidatos_municipios)
    columna_anio_o_fecha = encontrar_columna(df, candidatos_anio)

    faltantes = []

    if columna_entidad is None:
        faltantes.append("entidad federativa")
    if columna_municipios is None:
        faltantes.append("municipios corroborados")
    if columna_anio_o_fecha is None:
        faltantes.append("año o fecha del registro")

    if faltantes:
        raise ValueError(
            "Faltan columnas necesarias en el archivo CSV: "
            + ", ".join(faltantes)
            + "."
        )

    return {
        "entidad": columna_entidad,
        "municipios": columna_municipios,
        "anio_o_fecha": columna_anio_o_fecha,
    }


def extraer_anio(serie: pd.Series) -> pd.Series:
    """
    Extrae el año desde una columna que puede contener:
    - Año directo (ej. 2021)
    - Fecha completa (ej. 2021-08-15)

    Los valores inválidos se convierten en NaN.

    Args:
        serie: Serie con años o fechas.

    Returns:
        Serie con el año extraído como numérico.
    """
    # Primero intentar parsear como fecha
    fechas = pd.to_datetime(serie, errors="coerce")
    anios_desde_fecha = fechas.dt.year

    # Para valores que no se pudieron interpretar como fecha,
    # intentar convertir directamente a número (por ejemplo: 2019, 2020, etc.)
    valores_numericos = pd.to_numeric(serie, errors="coerce")

    # Combinar ambas opciones, priorizando el año extraído desde fecha
    anios = anios_desde_fecha.fillna(valores_numericos)

    return anios


def procesar_datos(
    df: pd.DataFrame, columnas: dict[str, str]
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """
    Procesa la información del CSV y genera tres series:
    1. Número de contingencias por entidad federativa
    2. Suma de municipios corroborados por entidad federativa
    3. Número de contingencias por año

    Se eliminan registros incompletos únicamente cuando afectan
    el análisis correspondiente.

    Args:
        df: DataFrame original con columnas normalizadas.
        columnas: Diccionario con nombres de columnas detectadas.

    Returns:
        Una tupla con tres Series agregadas.

    Raises:
        ValueError: Si no hay suficientes datos válidos para analizar.
    """
    df = df.copy()

    col_entidad = columnas["entidad"]
    col_municipios = columnas["municipios"]
    col_anio_o_fecha = columnas["anio_o_fecha"]

    # Normalizar entidad federativa como texto
    df[col_entidad] = df[col_entidad].astype(str).str.strip()

    # Convertir municipios corroborados a valor numérico
    df[col_municipios] = pd.to_numeric(df[col_municipios], errors="coerce")

    # Extraer año
    df["anio_extraido"] = extraer_anio(df[col_anio_o_fecha])

    # Considerar sólo años del periodo solicitado
    df.loc[~df["anio_extraido"].between(2019, 2024, inclusive="both"), "anio_extraido"] = pd.NA

    # -------- Análisis 1: contingencias por entidad --------
    df_entidades = df[
        df[col_entidad].notna()
        & (df[col_entidad] != "")
        & (df[col_entidad].str.lower() != "nan")
    ].copy()

    contingencias_por_entidad = (
        df_entidades.groupby(col_entidad)
        .size()
        .sort_values(ascending=False)
    )

    # -------- Análisis 2: municipios corroborados por entidad --------
    df_municipios = df[
        df[col_entidad].notna()
        & (df[col_entidad] != "")
        & (df[col_entidad].str.lower() != "nan")
        & df[col_municipios].notna()
        & (df[col_municipios] >= 0)
    ].copy()

    municipios_por_entidad = (
        df_municipios.groupby(col_entidad)[col_municipios]
        .sum()
        .sort_values(ascending=False)
    )

    # -------- Análisis 3: contingencias por año --------
    df_anios = df[df["anio_extraido"].notna()].copy()

    contingencias_por_anio = (
        df_anios.groupby("anio_extraido")
        .size()
        .sort_values(ascending=False)
    )

    if contingencias_por_entidad.empty:
        raise ValueError(
            "No hay datos válidos para calcular contingencias por entidad federativa."
        )

    if municipios_por_entidad.empty:
        raise ValueError(
            "No hay datos válidos para calcular municipios corroborados por entidad."
        )

    if contingencias_por_anio.empty:
        raise ValueError(
            "No hay datos válidos para calcular contingencias por año."
        )

    return contingencias_por_entidad, municipios_por_entidad, contingencias_por_anio


def graficar_barras(
    serie: pd.Series,
    titulo: str,
    etiqueta_x: str,
    etiqueta_y: str,
    top_n: int | None = None,
) -> None:
    """
    Genera una gráfica de barras a partir de una Serie de pandas.

    Args:
        serie: Serie con índice como categorías y valores numéricos.
        titulo: Título de la gráfica.
        etiqueta_x: Etiqueta del eje X.
        etiqueta_y: Etiqueta del eje Y.
        top_n: Número máximo de elementos a mostrar. Si es None, muestra todos.
    """
    datos = serie.head(top_n) if top_n is not None else serie

    plt.figure(figsize=(12, 6))
    plt.bar(datos.index.astype(str), datos.values)
    plt.title(titulo)
    plt.xlabel(etiqueta_x)
    plt.ylabel(etiqueta_y)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


def generar_visualizaciones(
    contingencias_por_entidad: pd.Series,
    municipios_por_entidad: pd.Series,
    contingencias_por_anio: pd.Series,
) -> None:
    """
    Genera las tres visualizaciones solicitadas:
    1. Entidades federativas con más contingencias
    2. Entidades con mayor número de municipios corroborados
    3. Año con mayor número de contingencias registradas

    Args:
        contingencias_por_entidad: Serie agregada de contingencias por entidad.
        municipios_por_entidad: Serie agregada de municipios por entidad.
        contingencias_por_anio: Serie agregada de contingencias por año.
    """
    graficar_barras(
        serie=contingencias_por_entidad,
        titulo="Entidades federativas con más contingencias",
        etiqueta_x="Entidad federativa",
        etiqueta_y="Número de contingencias",
        top_n=10,
    )

    graficar_barras(
        serie=municipios_por_entidad,
        titulo="Entidades con mayor número de municipios corroborados",
        etiqueta_x="Entidad federativa",
        etiqueta_y="Municipios corroborados",
        top_n=10,
    )

    # Para el año conviene mostrar todos porque el rango es pequeño (2019-2024)
    contingencias_por_anio = contingencias_por_anio.sort_index()

    graficar_barras(
        serie=contingencias_por_anio,
        titulo="Número de contingencias registradas por año",
        etiqueta_x="Año",
        etiqueta_y="Número de contingencias",
        top_n=None,
    )


def mostrar_resumen(
    contingencias_por_entidad: pd.Series,
    municipios_por_entidad: pd.Series,
    contingencias_por_anio: pd.Series,
) -> None:
    """
    Muestra en consola un resumen textual de los resultados principales.

    Args:
        contingencias_por_entidad: Serie de contingencias por entidad.
        municipios_por_entidad: Serie de municipios corroborados por entidad.
        contingencias_por_anio: Serie de contingencias por año.
    """
    entidad_mas_contingencias = contingencias_por_entidad.idxmax()
    total_contingencias_entidad = contingencias_por_entidad.max()

    entidad_mas_municipios = municipios_por_entidad.idxmax()
    total_municipios = municipios_por_entidad.max()

    anio_mas_contingencias = int(contingencias_por_anio.idxmax())
    total_contingencias_anio = contingencias_por_anio.max()

    print("\nResumen del análisis:")
    print(
        f"- Entidad con más contingencias: {entidad_mas_contingencias} "
        f"({total_contingencias_entidad})"
    )
    print(
        f"- Entidad con más municipios corroborados: {entidad_mas_municipios} "
        f"({total_municipios})"
    )
    print(
        f"- Año con más contingencias registradas: {anio_mas_contingencias} "
        f"({total_contingencias_anio})"
    )


def main() -> None:
    """
    Función principal del programa.
    Coordina la lectura, validación, procesamiento y visualización.
    """
    try:
        df = leer_csv(CSV_FILE)
        df = normalizar_columnas(df)
        columnas = validar_columnas(df)

        (
            contingencias_por_entidad,
            municipios_por_entidad,
            contingencias_por_anio,
        ) = procesar_datos(df, columnas)

        mostrar_resumen(
            contingencias_por_entidad,
            municipios_por_entidad,
            contingencias_por_anio,
        )

        generar_visualizaciones(
            contingencias_por_entidad,
            municipios_por_entidad,
            contingencias_por_anio,
        )

    except FileNotFoundError as exc:
        print(f"Error de lectura: {exc}")
        sys.exit(1)
    except ValueError as exc:
        print(f"Error de validación/procesamiento: {exc}")
        sys.exit(1)
    except RuntimeError as exc:
        print(f"Error de lectura: {exc}")
        sys.exit(1)
    except Exception as exc:
        print(f"Error inesperado durante la ejecución: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
