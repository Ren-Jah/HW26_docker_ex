# import db_manager
import sqlite3
from flask import Flask, json
from pprint import pprint as pp

app = Flask(__name__)


def get_data_from_db(sql):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        res = connection.execute(sql).fetchall()
        return res


def search_by_name(title):
    sql = f'''
    select *
    from netflix
    where title = '{title}'
    order by release_year desc
    limit 1'''

    result = get_data_from_db(sql)
    for item in result:
        return dict(item)


@app.get("/movie/<title>/")
def film_searcher(title):
    film = search_by_name(title)
    founded_film = json.dumps(film, ensure_ascii=False, indent=4)
    return founded_film


def search_by_years(year1, year2):
    sql = f'''
    select title, release_year
    from netflix
    where release_year between '{year1}' and '{year2}'
    order by release_year desc
    limit 100'''

    founded_films = []
    for item in get_data_from_db(sql):
        founded_films.append(dict(item))

    return founded_films


@app.get("/movie/<year1>/to/<year2>/")
def films_by_years(year1, year2):
    result = search_by_years(year1, year2)
    films = json.dumps(result, ensure_ascii=False, indent=4)
    return films


def search_by_rating(rating):
    rating_dict = {
        "children":("G", "G"),
        "family": ("G", "PG", "PG-13"),
        "adult":("R", "NC-17")
    }

    sql = f'''
        select title, rating, description
        from netflix
        where rating in {rating_dict.get(rating, ("R", "R"))}
        '''

    rated_films = []
    for item in get_data_from_db(sql):
        rated_films.append(dict(item))

    return rated_films


@app.get("/rating/<rating>/")
def films_by_rating(rating):
    films_by_rate = search_by_rating(rating)
    result = json.dumps(films_by_rate, ensure_ascii=False, indent=4)
    return result


def search_by_genre(genre):
    sql = f'''
    select *
    from netflix
    where listed_in like '%{genre}%'
    order by release_year desc
    limit 10'''

    listed_in_films = []
    result = get_data_from_db(sql)
    for item in result:
        listed_in_films.append(dict(item))

    return listed_in_films


@app.get("/genre/<genre>/")
def films_by_genre(genre):
    founded_films_by_genre = search_by_genre(genre)
    result = json.dumps(founded_films_by_genre, ensure_ascii=False, indent=4)
    return result


def double_play_actors(name1, name2):
    sql = f'''
    select *
    from netflix
    where "cast" like '%{name1}%' and "cast" like '%{name2}%' '''
    data = get_data_from_db(sql)
    result_actors = []
    names_dict = {}
    for item in data:
        names = set(dict(item).get('cast').split(",")) - set([name1, name2])

        for name in names:
            names_dict[str(name).strip()] = names_dict.get(str(name).strip(), 0) + 1

    for key, value in names_dict.items():
        if value >= 2:
            result_actors.append(key)

    return result_actors


def search_by_three_params(kind, year, genre):
    sql = f'''
        select title, description, listed_in
        from netflix
        where type = '{kind}'
        and release_year = '{year}'
        and listed_in like '%{genre}%' '''

    films = []
    for item in get_data_from_db(sql):
        films.append(dict(item))

    return films


if __name__ == '__main__':
    app.run(debug=True)


