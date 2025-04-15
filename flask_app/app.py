from flask import Flask, request, jsonify, render_template
import psycopg2

app = Flask(__name__)

# Route pour la racine
@app.route('/')
def index():
    # Servir le fichier HTML pour la carte interactive
    return render_template('index.html')

# Route pour calculer l'itinéraire
@app.route('/get_route', methods=['POST'])
def get_route():
    try:
        # Afficher le contenu brut de la requête et le type de contenu
        print('Contenu brut de la requête:', request.data)
        print('Type de contenu:', request.content_type)

        # Vérifier si le type de contenu est JSON
        if not request.is_json:
            return jsonify({'error': 'Le type de contenu doit être application/json.'}), 400

        # Récupérer les données de la requête
        data = request.get_json()
        print('Données reçues:', data)

        # Vérifier si les paramètres requis sont présents
        if not data or 'start' not in data or 'end' not in data:
            return jsonify({'error': 'Les paramètres start et end sont requis.'}), 400

        # Vérifier si les paramètres sont des entiers
        try:
            start_id = int(data.get('start'))
            end_id = int(data.get('end'))
        except ValueError:
            return jsonify({'error': 'Les paramètres start et end doivent être des entiers.'}), 400

        # Connexion à la base de données
        try:
            conn = psycopg2.connect(
                dbname="access_leg",
                user="bddlona",
                password="BDDLon@acce55LeG",
                host="localhost",
                port=5435
            )
            print("Connexion à la base de données réussie.")
        except psycopg2.Error as db_error:
            print(f"Erreur de connexion à la base de données : {db_error}")
            return jsonify({'error': 'Impossible de se connecter à la base de données.'}), 500

        cursor = conn.cursor()

        # Requête SQL pour pgRouting
        query = """
        SELECT * FROM pgr_dijkstra(
            'SELECT id, source, target, cost FROM accessibilite.troncon_cheminement_noded',
            %s, %s, directed := false
        );
        """
        try:
            cursor.execute(query, (start_id, end_id))
            result = cursor.fetchall()
            print("Résultats SQL :", result)  # Ajout du log pour vérifier les résultats SQL
        except psycopg2.Error as query_error:
            print(f"Erreur lors de l'exécution de la requête SQL : {query_error}")
            return jsonify({'error': 'Erreur lors de l\'exécution de la requête SQL.'}), 500

        # Convertir le résultat en GeoJSON
        try:
            features = []
            for row in result:
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [[row[2], row[3]], [row[4], row[5]]]
                    },
                    "properties": {
                        "cost": row[6]
                    }
                })

            geojson = {
                "type": "FeatureCollection",
                "features": features
            }
            print("GeoJSON généré avec succès :", geojson)  # Ajout du log pour vérifier le GeoJSON
        except Exception as geojson_error:
            print(f"Erreur lors de la conversion en GeoJSON : {geojson_error}")
            return jsonify({'error': 'Erreur lors de la conversion des données en GeoJSON.'}), 500

        # Fermer la connexion à la base de données
        cursor.close()
        conn.close()
        print("Connexion à la base de données fermée.")

        return jsonify(geojson)

    except Exception as e:
        print(f"Erreur serveur : {e}")
        return jsonify({'error': 'Erreur interne du serveur.'}), 500


if __name__ == '__main__':
    print("Démarrage de l'application Flask...")
    app.run(debug=True)