from database import get_db_connection

connection = get_db_connection()

print("Connexion à la base réussie !")

parcelles = connection.execute(
    "SELECT COUNT(*) AS total FROM parcelles"
).fetchone()

print("Nombre de parcelles :", parcelles["total"])

connection.close()
