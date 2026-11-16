from flask import Flask, jsonify, render_template, request
from scripts.database import get_db_connection
import sqlite3
import ee

app = Flask(__name__)

# Connexion à Google Earth Engine pour le calcul du NDVI
ee.Initialize(project="projetpython-492711")

CULTURES = [
    "Blé dur",
    "Blé tendre",
    "Orge",
    "Maïs",
    "Betterave sucrière",
    "Olivier",
    "Agrumes",
    "Maraîchage",
    "Luzerne",
    "Jachère",
    "Autre"
]


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/api/parcelles", methods=["GET"])
def get_parcelles():
    connection = get_db_connection()

    try:
        rows = connection.execute("""
            SELECT
                id,
                num_parcelle,
                agriculteur,
                culture,
                superficie_ha,
                production_t,
                date_saisie,
                AsGeoJSON(geom) AS geometrie
            FROM parcelles
        """).fetchall()

        import json

        features = []

        for row in rows:
            if row["geometrie"] is None:
                continue

            features.append({
                "type": "Feature",
                "geometry": json.loads(row["geometrie"]),
                "properties": {
                    "id": row["id"],
                    "num_parcelle": row["num_parcelle"],
                    "agriculteur": row["agriculteur"],
                    "culture": row["culture"],
                    "superficie_ha": row["superficie_ha"],
                    "production_t": row["production_t"],
                    "date_saisie": row["date_saisie"]
                }
            })

        return jsonify({
            "type": "FeatureCollection",
            "features": features
        })

    finally:
        connection.close()


@app.route("/api/parcelles", methods=["POST"])
def ajouter_parcelle():
    donnees = request.get_json(silent=True)

    if not donnees:
        return jsonify({"erreur": "Données JSON manquantes."}), 400

    num_parcelle = donnees.get("num_parcelle")
    agriculteur = donnees.get("agriculteur")
    culture = donnees.get("culture")
    production = donnees.get("production_t")
    geometrie = donnees.get("geometry")

    if not isinstance(num_parcelle, str) or not num_parcelle.strip():
        return jsonify({"erreur": "Le numéro de parcelle est obligatoire."}), 400

    if not isinstance(agriculteur, str) or not agriculteur.strip():
        return jsonify({"erreur": "Le nom de l'agriculteur est obligatoire."}), 400

    if culture not in CULTURES:
        return jsonify({"erreur": "La culture sélectionnée est invalide."}), 400

    if isinstance(production, bool) or not isinstance(production, (int, float)):
        return jsonify({"erreur": "La production doit être un nombre."}), 400

    if production < 0:
        return jsonify({"erreur": "La production doit être supérieure ou égale à zéro."}), 400

    if not isinstance(geometrie, dict) or geometrie.get("type") != "Polygon":
        return jsonify({"erreur": "La géométrie doit être un polygone GeoJSON."}), 400

    import json

    connection = get_db_connection()

    try:
        # Vérifier l'unicité du numéro
        existe = connection.execute(
            "SELECT 1 FROM parcelles WHERE num_parcelle = ?",
            (num_parcelle.strip(),)
        ).fetchone()

        if existe:
            return jsonify({
                "erreur": "Ce numéro de parcelle existe déjà."
            }), 409

        geojson = json.dumps(geometrie)

        # Convertir la géométrie, vérifier sa validité et calculer la superficie
        resultat = connection.execute("""
            SELECT
                ST_IsValid(
                    SetSRID(GeomFromGeoJSON(?), 4326)
                ),
                ST_Area(
                    SetSRID(GeomFromGeoJSON(?), 4326),
                    1
                ) / 10000
        """, (geojson, geojson)).fetchone()

        if resultat is None or resultat[0] != 1:
            return jsonify({
                "erreur": "La géométrie du polygone est invalide."
            }), 400

        superficie = resultat[1]

        if superficie is None or superficie <= 0:
            return jsonify({
                "erreur": "La superficie calculée est invalide."
            }), 400

        connection.execute("""
            INSERT INTO parcelles (
                num_parcelle,
                agriculteur,
                culture,
                superficie_ha,
                production_t,
                geom
            )
            VALUES (
                ?, ?, ?, ?, ?,
                SetSRID(GeomFromGeoJSON(?), 4326)
            )
        """, (
            num_parcelle.strip(),
            agriculteur.strip(),
            culture,
            superficie,
            production,
            geojson
        ))

        connection.commit()

        return jsonify({
            "message": "Parcelle enregistrée avec succès.",
            "num_parcelle": num_parcelle.strip(),
            "superficie_ha": superficie
        }), 201

    except sqlite3.IntegrityError:
        connection.rollback()
        return jsonify({
            "erreur": "Ce numéro de parcelle existe déjà."
        }), 409

    except Exception:
        connection.rollback()
        app.logger.exception("Erreur lors de l'enregistrement de la parcelle")
        return jsonify({
            "erreur": "Une erreur est survenue lors de l'enregistrement."
        }), 500

    finally:
        connection.close()

@app.route("/api/parcelles/<int:parcelle_id>", methods=["DELETE"])
def supprimer_parcelle(parcelle_id):
    connection = get_db_connection()

    try:
        parcelle = connection.execute(
            "SELECT id FROM parcelles WHERE id = ?",
            (parcelle_id,)
        ).fetchone()

        if parcelle is None:
            return jsonify({
                "erreur": "Parcelle introuvable."
            }), 404

        connection.execute(
            "DELETE FROM parcelles WHERE id = ?",
            (parcelle_id,)
        )

        connection.commit()

        return jsonify({
            "message": "Parcelle supprimée avec succès."
        }), 200

    except Exception:
        connection.rollback()
        app.logger.exception("Erreur lors de la suppression de la parcelle")
        return jsonify({
            "erreur": "Une erreur est survenue lors de la suppression."
        }), 500

    finally:
        connection.close()


@app.route("/api/parcelles/superficie", methods=["POST"])
def calculer_superficie():
    donnees = request.get_json(silent=True)

    if not donnees:
        return jsonify({"erreur": "Données JSON manquantes."}), 400

    geometrie = donnees.get("geometry")

    if not isinstance(geometrie, dict) or geometrie.get("type") != "Polygon":
        return jsonify({"erreur": "La géométrie doit être un polygone."}), 400

    import json

    connection = get_db_connection()

    try:
        geojson = json.dumps(geometrie)

        resultat = connection.execute("""
            SELECT
                ST_IsValid(
                    SetSRID(GeomFromGeoJSON(?), 4326)
                ),
                ST_Area(
                    SetSRID(GeomFromGeoJSON(?), 4326),
                    1
                ) / 10000
        """, (geojson, geojson)).fetchone()

        if resultat is None or resultat[0] != 1:
            return jsonify({"erreur": "Polygone invalide."}), 400

        superficie = resultat[1]

        if superficie is None or superficie <= 0:
            return jsonify({"erreur": "Superficie invalide."}), 400

        return jsonify({
            "superficie_ha": superficie
        }), 200

    finally:
        connection.close()
@app.route("/api/parcelles/<int:parcelle_id>/ndvi", methods=["GET"])
def calculer_ndvi(parcelle_id):
    import json
    from datetime import date, timedelta

    connection = get_db_connection()

    try:
        parcelle = connection.execute(
            """
            SELECT AsGeoJSON(geom) AS geometrie
            FROM parcelles
            WHERE id = ?
            """,
            (parcelle_id,)
        ).fetchone()
    finally:
        connection.close()

    if parcelle is None or parcelle["geometrie"] is None:
        return jsonify({"erreur": "Parcelle introuvable."}), 404

    try:
        geometrie = json.loads(parcelle["geometrie"])
        zone = ee.Geometry(geometrie)

        # Dates personnalisées envoyées par l'interface
        date_debut_choisie = request.args.get("date_debut")
        date_fin_choisie = request.args.get("date_fin")

        fin = date.today()
        debut = fin - timedelta(days=60)

        # Utiliser les dates personnalisées si elles sont fournies
        if date_debut_choisie or date_fin_choisie:
            if not date_debut_choisie or not date_fin_choisie:
                return jsonify({
                    "erreur": "Veuillez renseigner les deux dates."
                }), 400

            try:
                debut = date.fromisoformat(date_debut_choisie)
                fin = date.fromisoformat(date_fin_choisie)
            except ValueError:
                return jsonify({
                    "erreur": "Format de date invalide. Utilisez AAAA-MM-JJ."
                }), 400

            if debut >= fin:
                return jsonify({
                    "erreur": "La date de début doit précéder la date de fin."
                }), 400

            if fin > date.today():
                return jsonify({
                    "erreur": "La date de fin ne peut pas être dans le futur."
                }), 400
        
        images = (
            ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
            .filterBounds(zone)
            .filterDate(debut.isoformat(), (fin + timedelta(days=1)).isoformat())
            .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 20))
        )

        nombre_images = images.size().getInfo()

        if nombre_images == 0:
            return jsonify({
                "erreur": "Aucune image Sentinel-2 disponible pour cette période."
            }), 404

        # Masquer les nuages et leurs ombres avec la bande SCL
        def masquer_nuages(image):
            scl = image.select("SCL")

            masque = (
                scl.neq(0)
                .And(scl.neq(1))
                .And(scl.neq(3))
                .And(scl.neq(8))
                .And(scl.neq(9))
                .And(scl.neq(10))
                .And(scl.neq(11))
            )

            return image.updateMask(masque)

        # Créer une image composite sans les pixels masqués
        image = images.map(masquer_nuages).median()

        ndvi = image.normalizedDifference(
            ["B8", "B4"]
        ).rename("NDVI")

        moyenne = ndvi.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=zone,
            scale=10,
            maxPixels=1000000
        ).get("NDVI").getInfo()

        if moyenne is None:
            return jsonify({
                "erreur": "Aucune valeur NDVI exploitable pour cette parcelle."
            }), 404

        carte = ndvi.clip(zone).getMapId({
            "min": -0.2,
            "max": 0.8,
            "palette": [
                "#c62828",
                "#f39c12",
                "#f4d03f",
                "#8bc34a",
                "#1b7f43"
            ]
        })

        return jsonify({
            "ndvi_moyen": round(moyenne, 3),
            "url_carte": carte["tile_fetcher"].url_format,
            "date_debut": debut.isoformat(),
            "date_fin": fin.isoformat(),
            "nombre_images": nombre_images
        }), 200

    except Exception:
        app.logger.exception("Erreur lors du calcul NDVI")
        return jsonify({
            "erreur": "Le calcul NDVI a échoué."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)
