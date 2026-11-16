from database import get_db_connection

connection = get_db_connection()

try:
    curseur = connection.execute(
        "DELETE FROM parcelles WHERE num_parcelle = ?",
        ("TEST-001",)
    )
    connection.commit()

    if curseur.rowcount == 1:
        print("Parcelle TEST-001 supprimée avec succès.")
    else:
        print("Aucune parcelle TEST-001 trouvée.")

finally:
    connection.close()
