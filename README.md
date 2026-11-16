\# 🌱 AgriParcelles



\*\*Application web de gestion et de cartographie des parcelles agricoles avec analyse NDVI par satellite.\*\*



\## Présentation



AgriParcelles est une application web développée avec Python et Flask permettant de digitaliser, enregistrer, visualiser et gérer des parcelles agricoles.



Elle intègre également une fonctionnalité d'analyse de la végétation à partir d'images Sentinel-2, grâce à Google Earth Engine.



Le projet a été réalisé dans un cadre pédagogique et peut être adapté à d'autres zones agricoles.



\## Technologies utilisées



\- \*\*Python / Flask\*\* : serveur web et API.

\- \*\*SQLite / SpatiaLite\*\* : stockage des parcelles et de leurs géométries.

\- \*\*Leaflet\*\* : affichage cartographique interactif.

\- \*\*Leaflet-Geoman\*\* : dessin et édition des parcelles.

\- \*\*Google Earth Engine\*\* : traitement des images satellites.

\- \*\*Sentinel-2\*\* : images utilisées pour calculer le NDVI.

\- \*\*HTML / CSS / JavaScript\*\* : interface utilisateur.



\## Fonctionnalités



\- Affichage d'une carte interactive.

\- Digitalisation de parcelles agricoles.

\- Enregistrement des attributs : numéro, agriculteur, culture et production.

\- Calcul automatique de la superficie en hectares.

\- Visualisation et navigation entre les parcelles.

\- Suppression de parcelles.

\- Calcul du NDVI moyen par parcelle.

\- Sélection de la période d'analyse NDVI.

\- Affichage de la couche NDVI sur la carte.

\- Exportation des données au format CSV.



\## Zone d'étude



La zone initiale du projet est \*\*Z5 — Souss, Ouled Teïma (Maroc)\*\*.



\- Latitude : 30.40

\- Longitude : -9.21

\- Rayon de sélection : environ 10 km

\- Objectif pédagogique : digitaliser 15 parcelles agricoles.



\*\*État du projet :\*\* la digitalisation des 15 parcelles reste à compléter.



L'application peut également être utilisée pour digitaliser des parcelles dans d'autres régions.



\## Installation



\### 1. Récupérer le projet



```bash

git clone https://github.com/zaid2274/AgriParcelles.git

cd AgriParcelles

```



\### 2. Créer un environnement Python



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Installer les dépendances



```powershell

pip install -r requirements.txt

```



\### 4. Configurer les services nécessaires



L'application nécessite une installation compatible de \*\*SpatiaLite\*\* et une configuration de \*\*Google Earth Engine\*\* pour les analyses NDVI.



Chaque utilisateur doit utiliser ses propres identifiants Google Earth Engine.



La base SQLite locale n'est pas incluse dans le dépôt. Elle doit être initialisée avant la première utilisation, selon le schéma et les scripts fournis dans le projet.



\### 5. Lancer l'application



Après avoir configuré l'environnement Python, SpatiaLite, la base de données et Google Earth Engine :



```powershell

python app.py

```



Ouvrir ensuite :



`http://127.0.0.1:5000`



\*\*Remarque :\*\* sous Windows, le chargement de SpatiaLite peut nécessiter une configuration particulière de l'environnement QGIS. La commande de lancement doit alors être adaptée à l'installation locale.



\## Structure du projet



```text

AgriParcelles/

├── app.py

├── requirements.txt

├── templates/

│   └── index.html

├── scripts/

├── sql/

│   └── schema.sql

├── test\_spatialite.py

└── README.md

```



Le dossier `data/` contient la base de données locale et n'est pas publié sur GitHub.



\## Calcul du NDVI



Le NDVI (\*Normalized Difference Vegetation Index\*) est un indicateur permettant d'évaluer l'activité de la végétation.



Sa formule est :



\*\*NDVI = (B8 − B4) / (B8 + B4)\*\*



Avec :



\- \*\*B8\*\* : bande proche infrarouge de Sentinel-2.

\- \*\*B4\*\* : bande rouge de Sentinel-2.



Les images sont filtrées selon la zone géographique, la période et la couverture nuageuse. Un masque basé sur la bande SCL permet de réduire l'influence des nuages et de leurs ombres.



\## Réutilisation du projet



Le code peut servir de base à la création d'autres projets de digitalisation agricole.



Chaque utilisateur peut choisir sa zone d'étude, créer ses parcelles et enregistrer ses propres données dans une base locale.



\## État du développement



Le projet est fonctionnel dans son environnement de développement initial. La configuration sur d'autres ordinateurs peut nécessiter des adaptations, notamment pour SpatiaLite et Google Earth Engine.



Les 15 parcelles prévues dans la zone Z5 seront ajoutées ultérieurement.



\## Auteur



\*\*GitHub :\*\* \[zaid2274](https://github.com/zaid2274)



Projet pédagogique de cartographie agricole.

