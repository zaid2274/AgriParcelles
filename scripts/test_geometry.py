import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.database import get_db_connection

connection = get_db_connection()

print("Test ST_IsValid :",
      connection.execute(
          "SELECT ST_IsValid(GeomFromText('POLYGON((-9.21 30.40,-9.20 30.40,-9.20 30.41,-9.21 30.41,-9.21 30.40))',4326))"
      ).fetchone()[0])

print("Test ST_Area :",
      connection.execute(
          "SELECT ST_Area(GeomFromText('POLYGON((-9.21 30.40,-9.20 30.40,-9.20 30.41,-9.21 30.41,-9.21 30.40))',4326),1)/10000"
      ).fetchone()[0])

connection.close()
