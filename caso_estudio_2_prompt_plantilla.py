from pathlib import Path
import sys
import pandas as pd
import matplotlib.pyplot as plt


# Archivo esperado en la raíz del proyecto
ARCHIVO_CSV = "desastres.csv"


def leer_csv(ruta: str) -> pd.DataFrame | None:
    """
    Lee el archivo CSV y valida que exista y contenga datos.

    Args:
        ruta: Ruta del archivo CSV.

    Returns:
        DataFrame con los datos leídos o None si ocurre un error.
    """
    ruta_archivo = Path(ruta)

    if not ruta_archivo.exists():
        print("Error: El archivo no fue encontrado.")
        return None

    try:
        datos = pd.read_csv(ruta_archivo)
    except Exception as error:
        print(f"Error al leer el archivo CSV: {error}")
        return None

    if datos.empty:
        print("Error: El archivo no contiene datos.")
        return None

    return datos


def normalizar_columnas(datos: pd.DataFrame) -> pd.DataFrame:
    """
    Normaliza los nombres de las columnas para facilitar su validación.

    Convierte a minúsculas, elimina espacios extra y reemplaza espacios
    o guiones por guiones bajos.
    """
    datos = datos.copy()
    datos.columns = (
        datos.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    return datos


def encontrar_columna(datos: pd.DataFrame, candidatos: list[str]) -> str | None:
    """
    Busca una columna en el DataFrame usando una lista de nombres posibles.

    Args:
        datos: DataFrame donde se buscará la columna.
        candidatos: Lista de posibles nombres de columna.

    Returns:
        Nombre de la columna encontrada o None si no existe.
    """
    for columna in candidatos:
        if columna in datos.columns:
            return columna
    return None


def validar_columnas(datos: pd.DataFrame) -> dict[str, str] | None:
    """
    Valida que existan las columnas mínimas requeridas para el análisis.

    Deben existir columnas equivalentes para:
    - entidad federativa
    - municipios corroborados
    - año o fecha del registro

    Args:
        datos: DataFrame con columnas normalizadas.

    Returns:
        Diccionario con el mapeo de columnas si la validación es correcta,
        o None si faltan columnas.
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

    candidatos_fecha = [
        "anio",
        "año",
        "year",
        "fecha",
        "fecha_registro",
        "fecha_del_registro",
        "fecha_evento",
    ]

    columna_entidad = encontrar_columna(datos, candidatos_entidad)
    columna_municipios = encontrar_columna(datos, candidatos_municipios)
    columna_fecha = encontrar_columna(datos, candidatos_fecha)

    if not columna_entidad or not columna_municipios or not columna_fecha:
        print("Error: Faltan columnas requeridas para el análisis.")
        print("Se necesitan columnas equivalentes a:")
        print("- entidad federativa")
        print("- municipios corroborados")
        print("- año o fecha del registro")
        return None

    return {
        "entidad": columna_entidad,
        "municipios": columna_municipios,
        "fecha_o_anio": columna_fecha,
    }


def extraer_anio(columna: pd.Series) -> pd.Series:
    """
    Obtiene el año desde una columna que puede contener fechas completas
    o años directos.

    Args:
        columna: Serie con fechas o años.

    Returns:
        Serie con el año extraído.
    """
    fechas = pd.to_datetime(columna, errors="coerce")
    anios_fecha = fechas.dt.year

    anios_numericos = pd.to_numeric(columna, errors="coerce")

    return anios_fecha.fillna(anios_numericos)


def preparar_datos(
    datos: pd.DataFrame, columnas: dict[str, str]
) -> pd.DataFrame:
    """
    Limpia y prepara los datos para el análisis.

    Acciones realizadas:
    - Normaliza valores relevantes
    - Convierte municipios corroborados a numérico
    - Extrae el año del registro
    - Filtra el periodo 2019–2024
    - Elimina registros incompletos cuando afectan el análisis

    Args:
        datos: DataFrame original.
        columnas: Diccionario con el nombre real de las columnas detectadas.

    Returns:
        DataFrame preparado.
    """
    datos = datos.copy()

    columna_entidad = columnas["entidad"]
    columna_municipios = columnas["municipios"]
    columna_fecha = columnas["fecha_o_anio"]

    # Normalizar entidad federativa
    datos[columna_entidad] = datos[columna_entidad].astype(str).str.strip()

    # Convertir municipios corroborados a valor numérico
    datos[columna_municipios] = pd.to_numeric(
        datos[columna_municipios], errors="coerce"
    )

    # Extraer año desde fecha o año directo
    datos["anio_registro"] = extraer_anio(datos[columna_fecha])

    # Filtrar únicamente el periodo solicitado
    datos = datos[
        datos["anio_registro"].notna()
        & datos["anio_registro"].between(2019, 2024, inclusive="both")
    ].copy()

    # Eliminar registros con entidad faltante o vacía
    datos = datos[
        datos[columna_entidad].notna()
        & (datos[columna_entidad] != "")
        & (datos[columna_entidad].str.lower() != "nan")
    ].copy()

    return datos


def grafica_entidades_con_mas_contingencias(
    datos: pd.DataFrame, columna_entidad: str
) -> pd.Series:
    """
    Genera una gráfica de barras de las entidades con más contingencias.

    Args:
        datos: DataFrame preparado.
        columna_entidad: Nombre de la columna de entidad federativa.

    Returns:
        Serie con el conteo de contingencias por entidad.
    """
    resultado = (
        datos.groupby(columna_entidad)
        .size()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(resultado.head(10).index, resultado.head(10).values)
    plt.title("Entidades federativas con más contingencias")
    plt.xlabel("Entidad federativa")
    plt.ylabel("Número de contingencias")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    return resultado


def grafica_entidades_con_mas_municipios_corroborados(
    datos: pd.DataFrame, columna_entidad: str, columna_municipios: str
) -> pd.Series:
    """
    Genera una gráfica de barras de las entidades con mayor número
    de municipios corroborados.

    Sólo se consideran registros con municipios corroborados válidos.

    Args:
        datos: DataFrame preparado.
        columna_entidad: Nombre de la columna de entidad federativa.
        columna_municipios: Nombre de la columna de municipios corroborados.

    Returns:
        Serie con la suma de municipios corroborados por entidad.
    """
    datos_validos = datos[
        datos[columna_municipios].notna()
        & (datos[columna_municipios] >= 0)
    ].copy()

    resultado = (
        datos_validos.groupby(columna_entidad)[columna_municipios]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(12, 6))
    plt.bar(resultado.head(10).index, resultado.head(10).values)
    plt.title("Entidades con mayor número de municipios corroborados")
    plt.xlabel("Entidad federativa")
    plt.ylabel("Municipios corroborados")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

    return resultado


def grafica_anio_con_mas_contingencias(datos: pd.DataFrame) -> pd.Series:
    """
    Genera una gráfica de barras con el número de contingencias por año.

    Args:
        datos: DataFrame preparado.

    Returns:
        Serie con el conteo de contingencias por año.
    """
    resultado = (
        datos.groupby("anio_registro")
        .size()
        .sort_index()
    )

    plt.figure(figsize=(10, 5))
    plt.bar(resultado.index.astype(str), resultado.values)
    plt.title("Número de contingencias por año")
    plt.xlabel("Año")
    plt.ylabel("Número de contingencias")
    plt.tight_layout()
    plt.show()

    return resultado


def mostrar_resumen(
    contingencias_por_entidad: pd.Series,
    municipios_por_entidad: pd.Series,
    contingencias_por_anio: pd.Series,
) -> None:
    """
    Muestra un resumen de los principales resultados del análisis.
    """
    entidad_top_contingencias = contingencias_por_entidad.idxmax()
    valor_top_contingencias = contingencias_por_entidad.max()

    entidad_top_municipios = municipios_por_entidad.idxmax()
    valor_top_municipios = municipios_por_entidad.max()

    anio_top = int(contingencias_por_anio.idxmax())
    valor_anio_top = contingencias_por_anio.max()

    print("\nResumen del análisis:")
    print(
        f"- Entidad con más contingencias: "
        f"{entidad_top_contingencias} ({valor_top_contingencias})"
    )
    print(
        f"- Entidad con más municipios corroborados: "
        f"{entidad_top_municipios} ({valor_top_municipios})"
    )
    print(
        f"- Año con más contingencias registradas: "
        f"{anio_top} ({valor_anio_top})"
    )


def main() -> None:
    """
    Función principal que coordina todo el flujo del programa.
    """
    print("Iniciando análisis del archivo...")

    datos = leer_csv(f"./{ARCHIVO_CSV}")
    if datos is None:
        sys.exit(1)

    datos = normalizar_columnas(datos)

    columnas = validar_columnas(datos)
    if columnas is None:
        sys.exit(1)

    datos_preparados = preparar_datos(datos, columnas)

    if datos_preparados.empty:
        print("Error: No hay datos válidos para analizar.")
        sys.exit(1)

    try:
        contingencias_por_entidad = grafica_entidades_con_mas_contingencias(
            datos_preparados,
            columnas["entidad"],
        )

        municipios_por_entidad = (
            grafica_entidades_con_mas_municipios_corroborados(
                datos_preparados,
                columnas["entidad"],
                columnas["municipios"],
            )
        )

        contingencias_por_anio = grafica_anio_con_mas_contingencias(
            datos_preparados
        )

        if (
            contingencias_por_entidad.empty
            or municipios_por_entidad.empty
            or contingencias_por_anio.empty
        ):
            print("Error: No fue posible generar uno o más análisis.")
            sys.exit(1)

        mostrar_resumen(
            contingencias_por_entidad,
            municipios_por_entidad,
            contingencias_por_anio,
        )

        print("\nAnálisis finalizado correctamente.")

    except Exception as error:
        print(f"Error durante el procesamiento o la visualización: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
