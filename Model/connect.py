import pyodbc
server = 'DESKTOP-GPM5SKT\SQLEXPRESS'
database = 'MOVIE'
username = 'MANAGER'
password = '123'
# ENCRYPT defaults to yes starting in ODBC Driver 18. It's good to always specify ENCRYPT=yes on the client side to avoid MITM attacks.
cnxn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-GPM5SKT\SQLEXPRESS;"
            "Database=MOVIE;"
            "Trusted_Connection=yes;")
cnxn = pyodbc.connect(cnxn_str)
cursor = cnxn.cursor()
#sample
# cursor.execute(""" SELECT * FROM MOVIE """)
# res = cursor.fetchall() #list
# print(res)



def insert_movie(Movie_vn, Movie_en, link, rating, url_img,label):
    cursor.execute("""
        INSERT INTO Movie(Movie_vn, Movie_en, link, url_img, rating, the_number_of_views,label)
        VALUES(?, ?, ?, ?,?,?,?)
    """, Movie_vn, Movie_en, link, url_img, rating, 0,label)
    cnxn.commit()
    # cnxn.close()


def select_name_movie(name):
    cursor.execute(f"""
        select * from Movie where Movie_vn like N'%{name}%' or Movie_en like N'%{name}%' order by rating DESC
    """)
    res = [dict((cursor.description[i][0], value)
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    return res

def select_movie(label):
    cursor.execute("""
        select * from Movie where label=? order by rating DESC
    """, int(label))
    res = [dict((cursor.description[i][0], value)
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    return res

def select_polular_movie():
    cursor.execute("""
        select * from Movie order by MovieId DESC
    """)
    res = [dict((cursor.description[i][0], value)
               for i, value in enumerate(row)) for row in cursor.fetchall()]
    print(type(res))
    return res
if __name__ == '__main__':
    select_polular_movie()