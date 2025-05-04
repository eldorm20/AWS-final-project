from flask import Flask, jsonify, request
import psycopg2
from flask_cors import CORS # For handling cross-origin requests

app = Flask(__name__)
CORS(app) # Enable CORS for all routes (for simplicity in this example)

# Database credentials (replace with your actual values)
DB_HOST = "db-eldor.ct6ei6agkus4.ap-south-1.rds.amazonaws.com"
DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
TABLE_NAME = "tbl_eldor_imdb_movies"

def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
    return conn

@app.route('/movies', methods=['GET'])
def get_movies():
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        cur.execute(f"SELECT Rank, Title, Year, Rating, Runtime FROM {TABLE_NAME} ORDER BY Rank;")
        movies = cur.fetchall()
        cur.close()
        conn.close()
        movie_list = []
        for movie in movies:
            movie_list.append({
                'Rank': movie[0],
                'Title': movie[1],
                'Year': movie[2],
                'Rating': float(movie[3]),
                'Runtime': movie[4]
            })
        return jsonify(movie_list)
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(f"INSERT INTO {TABLE_NAME} (Title, Year, Rating, Runtime) VALUES (%s, %s, %s, %s);",
                        (data.get('title'), data.get('year'), data.get('rating'), data.get('runtime')))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({'message': 'Movie added successfully'}), 201
        except psycopg2.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'error': f'Error adding movie: {e}'}), 500
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

@app.route('/movies/<int:rank_id>', methods=['DELETE'])
def delete_movie(rank_id):
    conn = get_db_connection()
    if conn:
        cur = conn.cursor()
        try:
            cur.execute(f"DELETE FROM {TABLE_NAME} WHERE Rank = %s;", (rank_id,))
            conn.commit()
            cur.close()
            conn.close()
            if cur.rowcount > 0:
                return jsonify({'message': f'Movie with Rank {rank_id} deleted successfully'}), 200
            else:
                return jsonify({'message': f'Movie with Rank {rank_id} not found'}), 404
        except psycopg2.Error as e:
            conn.rollback()
            cur.close()
            conn.close()
            return jsonify({'error': f'Error deleting movie: {e}'}), 500
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
