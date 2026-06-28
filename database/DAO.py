from database.DB_connect import DBConnect
from model.arco import Arco
from model.artist import Artist


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGenres():
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct g.GenreId, g.Name
                    from genre g
                    order by g.Name """

        cursor.execute(query)

        for row in cursor:
            result.append((row['GenreId'], row['Name']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllNodes(genreId):
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct a.*
                    from artist a, album ab, track t 
                    where a.ArtistId = ab.ArtistId and ab.AlbumId = t.AlbumId and t.GenreId = %s """

        cursor.execute(query, (genreId, ))

        for row in cursor:
            result.append(Artist(**row))

        cursor.close()
        conn.close()
        return result

    #Sbagliata
    @staticmethod
    def getAllEdges(idMapA, genreId):
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct artist1.artistid as a1, artist2.artistid as a2, (artist1.pop + artist2.pop) as peso
                        from (
                        select  ab.ArtistId, sum(quantity) as pop
                            from album ab, track t, invoiceline i 
                            where ab.AlbumId = t.AlbumId 
                                and i.TrackId =t.TrackId  and t.GenreId = %s
                            group by ab.ArtistId ) artist1,
                        (select  ab.ArtistId, sum(quantity) as pop
                        from album ab, track t, invoiceline i 
                        where ab.AlbumId = t.AlbumId 
                            and i.TrackId =t.TrackId  and t.GenreId = %s
                        group by ab.ArtistId ) artist2,
                        invoice i1, invoice i2, invoiceline il1, invoiceline il2, track t1, track t2, album a1, album a2
                        where i2.CustomerId = i1.CustomerId 
                                                and i1.InvoiceId =il1.InvoiceId and i2.InvoiceId = il2.InvoiceId 
                                                and il1.TracKId=t1.TrackId and il2.TracKId=t2.TrackId
                                                and t1.albumId=a1.AlbumID and t2.albumId=a2.AlbumID
                                                and i1.CustomerId = i2.CustomerId
                                                and t1.GenreId =%s and t2.GenreId =%s
                                                AND a1.ArtistId = artist1.ArtistId   
                                                AND a2.ArtistId = artist2.ArtistId
                                                and artist1.artistid < artist2.artistid  """

        cursor.execute(query, (genreId, genreId, genreId, genreId))

        for row in cursor:
            a1=idMapA[row['a1']]
            a2=idMapA[row['a2']]
            peso=row['peso']
            result.append(Arco(a1, a2, peso))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getPopArtista(genreId):
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select  ab.ArtistId as a, sum(quantity) as popolarita
                from album ab, track t, invoiceline i 
                where ab.AlbumId = t.AlbumId 
                    and i.TrackId =t.TrackId  and t.GenreId = %s
                group by ab.ArtistId """

        cursor.execute(query, (genreId,))

        for row in cursor:
            result.append((row['a'], row['popolarita']))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getCoppieArtisti(genreId):
        # Prende tutti gli stati --> Crea l'oggetto Country
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct ab1.ArtistId as a1, ab2.ArtistId as a2
                    from invoice i1, invoice i2, invoiceline il1, invoiceline il2, track t1, track t2, album ab1, album ab2
                    where i1.CustomerId = i2.CustomerId 
                        and i1.InvoiceId = il1.InvoiceId and i2.InvoiceId = il2.InvoiceId 
                        and il1.TrackId = t1.TrackId and il2.TrackId = t2.TrackId 
                        and t1.AlbumId = ab1.AlbumId and t2.AlbumId = ab2.AlbumId
                        and t1.GenreId = %s and t2.GenreId = %s
                        and ab1.ArtistId < ab2.ArtistId"""

        cursor.execute(query, (genreId, genreId, ))

        for row in cursor:
            result.append((row['a1'], row['a2']))

        cursor.close()
        conn.close()
        return result