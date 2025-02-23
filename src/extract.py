from typing import Dict
import requests
from pandas import DataFrame, read_csv, read_json, to_datetime

from src.config import PUBLIC_HOLIDAYS_URL


def get_public_holidays(
    public_holidays_url: str = PUBLIC_HOLIDAYS_URL,
    year: str = "2024",
    country: str = "BR",
) -> DataFrame:
    # En primer lugar, realizamos una construccion con string literal para armar la url
    # utilizaremos la variable final del public holidays, el año y pais para armar la url
    url = f"{public_holidays_url}/{year}/{country}"

    # Luego, realizamos la petición GET a la API de días festivos en unh try/except
    # Esto nos permitira atrapar los errores en caso de que la peticion falle y
    # retornar de forma anticipida la funcion
    try:
        # Realizamos la petición GET a la API de días festivos
        response = requests.get(url)
        # Verificamos si la petición fue exitosa, si no lo fue lanzamos una excepción
        response.raise_for_status()
    except requests.RequestException as e:
        # Si hay un error en la petición, lanzamos SystemExit con el mensaje de error
        raise SystemExit(f"Error al obtener los días festivos: {e}")

    # Convertimos la respuesta JSON a un DataFrame de pandas
    df = DataFrame(response.json())

    # Eliminamos las columnas que no necesitamos del DataFrame
    # Con el axis=1 nos encargamos de elimiar las columnas y no las filas
    df = df.drop(["types", "counties"], axis=1)

    # Convertimos la columna 'date' a formato datetime para poder manipular las fechas
    df["date"] = to_datetime(df["date"])

    # Finalmente, retornamos el DataFrame
    return df


def extract(
    csv_folder: str,
    csv_table_mapping: Dict[str, str],
    public_holidays_url: str = PUBLIC_HOLIDAYS_URL,
) -> Dict[str, DataFrame]:

    dataframes = {
        table_name: read_csv(f"{csv_folder}/{csv_file}")
        for csv_file, table_name in csv_table_mapping.items()
    }

    holidays = get_public_holidays(public_holidays_url, "2017")

    dataframes["public_holidays"] = holidays

    return dataframes
