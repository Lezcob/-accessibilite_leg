# Creer sont espace de travail

nom : accessibilite_leg
URI de l'espace de nommage : http://localhost:8085/geoserver

Cocher espace de tavail par défault


# Configurer la connection Geoserver avec BDD postgis

## Il va y avoir autant de connection que de schemas dans notre BDD
### Il y a 4 shemas donc il faut recommencer 4 fois l'opération

Aller dans Etrepôts<br>
Ajouter un nouvel entrepôts<br>
Choisir PostGIS - PostGIS database<br>

config:<br>
Espace de travail: accessibilite_leg<br>
Nom de la source de données: ==> le 4 noms pour les 4 shemas : access_leg_tvx - access_leg_lim_admin - access_leg_tpt (tpt pour transport) - access_leg_tvx (tvx pour travaux)<br>
host : db<br>
port: 5432<br>
database: access_leg<br>
schemas : travaux<br>
user et password: cf fichier .env<br>

voici le nom des couches que j'ai nommé dans geoserver:<br>
 	arret (pour arret bus) -  	commune (limite communale) - erp -  	iris (les limites iris) -  	ligne (ligne de bus) -  stationnement_pmr - travaux - troncon_cheminement

## Configurer les style

Recupérer les fichier SLD dans le dossier style_couche_geoserver

### On va configurer les style pour la couche "travaux":
allez dans style et ajouter un nouveau style<br>

puis dans la configuraton du style:<br>
Nom : travaux<br>
Espace de travail : accessibilite_leg<br>
Format : SLD<br>
Fichier de style ==> charger le fichier travaux.sld.<br>
cliquer sur les boutton sauvegarder et appliquer.<br>

