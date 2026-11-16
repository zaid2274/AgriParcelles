import os
import sqlite3

# Chemins du projet
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "agriparcelles.sqlite")
SCHEMA_PATH = os.path.join(BASE_DIR, "sql", "schema.sql")

# Bibliothèque SpatiaLite fournie avec QGIS
QGIS_BIN = r"C:\Program Files\QGIS 3.44.15\bin"
dll_directory = os.add_dll_directory(QGIS_BIN)

# Lire le fichier SQL
with open(SCHEMA_PATH, "r", encoding="utf-8-sig") as file:
    schema_sql = file.read()

# Créer la base et exécuter le schéma
connection = sqlite3.connect(DB_PATH)
connection.enable_load_extension(True)
connection.load_extension(os.path.join(QGIS_BIN, "mod_spatialite.dll"))

connection.executescript(schema_sql)
connection.commit()

# Vérifications
version = connection.execute(
    "SELECT spatialite_version()"
).fetchone()[0]

columns = connection.execute(
    "PRAGMA table_info(parcelles)"
).fetchall()

geometry = connection.execute("""
    SELECT f_geometry_column, geometry_type, srid
    FROM geometry_columns
    WHERE f_table_name = 'parcelles'
""").fetchone()

print("Base de données créée avec succès !")
print("Fichier :", DB_PATH)
print("SpatiaLite :", version)
print("Colonnes :", [column[1] for column in columns])
print("Géométrie :", geometry)

connection.close()
