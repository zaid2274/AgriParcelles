import os
import sqlite3

p = r"C:\Program Files\QGIS 3.44.15\bin"

dll_directory = os.add_dll_directory(p)

connection = sqlite3.connect(":memory:")
connection.enable_load_extension(True)

connection.load_extension(
    os.path.join(p, "mod_spatialite.dll")
)

version = connection.execute(
    "SELECT spatialite_version()"
).fetchone()[0]

print("SpatiaLite fonctionne !")
print("Version :", version)
