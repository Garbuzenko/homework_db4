# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from pprint import pprint

# import sqlalchemy
import sqlalchemy

def query(connection):

    ########### Запросы #######
    print('1 количество исполнителей в каждом жанре')
    sql = """
    SELECT g.name, COUNT(s.SINGER_ID) FROM singers_geners as s
    JOIN gener as g ON g.id = s.geners_id
    GROUP BY g.id ;
    """
    pprint(connection.execute(sql).fetchall())

    print('2 количество треков, вошедших в альбомы 2019-2020 годов')
    sql = """
       SELECT COUNT(t.id) FROM albom as a
       JOIN track as t ON t.albom_id = a.id
       WHERE a.year >= 2019 AND a.year <= 2020;
       """
    pprint(connection.execute(sql).fetchall())


    print('3 средняя продолжительность треков по каждому альбому')
    sql = """
         SELECT a.name, AVG(t.duration_ms) FROM albom as a
         JOIN track as t ON t.albom_id = a.id
         GROUP BY a.id ;
         """
    pprint(connection.execute(sql).fetchall())


    print('4 все исполнители, которые не выпустили альбомы в 2020 году')
    sql = """
             SELECT full_name from singer 
             WHERE ID NOT IN (
                    SELECT s.id FROM singers_alboms as sa
                    INNER JOIN singer as s ON s.id = sa.singer_id
                    INNER JOIN albom as a ON  a.id = sa.albom_id
                    WHERE a.year = 2020
             );
             """
    pprint(connection.execute(sql).fetchall())


    print('5 названия сборников, в которых присутствует конкретный исполнитель (выберите сами)')
    sql = """
                SELECT c.name from collection as c
                WHERE c.id IN (
                       SELECT tc.collection_id FROM tracks_collection as tc
                       INNER JOIN track as t ON t.id = tc.track_id
                       INNER JOIN singer as s ON s.id = t.singer_id
                       WHERE s.full_name = 'Король и Шут'
                );
                """
    pprint(connection.execute(sql).fetchall())

    print('6 название альбомов, в которых присутствуют исполнители более 1 жанра')
    sql = """ 
            SELECT name FROM albom 
            WHERE id in
                ( SELECT sa.albom_id FROM singers_alboms as sa
                JOIN singers_geners as sg ON sg.singer_id = sa.singer_id
                GROUP BY sa.albom_id
                HAVING count(sg.geners_id) > 1 )
        ;"""
    pprint(connection.execute(sql).fetchall())

    print('7 наименование треков, которые не входят в сборники')
    sql = """   SELECT name FROM track
                WHERE id not in
                    ( SELECT track_id FROM tracks_collection )
            ;"""
    pprint(connection.execute(sql).fetchall())

    print('8 исполнителя(-ей), написавшего самый короткий по продолжительности трек (теоретически таких треков может быть несколько)')
    sql = """  SELECT full_name FROM singer
               WHERE id in (SELECT singer_id FROM track WHERE duration_ms in ( SELECT min(duration_ms) FROM track ))
           ;"""
    pprint(connection.execute(sql).fetchall())

    print('9 название альбомов, содержащих наименьшее количество треков')
    sql = """ 
    SELECT name from albom where id in (
        SELECT albom_id FROM track 
        GROUP BY albom_id  
        HAVING count(id)  = (  
                    SELECT count(id) FROM track 
                    GROUP BY albom_id  
                    order by count(id) 
                    limit 1
                    )
        )
          ;"""
    pprint(connection.execute(sql).fetchall())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    db = 'postgresql://postgres:password@localhost:5432/netology_db2'
    engine = sqlalchemy.create_engine(db)
    connection = engine.connect()
    query(connection)
