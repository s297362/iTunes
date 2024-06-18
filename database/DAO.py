from database.DB_connect import DBConnect
from model.album import Album
from model.arco import Arco


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_nodi():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT a.AlbumId, a.Title, SUM(t.Milliseconds)/60000 as Durata
from album a, track t 
where a.AlbumId = t.AlbumId
group by a.AlbumId"""
        cursor.execute(query, ())
        result = []
        for r in cursor:
            result.append(Album(**r))
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """SELECT t.AlbumId AS Nodo1, t2.AlbumId  AS Nodo2, COUNT(*) AS Weight
from playlisttrack p, playlisttrack p2, track t, track t2 
where t.TrackId = p.TrackId AND p2.TrackId = t2.TrackId AND t2.AlbumId < t.AlbumID AND p2.PlaylistId = p.PlaylistId
GROUP BY t.AlbumId , t2.AlbumId """
        cursor.execute(query, ())
        results = []
        for row in cursor:
            results.append(Arco(**row))
        return results
