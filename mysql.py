import pymysql
import csv
import json
import sys

def main():
    if len(sys.argv) == 3:
        login(sys.argv[1], sys.argv[2], 0)

    elif len(sys.argv) == 4:
        login(sys.argv[1], sys.argv[2], int(sys.argv[3]))

    else:
        print("YOU CAN'T DO THAT!!!")


def login(username, password, query):  # this will check for the login and retrieve the data wanted

    try:
        conn = pymysql.connect(host='localhost', port=3306, user=username, passwd=password, db='python_mysql')

        cur = conn.cursor()

        createtable(cur, conn)

    except:
        print("something")


def createtable(cur, conn):

            print(conn)
            cur = conn.cursor()
            print(cur)

            sqlQuery = "CREATE TABLE IF NOT EXISTS movies( movie_id INT, budget INT null ,homepage VARCHAR(256) , original_language VARCHAR(2), original_title VARCHAR(256), \
                         overview VARCHAR(2064), popularity FLOAT, release_date VARCHAR(10), revenue double, runtime INT , status VARCHAR(20), tagline VARCHAR(256), \
                        title VARCHAR(128),vote_average FLOAT, vote_count INT ,PRIMARY KEY(movie_id))"

            genres = "CREATE TABLE if not exists genres(genre_id INT, type VARCHAR(500), PRIMARY KEY (genre_id , type))"
            genre_relationship = "CREATE TABLE IF NOT EXISTS genre_relationship(id INT, movie_id INT, genre_id INT, PRIMARY KEY (id) , \
                                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id),  FOREIGN KEY (genre_id) REFERENCES genres(genre_id))"

            keywords = "CREATE TABLE IF NOT EXISTS keywords( keyboard_id BIGINT, keyboard_name varchar(500), PRIMARY KEY (keyboard_id,keyboard_name))"
            keywords_relationship = "CREATE TABLE IF NOT EXISTS keywords_relationship(id INT, movie_id INT, keyboard_id BIGINT, PRIMARY KEY (id), \
                                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id),  FOREIGN KEY (keyboard_id) REFERENCES keywords(keyboard_id))"

            production_companies = "CREATE TABLE IF NOT EXISTS production_companies( companies_id INT, company_name varchar(500), PRIMARY KEY (companies_id))"
            production_companies_relationship = "CREATE TABLE IF NOT EXISTS production_companies_relationship(id INT, movie_id INT, companies_id INT, PRIMARY KEY (id), \
                                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id),  FOREIGN KEY (companies_id) REFERENCES production_companies(companies_id))"

            production_countries = "CREATE TABLE IF NOT EXISTS production_countries( country_id varchar(10), country_name varchar(500), PRIMARY KEY (country_id))"
            production_countries_relationship = "CREATE TABLE IF NOT EXISTS production_countries_relationship(id INT, movie_id INT, country_id varchar(2), PRIMARY KEY (id), \
                                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id),  FOREIGN KEY (country_id) REFERENCES production_countries(country_id))"

            spoken_languages = "CREATE TABLE IF NOT EXISTS spoken_languages(language_id varchar(10), language_name varchar(500), PRIMARY KEY (language_id))"
            spoken_languages_relationship = "CREATE TABLE IF NOT EXISTS spoken_languages_relationship(id INT, movie_id INT, language_id varchar(10), PRIMARY KEY (id), \
                                      FOREIGN KEY (movie_id) REFERENCES movies(movie_id),  FOREIGN KEY (language_id) REFERENCES spoken_languages(language_id))"
            cur.execute(sqlQuery)
            cur.execute(genres)
            cur.execute(genre_relationship)
            cur.execute(keywords)
            cur.execute(keywords_relationship)
            cur.execute(production_companies)
            cur.execute(production_companies_relationship)
            cur.execute(production_countries)
            cur.execute(production_countries_relationship)
            cur.execute(spoken_languages)
            cur.execute(spoken_languages_relationship)

            cur.execute("SET FOREIGN_KEY_CHECKS = 0")

            loop1 = 0
            loop2 = 0
            loop3 = 0
            loop4 = 0
            loop5 = 0
            i = 0
            j = 0
            k = 0
            m = 0
            p = 0
            with open(r'C:\Users\srava\OneDrive\Desktop\tmdb_5000_movies.csv', encoding='utf8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        moviegenres = json.loads(row['genres'])
                        moviekeywords = json.loads(row['keywords'])
                        movieproduction_companies = json.loads(row['production_companies'])
                        movieproduction_countries = json.loads(row['production_countries'])
                        moviespoken_languages = json.loads(row['spoken_languages'])
                        if not i:
                                i = i + 1
                        if not j:
                                j = j+1
                        if not k:
                                k = k+1
                        if not m:
                                m = m+1
                        if not p:
                                p = p+1
                        else:
                            sql_statement = "INSERT INTO movies(movie_id, budget, homepage,\
                                    original_language, original_title, overview, popularity,\
                                    release_date, revenue, runtime, status, tagline, title,\
                                    vote_average, vote_count) VALUES (%s, %s, %s, %s, %s, %s,\
                                     %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            cur.execute(sql_statement, (row['id'], row['budget'], row['homepage'], row['original_language'],
                                                row['original_title'], row['overview'], row['popularity'], row['release_date'],
                                                row['revenue'], row['runtime'] if row['runtime'] != "" else row['runtime'] == '\0',
                                                row['status'], row['tagline'],
                                                row['title'], row['vote_average'], row['vote_count']))

                        for i in range(len(moviegenres)):
                            store1 = moviegenres[i]['id']
                            store2 = moviegenres[i]['name']

                            cur.execute("REPLACE INTO genres(genre_id,type) VALUES (%s,%s)", (store1, store2))
                            cur.execute("INSERT INTO genre_relationship(id,movie_id,genre_id) VALUES (%s,%s,%s)",(loop1, row['id'], store1))
                            loop1 = loop1 + 1

                        for j in range (len(moviekeywords)):
                            store3 = moviekeywords[j]['id']
                            store4 = moviekeywords[j]['name']
                            cur.execute("REPLACE INTO keywords(keyboard_id,keyboard_name) VALUES (%s,%s)", (store3, store4))

                            cur.execute("INSERT INTO keywords_relationship(id,movie_id,keyboard_id) VALUES (%s,%s,%s)",(loop2, row['id'], store3))
                            loop2 = loop2+1

                        for k in range(len(movieproduction_companies)):
                            store5 = movieproduction_companies[k]['name']
                            store6 = movieproduction_companies[k]['id']
                            cur.execute("REPLACE INTO production_companies(company_name, companies_id) VALUES (%s,%s)",(store5, store6))
                            cur.execute("INSERT INTO production_companies_relationship(id,movie_id,companies_id) VALUES (%s,%s,%s)",(loop3, row['id'], store6))
                            loop3 = loop3+1

                        for m in range(len(movieproduction_countries)):
                            store7 = movieproduction_countries[m]['iso_3166_1']
                            store8 = movieproduction_countries[m]['name']
                            cur.execute("REPLACE INTO production_countries(country_id, country_name) VALUES (%s,%s)",(store7, store8))
                            cur.execute("INSERT INTO production_countries_relationship(id,movie_id,country_id) VALUES (%s,%s,%s)",(loop4, row['id'], store7))
                            loop4 = loop4 + 1

                        for p in range(len(moviespoken_languages)):
                            store9 = moviespoken_languages[p]['iso_639_1']
                            store10 = moviespoken_languages[p]['name']
                            cur.execute("REPLACE INTO spoken_languages(language_id, language_name) VALUES (%s,%s)", (store9, store10))
                            cur.execute("INSERT INTO spoken_languages_relationship(id, movie_id, language_id) VALUES (%s,%s,%s)",(loop5, row['id'], store9))
                            loop5 = loop5 + 1
                        conn.commit()
            cur.execute("SET FOREIGN_KEY_CHECKS = 1")

def qOne(cur, conn):
    save1 = "SELECT AVG(budget) FROM movie"
    cur.execute(save1)
    print("")
    print("Query 1: What is the average budget of all movies?")
    print("$%s" % cur.fetchone())
# def qTwo():
#     save 2 = ""


if __name__ == "__main__":
    main()

