import pymysql.cursors
import connection

connection = connection.connect()

def add_user(uid, uname):
    cursor = connection.cursor()
    cursor.execute("SELECT idT FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    if results is None or str(results['idT']) != str(uid):
        connection = connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (idT, name, score) values ( %i, '%s', %i)" % (uid, uname, 0))
        connection.commit()   
        cursor.close()
        connection.close()
        return True

def score(uid):
    cursor = connection.cursor()
    cursor.execute("SELECT score FROM users WHERE idT = %i" % (uid))
    results = cursor.fetchone()
    cursor.close()
    connection.close()
    res = results["score"]
    return res