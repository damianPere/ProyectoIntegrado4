from typing import Dict

from pandas import DataFrame
from sqlalchemy.engine.base import Engine


def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
        database (Engine): SQLAlchemy engine for database connection
    """

    try:
        # Iteramos sobre cada par de nombre de tabla y DataFrame en el diccionario
        for table_name, df in data_frames.items():
            # Luego cargamos el DataFrame a la base de datos SQLite
            # Usamos if_exists='replace' sobreescribe la tabla si ya existe
            # Con index=False evitamos que el índice del DataFrame se guarde como una columna adicional en la tabla
            df.to_sql(table_name, database, if_exists="replace", index=False)

    except Exception as e:
        # Si ocurre algún error durante la carga, lanzamos un SystemExit con el mensaje
        raise SystemExit(f"Error al cargar los datos en la base de datos: {e}")

    # Finalmente imprimimos mensaje de éxito cuando todas las tablas se han cargado
    print("\nCarga de datos finalizada exitosamente!")
