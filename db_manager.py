import sqlite3

from pprint import pprint as pp


def get_data_from_db(sql):
    """ Подключение к БД и получение данных"""
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        res = connection.execute(sql).fetchall()
        return res


def search_by_name(title):
    """Поиск фильма по названию"""
    sql = f'''
    select *
    from netflix
    where title = '{title}'
    order by release_year desc
    limit 1'''

    result = get_data_from_db(sql)
    for item in result:
        return dict(item)


def search_by_years(year1, year2):
    """Поиск фильмов по диапозону годов"""
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


def search_by_rating(rating):
    """Поиск фильмов по рейтингам MPAA"""
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


def search_by_genre(genre):
    """Поиск фильмов по жанру"""
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


def double_play_actors(name1, name2):
    """функцию, которая получает в качестве аргумента имена двух актеров,
     сохраняет всех актеров из колонки cast и возвращает список тех,
      кто играет с ними в паре больше 2 раз.  """
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
    """Поиск фильмов по трем параметрам: тип, год и жанр"""
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

