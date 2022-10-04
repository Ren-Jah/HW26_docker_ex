from flask import Flask, json
import db_manager

app = Flask(__name__)


@app.get("/movie/<title>/")
def film_searcher(title):
    film = db_manager.search_by_name(title)
    founded_film = json.dumps(film, ensure_ascii=False, indent=4)
    return founded_film


@app.get("/movie/<year1>/to/<year2>/")
def films_by_years(year1, year2):
    result = db_manager.search_by_years(year1, year2)
    films = json.dumps(result, ensure_ascii=False, indent=4)
    return films


@app.get("/rating/<rating>/")
def films_by_rating(rating):
    films_by_rate = db_manager.search_by_rating(rating)
    result = json.dumps(films_by_rate, ensure_ascii=False, indent=4)
    return result


@app.get("/genre/<genre>/")
def films_by_genre(genre):
    founded_films_by_genre = db_manager.search_by_genre(genre)
    result = json.dumps(founded_films_by_genre, ensure_ascii=False, indent=4)
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)