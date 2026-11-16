import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "agriparcelles.sqlite")

QGIS_ROOT = r"C:\Program Files\QGIS 3.44.15"
QGIS_BIN = os.path.join(QGIS_ROOT, "bin")

# Préparer le chargement des DLL de QGIS
_dll_handles = []

for folder in [
    QGIS_BIN,
    os.path.join(QGIS_ROOT, "apps", "Qt5", "bin"),
]:
    if os.path.isdir(folder):
        _dll_handles.append(os.add_dll_directory(folder))

def get_db_connection():
    connection = sqlite3.connect(DB_PATH)

    connection.enable_load_extension(True)

    connection.load_extension(
        os.path.join(QGIS_BIN, "mod_spatialite.dll")
    )

    connection.row_factory = sqlite3.Row

    return connection
