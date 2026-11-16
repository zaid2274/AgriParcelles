import os
import sqlite3

db_path = r"C:\AgriParcelles\data\agriparcelles.sqlite"
qgis_bin = r"C:\Program Files\QGIS 3.44.15\bin"

dll_directory = os.add_dll_directory(qgis_bin)

connection = sqlite3.connect(db_path)
connection.enable_load_extension(True)
connection.load_extension(
    os.path.join(qgis_bin, "mod_spatialite.dll")
)

print("Nombre de parcelles :",
      connection.execute("SELECT COUNT(*) FROM parcelles").fetchone()[0])

print("\nColonnes de la table :")
for column in connection.execute("PRAGMA table_info(parcelles)"):
    print("-", column[1])

print("\nColonne géométrique :")
print(connection.execute("""
    SELECT f_geometry_column, geometry_type, srid
    FROM geometry_columns
    WHERE f_table_name = 'parcelles'
""").fetchone())

print("\nIndex spatial :")
print(connection.execute("""
    SELECT name FROM sqlite_master
    WHERE type = 'table' AND name LIKE 'idx_parcelles_geom%'
""").fetchall())

connection.close()
