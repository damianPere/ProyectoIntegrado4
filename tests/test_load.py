from src.config import DATASET_ROOT_PATH, PUBLIC_HOLIDAYS_URL, get_csv_to_table_mapping
from src.config import get_csv_to_table_mapping
from src.extract import extract, get_public_holidays
from src.load import load


def test_load():
    #     """Test the extract function."""
    csv_folder = DATASET_ROOT_PATH
    print(" csv_folder:", csv_folder)
    csv_table_mapping = get_csv_to_table_mapping()
    public_holidays_url = PUBLIC_HOLIDAYS_URL
    dataframes = extract(csv_folder, csv_table_mapping, public_holidays_url)
    print("Nombres de las tablas:", len(list(dataframes.keys())))
