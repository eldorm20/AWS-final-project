# Top IMDB Movies Flask App

This is a Flask web application that fetches and displays a list of top IMDB movies from a PostgreSQL database. It also allows users to add and delete movies through a web interface.

## Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/eldorm20/AWS-final-project.git](https://github.com/eldorm20/AWS-final-project.git)
    cd AWS-final-project/webapp_eldor
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt # If you have a requirements.txt
    ```
3.  Configure database credentials in `app.py`. Make sure the PostgreSQL database is running and accessible.

## Usage

1.  Run the Flask application:
    ```bash
    python app.py
    ```
2.  Access the web interface by opening the `inde_eldor.html` file (hosted on S3). The JavaScript in this file will interact with the Flask API endpoints:
    * `/movies` (GET): To retrieve the list of movies.
    * `/movies` (POST): To add a new movie (sends JSON data).
    * `/movies/<rank_id>` (DELETE): To delete a movie by its Rank.

## Technologies Used

* Python
* Flask
* psycopg2 (for PostgreSQL interaction)
* HTML
* CSS
* JavaScript

## Deployment

(Add any specific deployment instructions here if applicable)
